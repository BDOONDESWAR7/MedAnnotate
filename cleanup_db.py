import os
import certifi
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/medannotate')
CLIENT_KWARGS = {'tlsCAFile': certifi.where()} if 'mongodb+srv' in MONGO_URI else {}

print(f"Connecting to: {MONGO_URI.split('@')[-1] if '@' in MONGO_URI else MONGO_URI}")
client = MongoClient(MONGO_URI, **CLIENT_KWARGS)
db = client.get_default_database()

def cleanup():
    collections = ['users', 'images', 'annotations', 'payouts', 'fs.files', 'fs.chunks']
    for col in collections:
        count = db[col].count_documents({})
        print(f"Dropping {col} (records: {count})...")
        db[col].delete_many({})

def seed():
    print("Seeding admin...")
    admin_user = {
        'name': 'System Administrator',
        'email': 'admin@medannotate.com',
        'password': generate_password_hash('Admin@1234'),
        'role': 'admin',
        'verified': True,
        'created_at': datetime.utcnow(),
        'total_earnings': 0.0,
        'pending_earnings': 0.0,
        'paid_earnings': 0.0
    }
    db.users.insert_one(admin_user)
    print("Seed complete. Admin login: admin@medannotate.com / Admin@1234")

if __name__ == "__main__":
    confirm = input("ARE YOU SURE? This will WIPE the database. Type 'YES' to proceed: ")
    if confirm == 'YES':
        cleanup()
        seed()
    else:
        print("Aborted.")
