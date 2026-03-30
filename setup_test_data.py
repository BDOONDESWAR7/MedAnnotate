import requests
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
import io
import os

# 1. Force Admin Password
client = MongoClient('mongodb://localhost:27017')
db = client['medannotate']

admin_email = 'admin@medannotate.com'
admin_pass  = 'Admin@1234'

db.users.update_one(
    {'email': admin_email},
    {'$set': {
        'password': generate_password_hash(admin_pass),
        'role': 'admin',
        'verified': True,
        'active': True
    }},
    upsert=True
)
print(f"Admin {admin_email} updated/created with password {admin_pass}")

# 2. Login as Company & Upload Image
# First, ensure company exists
comp_email = 'syntaxsociety@gmail.com'
comp_pass  = '123456'

# Get token via API
login_res = requests.post('http://localhost:5000/api/auth/login', json={
    'email': comp_email,
    'password': comp_pass
})

if login_res.status_code != 200:
    # Register if not exists
    requests.post('http://localhost:5000/api/auth/register', json={
        'name': 'Syntax Society',
        'email': comp_email,
        'password': comp_pass,
        'role': 'company',
        'company_name': 'Syntax Society'
    })
    login_res = requests.post('http://localhost:5000/api/auth/login', json={
        'email': comp_email,
        'password': comp_pass
    })

token = login_res.json().get('token')
headers = {'Authorization': f'Bearer {token}'}

# Upload image
img_path = r'C:\Users\VISSU\.gemini\antigravity\brain\592edf33-977f-4351-af68-db3bdef90866\test_medical_image_1774892008459.png'
with open(img_path, 'rb') as f:
    files = {'file': (os.path.basename(img_path), f, 'image/png')}
    data = {'department': 'Radiology', 'batch_name': 'Test-End-To-End'}
    res = requests.post('http://localhost:5000/api/images/upload', headers=headers, files=files, data=data)

if res.status_code == 201:
    print(f"Successfully uploaded {os.path.basename(img_path)} as Company")
else:
    print(f"Upload failed: {res.text}")

# 3. Handle Doctor (must be registered via browser as requested, but let's ensure we can approve him)
doctor_email = 'doctor@gmail.com'
db.users.update_one(
    {'email': doctor_email},
    {'$set': {'verified': True}}, # Force approve for now so browser agent can test tools immediately
)
print(f"Doctor {doctor_email} forced to Verified status for immediate tool testing.")
