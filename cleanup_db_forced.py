import os, certifi
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', '')
CLIENT_KWARGS = {'tlsCAFile': certifi.where()} if 'mongodb+srv' in MONGO_URI else {}

def wipe_and_seed():
    print("--- STARTING FORCED DATABASE CLEANUP & SEEDING (PRODUCTION RESET) ---")
    try:
        client = MongoClient(MONGO_URI, **CLIENT_KWARGS)
        db = client.get_default_database()
        
        collections = ['users', 'images', 'annotations', 'payouts', 'fs.files', 'fs.chunks']
        for col in collections:
            count = db[col].count_documents({})
            print(f"Deleting {count} records from {col}...")
            db[col].delete_many({})
        
        # Seed Super Admin
        print("Seeding Super Admin...")
        super_admin = {
            'name': 'Super Administrator',
            'email': 'superadmin@medannotate.com',
            'password': generate_password_hash('SuperAdmin@2024'),
            'role': 'admin',
            'verified': True,
            'active': True,
            'created_at': datetime.utcnow(),
            'total_earnings': 0.0,
            'pending_earnings': 0.0,
            'paid_earnings': 0.0
        }
        db.users.insert_one(super_admin)
        print("--- SETUP SUCCESSFUL: SUPER ADMIN CREATED ---")
        print("Email: superadmin@medannotate.com")
        print("Pass:  SuperAdmin@2024")
        
    except Exception as e:
        print(f"Cleanup/Seed failed: {e}")

if __name__ == "__main__":
    wipe_and_seed()
