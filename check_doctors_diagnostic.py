from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

def check():
    load_dotenv()
    uri = os.environ.get('MONGO_URI')
    if not uri: return
    
    try:
        client = MongoClient(uri, tlsCAFile=certifi.where())
        db = client.get_default_database()
        
        # 1. Total Doctors
        docs = list(db.users.find({'role': 'doctor'}))
        print(f"Total Doctors: {len(docs)}")
        for d in docs:
            print(f"  - Name: {d.get('name')} | Email: {d.get('email')} | Verified: {d.get('verified')} | Specialty: {d.get('specialty')}")
        
        # 2. Images Assigned to "Dummy"
        # I'll search for 'dummy' in assigned_doctor_name case-insensitive
        dummies = list(db.images.find({'assigned_doctor_name': {'$regex': 'dummy', '$options': 'i'}}))
        print(f"\nImages assigned to 'Dummy': {len(dummies)}")
        for i in dummies:
            print(f"  - Image: {i.get('filename')} | Assigned: {i.get('assigned_doctor_name')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check()
