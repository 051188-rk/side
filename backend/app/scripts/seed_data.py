"""
Data seeding script

This script seeds the database with initial test data for development.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.repositories.firebase_client import firebase_client
from app.repositories.user_repository import UserRepository
from app.repositories.organization_repository import OrganizationRepository
from app.core.logging import log


async def seed_data():
    """Seed the database with initial test data."""
    try:
        log.info("Seeding database with test data...")
        
        # Initialize Firebase
        firebase_client.initialize()
        
        user_repo = UserRepository()
        org_repo = OrganizationRepository()
        
        # Create test organization
        org_id = await org_repo.create_organization(
            name="Test Organization",
            slug="test-org",
            plan="free"
        )
        log.info(f"Created test organization: {org_id}")
        
        # Create test users
        test_users = [
            {
                "email": "admin@test.com",
                "display_name": "Admin User",
                "role": "admin",
                "organization_id": org_id,
            },
            {
                "email": "user@test.com",
                "display_name": "Test User",
                "role": "user",
                "organization_id": org_id,
            },
        ]
        
        for user_data in test_users:
            user_id = await user_repo.create_user(**user_data)
            log.info(f"Created test user: {user_id}")
        
        log.info("Data seeding completed successfully")
        
    except Exception as e:
        log.error(f"Data seeding failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(seed_data())
