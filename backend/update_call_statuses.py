#!/usr/bin/env python3
"""
Script to update call statuses in the database to match the new enum values
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

def update_call_statuses():
    """Update call statuses in the database"""
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Update statuses
        updates = [
            ("error", "fail"),
            ("pending", "upload"),
            ("processing", "transcription"),
            ("completed", "done")
        ]
        
        for old_status, new_status in updates:
            result = conn.execute(
                text("UPDATE calls SET status = :new_status WHERE status = :old_status"),
                {"new_status": new_status, "old_status": old_status}
            )
            print(f"Updated {result.rowcount} calls from '{old_status}' to '{new_status}'")
        
        conn.commit()
        print("Database update completed!")

if __name__ == "__main__":
    update_call_statuses()
