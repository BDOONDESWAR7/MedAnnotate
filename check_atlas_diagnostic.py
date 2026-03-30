from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

def check():
    load_dotenv()
    uri = os.environ.get('MONGO_URI')
    if not uri: 
        print("Error: No MONGO_URI in .env")
        return
    
    try:
        client = MongoClient(uri, tlsCAFile=certifi.where())
        db = client.get_default_database()
        ping = db.command('ping')
        print(f"Connection: OK (Ping: {ping})")
        
        count = db.images.count_documents({})
        print(f"Total images: {count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check()
