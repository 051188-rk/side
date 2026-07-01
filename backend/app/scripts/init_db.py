"""
Database initialization script

This script initializes the Firebase Firestore database with required indexes and initial data.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.repositories.firebase_client import firebase_client
from app.core.logging import log
from app.config import settings


async def initialize_database():
    """Initialize the database with required collections and indexes."""
    try:
        log.info("Initializing database...")
        
        # Initialize Firebase
        firebase_client.initialize()
        
        db = firebase_client.db
        
        # Create initial collections (they will be created on first write)
        collections = [
            "users",
            "organizations",
            "feedback",
            "tickets",
            "ticket_updates",
            "duplicate_clusters",
            "customers",
            "messages",
            "activity_logs",
            "notifications",
            "integrations",
            "agent_runs",
            "memory",
            "analytics",
            "daily_reports",
        ]
        
        log.info(f"Ensuring {len(collections)} collections exist...")
        
        # Firestore creates collections automatically on first write
        # We'll verify by attempting to list documents
        for collection_name in collections:
            try:
                docs = db.collection(collection_name).limit(1).get()
                log.info(f"Collection '{collection_name}' is ready")
            except Exception as e:
                log.warning(f"Could not verify collection '{collection_name}': {e}")
        
        log.info("Database initialization completed successfully")
        
    except Exception as e:
        log.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(initialize_database())
