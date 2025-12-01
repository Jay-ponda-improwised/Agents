#!/usr/bin/env python3
"""
Database migration script that runs Alembic migrations
"""
import os
import sys
import logging

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run database migrations using Alembic"""
    try:
        # Import here to ensure the path is set correctly
        from alembic.config import Config
        from alembic import command
        from config.database import engine

        # Check if we can connect to the database
        logger.info("Testing database connection...")
        connection = engine.connect()
        connection.close()
        logger.info("Database connection successful!")

        # Run Alembic migrations
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully!")

    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()