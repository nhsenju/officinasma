from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import AIDetection, Vehicle
from app.schemas.ai_detection import AIDetectionCreate, AIDetectionUpdate
from datetime import datetime
import cv2
import numpy as np
import easyocr
import os

class AIService:
    def __init__(self, db: Session):
        self.db = db
        # Initialize EasyOCR reader for license plate recognition
        self.reader = easyocr.Reader(['en'], gpu=False)

    def get_detection(self, detection_id: int) -> Optional[AIDetection]:
        return self.db.query(AIDetection).filter(AIDetection.id == detection_id).first()

    def get_detections(self, skip: int = 0, limit: int = 100) -> List[AIDetection]:
        return self.db.query(AIDetection).offset(skip).limit(limit).all()

    def get_unprocessed_detections(self) -> List[AIDetection]:
        return self.db.query(AIDetection).filter(AIDetection.processed == False).all()

    def create_detection(self, detection: AIDetectionCreate) -> AIDetection:
        db_detection = AIDetection(
            license_plate=detection.license_plate,
            confidence=detection.confidence,
            image_path=detection.image_path,
            processed=detection.processed,
            vehicle_id=detection.vehicle_id
        )
        self.db.add(db_detection)
        self.db.commit()
        self.db.refresh(db_detection)
        return db_detection

    def update_detection(self, detection_id: int, detection: AIDetectionUpdate) -> Optional[AIDetection]:
        db_detection = self.get_detection(detection_id)
        if not db_detection:
            return None
        
        update_data = detection.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detection, field, value)
        
        db_detection.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_detection)
        return db_detection

    def process_license_plate(self, image_path: str) -> Optional[dict]:
        """
        Process an image to detect and recognize license plates
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)

            # Find contours
            contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours by area (license plates are typically rectangular)
            plate_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / float(h)
                    if 2.0 <= aspect_ratio <= 5.0:  # License plate aspect ratio
                        plate_contours.append(contour)

            # Process each potential license plate region
            results = []
            for contour in plate_contours:
                x, y, w, h = cv2.boundingRect(contour)
                plate_region = gray[y:y+h, x:x+w]
                
                # Use EasyOCR to recognize text
                ocr_result = self.reader.readtext(plate_region)
                
                for (bbox, text, confidence) in ocr_result:
                    # Clean and validate license plate text
                    cleaned_text = self.clean_license_plate(text)
                    if self.is_valid_license_plate(cleaned_text):
                        results.append({
                            'license_plate': cleaned_text,
                            'confidence': confidence,
                            'bbox': bbox
                        })

            return results[0] if results else None

        except Exception as e:
            print(f"Error processing license plate: {e}")
            return None

    def clean_license_plate(self, text: str) -> str:
        """
        Clean and format license plate text
        """
        # Remove special characters and spaces
        cleaned = ''.join(c for c in text.upper() if c.isalnum())
        return cleaned

    def is_valid_license_plate(self, text: str) -> bool:
        """
        Validate if the recognized text looks like a license plate
        """
        # Italian license plate format: AA123BB or 123456
        if len(text) >= 5 and len(text) <= 10:
            # Check if it contains both letters and numbers
            has_letters = any(c.isalpha() for c in text)
            has_numbers = any(c.isdigit() for c in text)
            return has_letters and has_numbers
        return False

    def match_vehicle(self, license_plate: str) -> Optional[Vehicle]:
        """
        Match detected license plate to a vehicle in the database
        """
        return self.db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()

    def process_camera_stream(self, camera_url: str) -> Optional[dict]:
        """
        Process live camera stream for license plate detection
        """
        try:
            # Open camera stream
            cap = cv2.VideoCapture(camera_url)
            if not cap.isOpened():
                return None

            # Read frame
            ret, frame = cap.read()
            if not ret:
                cap.release()
                return None

            # Save frame temporarily
            temp_path = f"/tmp/camera_frame_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(temp_path, frame)
            cap.release()

            # Process the frame
            result = self.process_license_plate(temp_path)
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            return result

        except Exception as e:
            print(f"Error processing camera stream: {e}")
            return None

    def get_detection_statistics(self, start_date: datetime, end_date: datetime) -> dict:
        detections = self.db.query(AIDetection).filter(
            AIDetection.detected_at >= start_date,
            AIDetection.detected_at <= end_date
        ).all()
        
        total_detections = len(detections)
        processed_detections = len([d for d in detections if d.processed])
        average_confidence = sum(d.confidence for d in detections) / total_detections if total_detections > 0 else 0
        
        return {
            "total_detections": total_detections,
            "processed_detections": processed_detections,
            "processing_rate": (processed_detections / total_detections * 100) if total_detections > 0 else 0,
            "average_confidence": round(average_confidence, 2)
        }
