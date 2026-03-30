from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
from bson import ObjectId

def verify_eswar():
    load_dotenv()
    uri = os.environ.get('MONGO_URI')
    if not uri: return
    
    try:
        client = MongoClient(uri, tlsCAFile=certifi.where())
        db = client.get_default_database()
        
        # 1. Find ESWAR
        eswar = db.users.find_one({'name': {'$regex': '^eswar$', '$options': 'i'}})
        if not eswar:
            print("Error: ESWAR doctor not found")
            return
            
        # 2. Update to verified + specialty
        res = db.users.update_one(
            {'_id': eswar['_id']},
            {'$set': {
                'verified': True,
                'specialty': 'Radiology',
                'active': True
            }}
        )
        if res.modified_count > 0:
            print(f"Successfully verified {eswar['name']} and set specialty to Radiology")
        else:
            print(f"ESWAR was already verified or no changes made.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    verify_eswar()
