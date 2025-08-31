import requests
import os
from huggingface_hub import hf_hub_download

def download_model():
    """Scarica il modello YOLOv11 per il rilevamento delle targhe usando l'API di Hugging Face"""
    model_path = "models/license_plate_detector.pt"
    
    # Crea la directory se non esiste
    os.makedirs("models", exist_ok=True)
    
    print("Scaricando il modello YOLOv11 per il rilevamento delle targhe...")
    
    try:
        # Scarica il modello usando l'API di Hugging Face
        downloaded_path = hf_hub_download(
            repo_id="morsetechlab/yolov11-license-plate-detection",
            filename="yolov11x-license-plate.pt",
            local_dir="models"
        )
        
        # Rinomina il file se necessario
        if downloaded_path != model_path:
            os.rename(downloaded_path, model_path)
        
        print(f"Modello YOLOv11 scaricato con successo in {model_path}")
        print(f"Dimensione file: {os.path.getsize(model_path)} bytes")
        
    except Exception as e:
        print(f"Errore nel download del modello: {e}")
        print("Tentativo con modello YOLOv8 pre-addestrato...")
        
        # Fallback: usa YOLOv8 pre-addestrato
        try:
            from ultralytics import YOLO
            model = YOLO('yolov8n.pt')  # Modello nano pre-addestrato
            model.save(model_path)
            print(f"Modello YOLOv8 pre-addestrato salvato in {model_path}")
        except Exception as e2:
            print(f"Errore anche con il fallback: {e2}")

if __name__ == "__main__":
    download_model()
