import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/medannotate')
CLIENT_KWARGS = {'tlsCAFile': certifi.where()} if 'mongodb+srv' in MONGO_URI else {}

client = MongoClient(MONGO_URI, **CLIENT_KWARGS)
db = client.get_default_database()

def create_indexes():
    print("Creating indexes...")
    try:
        db.users.create_index('email', unique=True)
        db.users.create_index([('role', 1), ('verified', 1)])
        db.images.create_index([('assigned_doctor_id', 1), ('status', 1)])
        db.images.create_index([('company_id', 1), ('status', 1)])
        db.images.create_index('status')
        db.images.create_index('department')
        db.annotations.create_index([('doctor_id', 1), ('status', 1)])
        db.annotations.create_index('image_id')
        db.payouts.create_index([('doctor_id', 1), ('status', 1)])
        db.payouts.create_index('status')
        print("Indexes created successfully.")
    except Exception as e:
        print(f"Index error: {e}")

if __name__ == "__main__":
    create_indexes()
