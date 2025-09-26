#!/usr/bin/env python3
"""
Reset database with new schema
"""

import os
from app.fiu_models import Base, engine

def reset_database():
    """Drop and recreate all tables"""
    print("Resetting database...")
    
    # Remove existing database file
    db_file = "fiu_platform.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print("Removed existing database")
        except PermissionError:
            print("Database file in use, will recreate tables")
    
    # Drop and recreate tables
    try:
        Base.metadata.drop_all(bind=engine)
        print("Dropped existing tables")
    except:
        pass
    
    Base.metadata.create_all(bind=engine)
    print("Created new database with updated schema")

if __name__ == "__main__":
    reset_database()