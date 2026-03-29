import sys, os, certifi
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', '')
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def restore():
    print("--- RESTORING ORIGINAL MEDANNOTATE DEMO DATA ---")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000, tlsCAFile=certifi.where())
        db = client['medannotate']
        print(f"Connected to {db.name}")

        # 1. CLEANUP
        collections = ['users', 'images', 'annotations', 'payouts', 'fs.files', 'fs.chunks']
        for col in collections:
            db[col].delete_many({})
            print(f"Cleared {col}")

        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)

        # 2. RESTORE DEMO DOCTORS
        # Elena Petrova - The original lead doctor
        elena_id = db.users.insert_one({
            'name': 'Dr. Elena Petrova', 'email': 'doctor@demo.com',
            'password': generate_password_hash('doctor123'),
            'role': 'doctor', 'verified': True, 'active': True,
            'specialty': 'Radiology', 'license_number': 'EP-99421',
            'total_earnings': 1250.80, 'pending_earnings': 14.0, 'paid_earnings': 1236.80,
            'created_at': now - timedelta(days=32)
        }).inserted_id
        print("Restored Dr. Elena Petrova")

        # Marcus Thorne - Second specialist
        marcus_id = db.users.insert_one({
            'name': 'Dr. Marcus Thorne', 'email': 'marcus@demo.com',
            'password': generate_password_hash('doctor123'),
            'role': 'doctor', 'verified': True, 'active': True,
            'specialty': 'Dermatology', 'license_number': 'MT-22819',
            'total_earnings': 412.00, 'pending_earnings': 0.0, 'paid_earnings': 412.00,
            'created_at': now - timedelta(days=15)
        }).inserted_id
        print("Restored Dr. Marcus Thorne")

        # 3. RESTORE DEMO COMPANY
        ai_corp_id = db.users.insert_one({
            'name': 'AI Corp Admin', 'email': 'company@demo.com', 'role': 'company',
            'company_name': 'AI Corp', 'password': generate_password_hash('company123'),
            'verified': True, 'active': True, 'created_at': now - timedelta(days=40)
        }).inserted_id
        print("Restored AI Corp")

        # 4. RESTORE ADMIN
        db.users.insert_one({
            'name': 'MedLabel Admin', 'email': 'admin@demo.com', 'role': 'admin',
            'password': generate_password_hash('admin123'),
            'verified': True, 'active': True, 'created_at': now - timedelta(days=50)
        })
        print("Restored Admin Account")

        # 5. RESTORE IMAGES
        # Add 5 demo images (X-rays and Scans)
        img1_id = db.images.insert_one({
            'filename': 'XRAY-001-CHEST.dcm', 'department': 'Radiology',
            'status': 'approved', 'company_id': ai_corp_id,
            'company_name': 'AI Corp', 'assigned_doctor_id': elena_id,
            'assigned_doctor_name': 'Dr. Elena Petrova', 'anonymized': True,
            'batch_name': 'Batch_2024_03', 'file_size': 312456, 'created_at': day_ago
        }).inserted_id

        img2_id = db.images.insert_one({
            'filename': 'SCAN-DERM-092.png', 'department': 'Dermatology',
            'status': 'assigned', 'company_id': ai_corp_id,
            'company_name': 'AI Corp', 'assigned_doctor_id': marcus_id,
            'assigned_doctor_name': 'Dr. Marcus Thorne', 'anonymized': True,
            'batch_name': 'Skin_Lesion_A', 'file_size': 128456, 'created_at': now
        }).inserted_id

        img3_id = db.images.insert_one({
            'filename': 'MRI-NEURO-771.dcm', 'department': 'Neurology',
            'status': 'qa_review', 'company_id': ai_corp_id,
            'company_name': 'AI Corp', 'assigned_doctor_id': elena_id,
            'assigned_doctor_name': 'Dr. Elena Petrova', 'anonymized': True,
            'batch_name': 'Brain_Scans_Jan', 'file_size': 2045612, 'created_at': day_ago
        }).inserted_id

        # 6. RESTORE ANNOTATIONS
        db.annotations.insert_one({
            'image_id': img1_id, 'doctor_id': elena_id, 'doctor_name': 'Dr. Elena Petrova',
            'labels': ['Pneumonia', 'Pleural Effusion'], 'notes': 'Significant opacity in lower left lobe.',
            'confidence': 98, 'status': 'qa_approved', 'created_at': day_ago
        })

        db.annotations.insert_one({
            'image_id': img3_id, 'doctor_id': elena_id, 'doctor_name': 'Dr. Elena Petrova',
            'labels': ['Glioma'], 'notes': 'Mass detected in frontal lobe.',
            'confidence': 85, 'status': 'submitted', 'created_at': day_ago
        })

        print("--- RESTORATION COMPLETE ---")
        print("Login with doctor@demo.com | company@demo.com | admin@demo.com")
        print("Password: doctor123 | company123 | admin123")

    except Exception as e:
        print(f"Restoration failed: {e}")

if __name__ == "__main__":
    restore()
