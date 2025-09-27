#!/usr/bin/env python3
"""
Database migration script to add detailed expense fields to existing Transaction table
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add detailed expense fields to existing database"""
    
    db_path = "./fiu_platform.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Creating new database with updated schema...")
        from app.fiu_models import create_tables
        create_tables()
        print("✅ New database created with detailed expense support")
        return
    
    print("🔄 Migrating existing database to support detailed expenses...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        new_columns = [
            ("merchant", "TEXT"),
            ("reason", "TEXT"),
            ("priority", "TEXT"),
            ("payment_method", "TEXT"),
            ("is_detailed", "BOOLEAN DEFAULT 0")
        ]
        
        columns_added = []
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE transactions ADD COLUMN {column_name} {column_type}")
                    columns_added.append(column_name)
                    print(f"✅ Added column: {column_name}")
                except sqlite3.Error as e:
                    print(f"⚠️  Warning adding {column_name}: {e}")
        
        if columns_added:
            conn.commit()
            print(f"✅ Successfully added {len(columns_added)} new columns for detailed expenses")
        else:
            print("ℹ️  Database already has detailed expense support")
        
        # Verify the migration
        cursor.execute("PRAGMA table_info(transactions)")
        all_columns = [column[1] for column in cursor.fetchall()]
        
        print(f"\n📋 Current transaction table columns:")
        for col in all_columns:
            print(f"   - {col}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database migration error: {e}")
    except Exception as e:
        print(f"❌ Migration error: {e}")

def verify_migration():
    """Verify that the migration was successful"""
    
    db_path = "./fiu_platform.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check for required columns
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        required_columns = ["merchant", "reason", "priority", "payment_method", "is_detailed"]
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Migration incomplete. Missing columns: {missing_columns}")
            return False
        else:
            print("✅ Migration verification successful - all detailed expense columns present")
            return True
        
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🏦 FIU Platform - Database Migration for Detailed Expenses")
    print("=" * 65)
    print(f"Migration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run migration
    migrate_database()
    
    print()
    
    # Verify migration
    verify_migration()
    
    print()
    print("=" * 65)
    print("📚 New Features Available After Migration:")
    print("   - Store detailed expense purposes and reasons")
    print("   - Track spending priorities (essential, important, optional, impulse)")
    print("   - Record merchant/store information")
    print("   - Monitor payment methods")
    print("   - Generate comprehensive expense analysis")
    print()
    print("🚀 You can now use the detailed expenses API:")
    print("   GET  /api/expenses/detailed/{user_id}")
    print("   POST /api/expense/detailed/add")