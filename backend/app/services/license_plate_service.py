import cv2
import numpy as np
import re
from datetime import datetime, date
from typing import Optional, List, Dict
import asyncio
import logging
from sqlalchemy.orm import Session
from app.core.database import Vehicle, Appointment, Customer
from app.services.vehicle_service import VehicleService
from app.services.appointment_service import AppointmentService
import os
from pathlib import Path
from ultralytics import YOLO
import easyocr

logger = logging.getLogger(__name__)

class LicensePlateService:
    def __init__(self, db: Session):
        self.db = db
        self.vehicle_service = VehicleService(db)
        self.appointment_service = AppointmentService(db)
        self.is_streaming = False
        self.current_stream = None
        self.output_stream = None
        
        # Inizializza YOLO per il rilevamento targhe
        self.yolo_model = None
        self._load_yolo_model()
        
        # Inizializza EasyOCR per il riconoscimento testo
        self.ocr_reader = None
        self._load_ocr_reader()
        
        # Crea directory per salvare le foto delle targhe
        self.plates_dir = Path("uploads/plates")
        self.plates_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_yolo_model(self):
        """Carica il modello YOLO per il rilevamento targhe"""
        try:
            model_path = "models/license_plate_detector.pt"
            if os.path.exists(model_path):
                self.yolo_model = YOLO(model_path)
                logger.info("Modello YOLO caricato per il rilevamento targhe")
            else:
                # Fallback al modello pre-addestrato YOLOv8
                self.yolo_model = YOLO('yolov8n.pt')
                logger.info("Modello YOLOv8 pre-addestrato caricato")
        except Exception as e:
            logger.error(f"Errore nel caricamento modello YOLO: {e}")
            self.yolo_model = None
    
    def _load_ocr_reader(self):
        """Carica EasyOCR per il riconoscimento testo"""
        try:
            # Inizializza EasyOCR per italiano e inglese
            self.ocr_reader = easyocr.Reader(['it', 'en'], gpu=False)
            logger.info("EasyOCR caricato per il riconoscimento testo")
        except Exception as e:
            logger.error(f"Errore nel caricamento EasyOCR: {e}")
            self.ocr_reader = None
        
    def start_livestream_monitoring(self, stream_url: str = "0", output_url: str = None):
        """Avvia il monitoraggio del livestream per il riconoscimento targhe"""
        try:
            self.is_streaming = True
            self.current_stream = cv2.VideoCapture(stream_url)
            
            if not self.current_stream.isOpened():
                logger.error(f"Impossibile aprire lo stream: {stream_url}")
                return False
            
            # Configura lo stream di output se specificato
            if output_url:
                self._setup_output_stream(output_url)
                
            logger.info("Livestream monitoring avviato")
            return True
            
        except Exception as e:
            logger.error(f"Errore nell'avvio del livestream: {e}")
            return False
    
    def _setup_output_stream(self, output_url: str):
        """Configura lo stream di output con blur"""
        try:
            # Ottieni le proprietà del video di input
            fps = int(self.current_stream.get(cv2.CAP_PROP_FPS))
            width = int(self.current_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.current_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Configura il codec per l'output
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.output_stream = cv2.VideoWriter(output_url, fourcc, fps, (width, height))
            
            logger.info(f"Stream di output configurato: {output_url}")
            
        except Exception as e:
            logger.error(f"Errore nella configurazione output stream: {e}")
    
    def stop_livestream_monitoring(self):
        """Ferma il monitoraggio del livestream"""
        self.is_streaming = False
        if self.current_stream:
            self.current_stream.release()
        if self.output_stream:
            self.output_stream.release()
        logger.info("Livestream monitoring fermato")
    
    def apply_blur_to_faces(self, frame):
        """Applica blur alle facce nel frame"""
        try:
            # Per ora saltiamo il blur delle facce per concentrarci sul rilevamento targhe
            # TODO: Implementare rilevamento facce se necessario
            pass
        except Exception as e:
            logger.error(f"Errore nell'applicazione blur facce: {e}")
            
        return frame
    
    def apply_blur_to_plates(self, frame, detected_plates):
        """Applica blur alle targhe rilevate"""
        try:
            for plate_info in detected_plates:
                bbox = plate_info['bbox']
                x, y, w, h = bbox
                
                # Applica blur gaussiano alla regione della targa
                plate_roi = frame[y:y+h, x:x+w]
                blurred_plate = cv2.GaussianBlur(plate_roi, (99, 99), 30)
                frame[y:y+h, x:x+w] = blurred_plate
                
        except Exception as e:
            logger.error(f"Errore nell'applicazione blur targhe: {e}")
            
        return frame
    
    def save_plate_image(self, frame, bbox, license_plate):
        """Salva l'immagine della targa rilevata"""
        try:
            x, y, w, h = bbox
            plate_region = frame[y:y+h, x:x+w]
            
            # Genera nome file unico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"plate_{license_plate}_{timestamp}.jpg"
            filepath = self.plates_dir / filename
            
            # Salva l'immagine
            cv2.imwrite(str(filepath), plate_region)
            logger.info(f"Immagine targa salvata: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Errore nel salvataggio immagine targa: {e}")
            return None
    
    def detect_license_plate(self, frame) -> List[Dict]:
        """Riconosce le targhe in un frame usando YOLO + EasyOCR"""
        detected_plates = []
        
        try:
            if self.yolo_model is None:
                logger.warning("Modello YOLO non disponibile")
                return detected_plates
            
            # Usa YOLO per rilevare oggetti (targhe)
            results = self.yolo_model(frame, conf=0.5, verbose=False)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Ottieni coordinate del bounding box
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        # Estrai la regione della targa
                        plate_region = frame[y1:y2, x1:x2]
                        
                        if plate_region.size == 0:
                            continue
                        
                        # Usa EasyOCR per riconoscere il testo
                        license_plate = self._extract_text_from_image(plate_region)
                        
                        if license_plate and self._is_valid_italian_plate(license_plate):
                            detected_plates.append({
                                'license_plate': license_plate,
                                'bbox': (x1, y1, x2-x1, y2-y1),
                                'confidence': float(box.conf[0])
                            })
                            logger.info(f"Targa rilevata: {license_plate} (confidenza: {float(box.conf[0]):.2f})")
            
            return detected_plates
            
        except Exception as e:
            logger.error(f"Errore nel riconoscimento targa: {e}")
            return []
    
    def _extract_text_from_image(self, image) -> Optional[str]:
        """Estrae testo dall'immagine usando EasyOCR"""
        try:
            if self.ocr_reader is None:
                logger.warning("EasyOCR non disponibile")
                return None
            
            # Usa EasyOCR per riconoscere il testo
            results = self.ocr_reader.readtext(image)
            
            if results:
                # Prendi il testo con la confidenza più alta
                best_result = max(results, key=lambda x: x[2])
                text = best_result[1].strip()
                confidence = best_result[2]
                
                # Filtra solo caratteri alfanumerici e spazi
                text = re.sub(r'[^A-Z0-9\s]', '', text.upper())
                text = re.sub(r'\s+', '', text)  # Rimuovi spazi
                
                logger.info(f"Testo riconosciuto: '{text}' (confidenza: {confidence:.2f})")
                
                # Restituisci solo se la confidenza è alta e il testo ha senso
                if confidence > 0.3 and len(text) >= 5:
                    return text
            
            return None
            
        except Exception as e:
            logger.error(f"Errore nell'estrazione testo: {e}")
            return None
    
    def _is_valid_italian_plate(self, plate: str) -> bool:
        """Verifica se la targa segue il formato italiano"""
        # Formato italiano: AA123AA o AA123AA
        pattern = r'^[A-Z]{2}\d{3}[A-Z]{2}$'
        return bool(re.match(pattern, plate))
    
    def find_vehicle_by_plate(self, license_plate: str) -> Optional[Vehicle]:
        """Cerca un veicolo nel database tramite targa"""
        try:
            return self.vehicle_service.get_vehicle_by_license_plate(license_plate)
        except Exception as e:
            logger.error(f"Errore nella ricerca veicolo: {e}")
            return None
    
    def check_appointments_for_vehicle(self, vehicle_id: int, check_date: date = None) -> List[Appointment]:
        """Verifica se un veicolo ha appuntamenti per una data specifica"""
        try:
            if not check_date:
                check_date = date.today()
            
            # Ottieni tutti gli appuntamenti del veicolo
            appointments = self.appointment_service.get_appointments_by_vehicle(vehicle_id)
            
            # Filtra per data
            today_appointments = []
            for appointment in appointments:
                appointment_date = appointment.appointment_date.date()
                if appointment_date == check_date:
                    today_appointments.append(appointment)
            
            return today_appointments
            
        except Exception as e:
            logger.error(f"Errore nella verifica appuntamenti: {e}")
            return []
    
    def get_customer_info(self, vehicle: Vehicle) -> Optional[Dict]:
        """Ottiene informazioni sul cliente proprietario del veicolo"""
        try:
            if vehicle.customer:
                return {
                    "id": vehicle.customer.id,
                    "full_name": vehicle.customer.full_name,
                    "email": vehicle.customer.email,
                    "phone": vehicle.customer.phone
                }
            return None
            
        except Exception as e:
            logger.error(f"Errore nel recupero info cliente: {e}")
            return None
    
    async def process_detected_plate(self, license_plate: str) -> Dict:
        """Processa una targa rilevata"""
        try:
            # Cerca il veicolo nel database
            vehicle = self.find_vehicle_by_plate(license_plate)
            
            if vehicle:
                # Ottieni informazioni cliente
                customer_info = self.get_customer_info(vehicle)
                
                # Verifica appuntamenti per oggi
                appointments = self.check_appointments_for_vehicle(vehicle.id)
                
                # Prepara il risultato
                result = {
                    "license_plate": license_plate,
                    "detected_at": datetime.now().isoformat(),
                    "vehicle_found": True,
                    "vehicle_info": {
                        "id": vehicle.id,
                        "brand": vehicle.brand,
                        "model": vehicle.model,
                        "year": vehicle.year,
                        "color": vehicle.color,
                        "fuel_type": vehicle.fuel_type
                    },
                    "customer_info": customer_info,
                    "appointments": [
                        {
                            "id": apt.id,
                            "appointment_date": apt.appointment_date.isoformat(),
                            "service": {
                                "id": apt.service.id,
                                "name": apt.service.name
                            } if apt.service else None
                        } for apt in appointments
                    ],
                    "message": f"Veicolo trovato: {vehicle.brand} {vehicle.model}"
                }
                
                if appointments:
                    result["message"] += f" - {len(appointments)} appuntamento/i per oggi"
                else:
                    result["message"] += " - Nessun appuntamento per oggi"
                    
            else:
                result = {
                    "license_plate": license_plate,
                    "detected_at": datetime.now().isoformat(),
                    "vehicle_found": False,
                    "vehicle_info": None,
                    "customer_info": None,
                    "appointments": [],
                    "message": f"Targa {license_plate} non trovata nel database"
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Errore nel processamento targa: {e}")
            return {
                "license_plate": license_plate,
                "detected_at": datetime.now().isoformat(),
                "vehicle_found": False,
                "vehicle_info": None,
                "customer_info": None,
                "appointments": [],
                "message": "Errore nel processamento"
            }
    
    async def monitor_livestream(self, stream_url: str = "rtsp://host.docker.internal:8554/webcam", output_url: str = None):
        """Monitora continuamente il livestream per il riconoscimento targhe"""
        # Usa sempre lo stream fisso
        fixed_stream_url = "rtsp://host.docker.internal:8554/webcam"
        if not self.start_livestream_monitoring(fixed_stream_url, output_url):
            return
        
        logger.info("Avvio monitoraggio livestream per riconoscimento targhe")
        
        try:
            frame_count = 0
            while self.is_streaming:
                ret, frame = self.current_stream.read()
                
                if not ret:
                    logger.warning("Frame non letto correttamente")
                    continue
                
                frame_count += 1
                if frame_count % 30 == 0:  # Log ogni 30 frame (circa 1 secondo a 30fps)
                    logger.info(f"Processando frame {frame_count}")
                
                # Applica blur alle facce
                frame = self.apply_blur_to_faces(frame)
                
                # Riconosci targhe nel frame
                detected_plates = self.detect_license_plate(frame)
                
                # Applica blur alle targhe rilevate
                frame = self.apply_blur_to_plates(frame, detected_plates)
                
                # Processa ogni targa rilevata
                for plate_info in detected_plates:
                    license_plate = plate_info['license_plate']
                    bbox = plate_info['bbox']
                    
                    logger.info(f"Targa rilevata: {license_plate}")
                    
                    # Salva l'immagine della targa
                    plate_image_path = self.save_plate_image(frame, bbox, license_plate)
                    
                    # Processa la targa rilevata
                    result = await self.process_detected_plate(license_plate)
                    result['plate_image_path'] = plate_image_path
                    
                    # Log del risultato
                    if result.get("vehicle_found"):
                        if result.get("appointments"):
                            logger.info(f"✅ {result['message']}")
                        else:
                            logger.info(f"ℹ️ {result['message']}")
                    else:
                        logger.info(f"❌ {result['message']}")
                    
                    # Qui potresti inviare notifiche, salvare nel database, etc.
                    await self._handle_plate_detection(result)
                
                # Scrivi il frame processato nello stream di output
                if self.output_stream:
                    self.output_stream.write(frame)
                
                # Pausa per non sovraccaricare la CPU
                await asyncio.sleep(0.1)  # 10 FPS
                
        except Exception as e:
            logger.error(f"Errore nel monitoraggio livestream: {e}")
        finally:
            self.stop_livestream_monitoring()
    
    async def _handle_plate_detection(self, result: Dict):
        """Gestisce il risultato del riconoscimento targa"""
        try:
            # Salva la rilevazione nel database
            from app.core.database import AIDetection
            
            detection = AIDetection(
                license_plate=result["license_plate"],
                confidence_score=0.85,  # Simulato
                detection_data=result,
                is_automatic=True
            )
            
            self.db.add(detection)
            self.db.commit()
            
            # Se c'è un appuntamento, invia notifica
            if result.get("appointments"):
                await self._send_appointment_notification(result)
                
        except Exception as e:
            logger.error(f"Errore nella gestione rilevazione: {e}")
    
    async def _send_appointment_notification(self, result: Dict):
        """Invia notifica per appuntamento rilevato"""
        try:
            # Qui implementeresti l'invio di notifiche
            # Email, SMS, push notification, etc.
            
            customer = result.get("customer_info")
            vehicle = result.get("vehicle_info")
            appointments = result.get("appointments")
            
            if customer and vehicle and appointments:
                message = f"""
                🚗 CLIENTE ARRIVATO
                
                Targa: {result['license_plate']}
                Veicolo: {vehicle['brand']} {vehicle['model']} ({vehicle['year']})
                Cliente: {customer['full_name']}
                Appuntamenti: {len(appointments)}
                
                Orario rilevamento: {result['detected_at']}
                """
                
                logger.info(f"Notifica appuntamento: {message}")
                
        except Exception as e:
            logger.error(f"Errore nell'invio notifica: {e}")
