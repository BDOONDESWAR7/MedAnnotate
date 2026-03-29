import os
from app import create_app
from extensions import mongo
from routes.auth import generate_password_hash
from datetime import datetime
from bson import ObjectId
import io
import gridfs
from flask import Flask

# Mock request and context
app = create_app()

def test_internal_logic():
    with app.app_context():
        print("Testing internal DB logic...")
        
        # 1. Test User Insert
        email = f"debug_test_{int(datetime.utcnow().timestamp())}@test.com"
        print(f"Inserting user: {email}")
        user_doc = {
            'name': 'Debug User', 'email': email,
            'password': generate_password_hash('Password123!'),
            'role': 'company', 'verified': True, 'active': True,
            'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow(),
            'company_name': 'Debug Corp'
        }
        res = mongo.db.users.insert_one(user_doc)
        uid = res.inserted_id
        print(f"User inserted: {uid}")
        
        # 2. Test Image/GridFS Insert (simulating upload)
        print("Inserting image to GridFS...")
        fs = gridfs.GridFS(mongo.db)
        file_bytes = b"fake medical image data"
        gridfs_id = fs.put(io.BytesIO(file_bytes), filename="debug.png")
        print(f"GridFS ID: {gridfs_id}")
        
        print("Inserting image metadata...")
        img_doc = {
            'filename': 'debug.png', 'department': 'Radiology',
            'status': 'pending', 'company_id': uid,
            'gridfs_id': gridfs_id, 'created_at': datetime.utcnow()
        }
        img_res = mongo.db.images.insert_one(img_doc)
        print(f"Image metadata inserted: {img_res.inserted_id}")
        
        # Verify
        found = mongo.db.images.find_one({'_id': img_res.inserted_id})
        if found:
            print("VERIFIED: Image persisted and found in DB.")
        else:
            print("FAILURE: Image NOT found after insertion!")

if __name__ == "__main__":
    try:
        test_internal_logic()
    except Exception as e:
        import traceback
        traceback.print_exc()
