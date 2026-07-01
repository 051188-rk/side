"""
Documentation generation script

This script generates API documentation from the FastAPI application.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.docs.api_reference import APIReferenceGenerator
from app.core.logging import log


async def generate_documentation():
    """Generate API documentation."""
    try:
        log.info("Generating API documentation...")
        
        generator = APIReferenceGenerator(app)
        
        # Save OpenAPI spec
        generator.save_openapi_json("openapi.json")
        log.info("Saved OpenAPI specification to openapi.json")
        
        # Save Markdown docs
        generator.save_markdown_docs("API.md")
        log.info("Saved Markdown documentation to API.md")
        
        log.info("Documentation generation completed successfully")
        
    except Exception as e:
        log.error(f"Documentation generation failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(generate_documentation())
