from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import os
import tempfile
from app.core.database import get_db
from app.schemas.ai_detection import AIDetection, AIDetectionCreate, AIDetectionUpdate
from app.services.ai_service import AIService
from app.services.license_plate_service import LicensePlateService
import asyncio
import logging
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)

# Variabile globale per tenere traccia del servizio di monitoraggio
license_plate_service = None
monitoring_task = None

@router.get("/", response_model=List[AIDetection])
def get_detections(
    skip: int = 0,
    limit: int = 100,
    processed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all AI detections with optional filters"""
    service = AIService(db)
    detections = service.get_detections(skip=skip, limit=limit)
    
    if processed is not None:
        detections = [d for d in detections if d.processed == processed]
    
    return detections

@router.post("/detect", response_model=dict)
async def detect_license_plate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Detect license plate from uploaded image"""
    service = AIService(db)
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Process the image
        result = service.process_license_plate(temp_path)
        
        if result:
            # Create detection record
            detection = AIDetectionCreate(
                license_plate=result['license_plate'],
                confidence=result['confidence'],
                image_path=temp_path,
                processed=False
            )
            
            # Try to match with existing vehicle
            vehicle = service.match_vehicle(result['license_plate'])
            if vehicle:
                detection.vehicle_id = vehicle.id
                detection.processed = True
            
            db_detection = service.create_detection(detection)
            
            return {
                "success": True,
                "license_plate": result['license_plate'],
                "confidence": result['confidence'],
                "vehicle_found": vehicle is not None,
                "detection_id": db_detection.id
            }
        else:
            return {
                "success": False,
                "message": "No license plate detected"
            }
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@router.post("/stream", response_model=dict)
def process_camera_stream(
    camera_url: str,
    db: Session = Depends(get_db)
):
    """Process live camera stream for license plate detection"""
    service = AIService(db)
    result = service.process_camera_stream(camera_url)
    
    if result:
        # Create detection record
        detection = AIDetectionCreate(
            license_plate=result['license_plate'],
            confidence=result['confidence'],
            processed=False
        )
        
        # Try to match with existing vehicle
        vehicle = service.match_vehicle(result['license_plate'])
        if vehicle:
            detection.vehicle_id = vehicle.id
            detection.processed = True
        
        db_detection = service.create_detection(detection)
        
        return {
            "success": True,
            "license_plate": result['license_plate'],
            "confidence": result['confidence'],
            "vehicle_found": vehicle is not None,
            "detection_id": db_detection.id
        }
    else:
        return {
            "success": False,
            "message": "No license plate detected from stream"
        }

@router.get("/{detection_id}", response_model=AIDetection)
def get_detection(
    detection_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific detection by ID"""
    service = AIService(db)
    detection = service.get_detection(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@router.put("/{detection_id}", response_model=AIDetection)
def update_detection(
    detection_id: int,
    detection: AIDetectionUpdate,
    db: Session = Depends(get_db)
):
    """Update a detection"""
    service = AIService(db)
    updated_detection = service.update_detection(detection_id, detection)
    if not updated_detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return updated_detection

@router.get("/unprocessed/", response_model=List[AIDetection])
def get_unprocessed_detections(db: Session = Depends(get_db)):
    """Get all unprocessed detections"""
    service = AIService(db)
    return service.get_unprocessed_detections()

@router.get("/statistics/")
def get_detection_statistics(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Get AI detection statistics for a date range"""
    service = AIService(db)
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    return service.get_detection_statistics(start_datetime, end_datetime)

@router.post("/livestream/start")
async def start_livestream_monitoring(
    stream_url: str = "0",
    output_url: str = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Avvia il monitoraggio del livestream per il riconoscimento targhe"""
    global license_plate_service, monitoring_task
    
    try:
        # Crea il servizio se non esiste
        if license_plate_service is None:
            license_plate_service = LicensePlateService(db)
        
        # Usa sempre lo stream fisso (host.docker.internal per accesso dall'interno del container)
        fixed_stream_url = "rtsp://host.docker.internal:8554/webcam"
        
        # Avvia il monitoraggio in background
        if monitoring_task is None or monitoring_task.done():
            monitoring_task = asyncio.create_task(
                license_plate_service.monitor_livestream(fixed_stream_url, output_url)
            )
            
        return {
            "status": "success",
            "message": f"Monitoraggio livestream avviato per: {fixed_stream_url}",
            "stream_url": fixed_stream_url,
            "output_url": output_url
        }
        
    except Exception as e:
        logger.error(f"Errore nell'avvio monitoraggio: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'avvio monitoraggio: {str(e)}")

@router.post("/livestream/stop")
async def stop_livestream_monitoring():
    """Ferma il monitoraggio del livestream"""
    global license_plate_service, monitoring_task
    
    try:
        if license_plate_service:
            license_plate_service.stop_livestream_monitoring()
        
        if monitoring_task and not monitoring_task.done():
            monitoring_task.cancel()
            monitoring_task = None
            
        return {
            "status": "success",
            "message": "Monitoraggio livestream fermato"
        }
        
    except Exception as e:
        logger.error(f"Errore nell'arresto monitoraggio: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'arresto monitoraggio: {str(e)}")

@router.get("/livestream/status")
async def get_livestream_status():
    """Ottiene lo stato del monitoraggio livestream"""
    global license_plate_service, monitoring_task
    
    is_active = False
    if license_plate_service:
        is_active = license_plate_service.is_streaming
    
    is_task_running = False
    if monitoring_task:
        is_task_running = not monitoring_task.done()
    
    return {
        "is_streaming": is_active,
        "is_task_running": is_task_running,
        "status": "active" if (is_active or is_task_running) else "inactive"
    }

@router.post("/plate/detect")
async def detect_license_plate(
    license_plate: str,
    db: Session = Depends(get_db)
):
    """Processa manualmente una targa rilevata"""
    try:
        service = LicensePlateService(db)
        result = await service.process_detected_plate(license_plate)
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Errore nel processamento targa: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel processamento: {str(e)}")

@router.get("/plate/search/{license_plate}")
async def search_license_plate(
    license_plate: str,
    db: Session = Depends(get_db)
):
    """Cerca informazioni su una targa specifica"""
    try:
        service = LicensePlateService(db)
        
        # Cerca il veicolo
        vehicle = service.find_vehicle_by_plate(license_plate)
        
        if not vehicle:
            return {
                "status": "not_found",
                "message": f"Targa {license_plate} non trovata nel database",
                "data": None
            }
        
        # Ottieni informazioni cliente
        customer = service.get_customer_info(vehicle)
        
        # Verifica appuntamenti per oggi
        appointments = service.check_appointments_for_vehicle(vehicle.id)
        
        result = {
            "license_plate": license_plate,
            "vehicle": {
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "color": vehicle.color,
                "fuel_type": vehicle.fuel_type
            },
            "customer": {
                "id": customer.id,
                "full_name": customer.full_name,
                "phone": customer.phone,
                "email": customer.email
            } if customer else None,
            "appointments_today": [
                {
                    "id": apt.id,
                    "appointment_date": apt.appointment_date,
                    "service_name": apt.service.name if apt.service else "Servizio non specificato",
                    "status": apt.status
                }
                for apt in appointments
            ],
            "has_appointment_today": len(appointments) > 0
        }
        
        return {
            "status": "found",
            "message": f"Veicolo trovato: {vehicle.brand} {vehicle.model}",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Errore nella ricerca targa: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nella ricerca: {str(e)}")

@router.get("/detections/recent")
async def get_recent_detections(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Ottiene le rilevazioni recenti"""
    try:
        from app.core.database import AIDetection
        
        detections = db.query(AIDetection)\
            .order_by(AIDetection.created_at.desc())\
            .limit(limit)\
            .all()
        
        return {
            "status": "success",
            "data": [
                {
                    "id": detection.id,
                    "license_plate": detection.license_plate,
                    "confidence_score": getattr(detection, 'confidence_score', detection.confidence if hasattr(detection, 'confidence') else 0.0),
                    "detection_data": getattr(detection, 'detection_data', {}),
                    "is_automatic": getattr(detection, 'is_automatic', True),
                    "created_at": detection.created_at
                }
                for detection in detections
            ]
        }
        
    except Exception as e:
        logger.error(f"Errore nel recupero rilevazioni: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero: {str(e)}")

@router.get("/stats")
async def get_ai_stats(db: Session = Depends(get_db)):
    """Ottiene statistiche del sistema AI"""
    try:
        from app.core.database import AIDetection, Vehicle, Appointment
        from datetime import datetime, timedelta
        
        # Statistiche generali
        total_detections = db.query(AIDetection).count()
        total_vehicles = db.query(Vehicle).count()
        
        # Rilevazioni oggi
        today = datetime.now().date()
        today_detections = db.query(AIDetection)\
            .filter(AIDetection.created_at >= today)\
            .count()
        
        # Appuntamenti oggi
        today_appointments = db.query(Appointment)\
            .filter(Appointment.appointment_date >= today)\
            .filter(Appointment.appointment_date < today + timedelta(days=1))\
            .count()
        
        # Rilevazioni con appuntamenti
        detections_with_appointments = db.query(AIDetection)\
            .filter(AIDetection.detection_data['appointments'].astext != '[]')\
            .count()
        
        return {
            "status": "success",
            "data": {
                "total_detections": total_detections,
                "total_vehicles": total_vehicles,
                "today_detections": today_detections,
                "today_appointments": today_appointments,
                "detections_with_appointments": detections_with_appointments,
                "accuracy_rate": (detections_with_appointments / total_detections * 100) if total_detections > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Errore nel recupero statistiche: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero statistiche: {str(e)}")

@router.get("/plates/images")
async def get_plate_images():
    """Ottiene la lista delle immagini delle targhe salvate"""
    try:
        plates_dir = Path("uploads/plates")
        
        if not plates_dir.exists():
            return {
                "status": "success",
                "data": [],
                "message": "Nessuna immagine trovata"
            }
        
        # Ottieni tutti i file .jpg nella directory
        image_files = list(plates_dir.glob("*.jpg"))
        
        images = []
        for image_file in image_files:
            # Estrai informazioni dal nome del file
            filename = image_file.name
            if filename.startswith("plate_"):
                # Formato: plate_AB123CD_20231201_143022.jpg
                parts = filename.replace(".jpg", "").split("_")
                if len(parts) >= 3:
                    license_plate = parts[1]
                    timestamp = f"{parts[2]}_{parts[3]}"
                    
                    images.append({
                        "filename": filename,
                        "license_plate": license_plate,
                        "timestamp": timestamp,
                        "filepath": str(image_file),
                        "size": image_file.stat().st_size
                    })
        
        # Ordina per timestamp (più recenti prima)
        images.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "status": "success",
            "data": images,
            "total": len(images)
        }
        
    except Exception as e:
        logger.error(f"Errore nel recupero immagini targhe: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero immagini: {str(e)}")

@router.get("/plates/images/{filename}")
async def get_plate_image(filename: str):
    """Ottiene una specifica immagine di targa"""
    try:
        plates_dir = Path("uploads/plates")
        image_path = plates_dir / filename
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Immagine non trovata")
        
        return FileResponse(
            path=str(image_path),
            media_type="image/jpeg",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errore nel recupero immagine: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero immagine: {str(e)}")

@router.delete("/plates/images/{filename}")
async def delete_plate_image(filename: str):
    """Elimina una specifica immagine di targa"""
    try:
        plates_dir = Path("uploads/plates")
        image_path = plates_dir / filename
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Immagine non trovata")
        
        # Elimina il file
        image_path.unlink()
        
        return {
            "status": "success",
            "message": f"Immagine {filename} eliminata"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errore nell'eliminazione immagine: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'eliminazione: {str(e)}")
