import os
import certifi
from pymongo import MongoClient
from bson import ObjectId
import gridfs
import io
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
print(f"Connecting to: {MONGO_URI.split('@')[-1] if '@' in MONGO_URI else 'local'}")

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where() if 'mongodb+srv' in MONGO_URI else None)
    db = client.get_default_database()
    print(f"Database: {db.name}")
    
    # 1. Test standard collection write
    print("Testing 'users' write...")
    res = db.users.find_one({'role': 'admin'})
    if res:
        print(f"Admin found: {res['email']}")
    else:
        print("Admin NOT found!")

    # 2. Test GridFS write
    print("Testing GridFS write...")
    fs = gridfs.GridFS(db)
    test_id = fs.put(b"test data", filename="test.txt")
    print(f"GridFS file created: {test_id}")
    
    # 3. Test image metadata write
    print("Testing 'images' metadata write...")
    img_res = db.images.insert_one({
        'filename': 'test.txt',
        'gridfs_id': test_id,
        'status': 'test'
    })
    print(f"Metadata inserted: {img_res.inserted_id}")
    
    # Cleanup
    db.images.delete_one({'_id': img_res.inserted_id})
    fs.delete(test_id)
    print("Cleanup successful.")
    
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
