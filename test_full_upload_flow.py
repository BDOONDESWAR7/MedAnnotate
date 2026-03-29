import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000/api"

def test_flow():
    print(f"Testing production API at {BASE_URL}...")
    
    # 1. Register a company
    email = f"test_comp_{int(time.time())}@test.com"
    print(f"Registering {email}...")
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "Password123!",
        "name": "Test Company",
        "role": "company",
        "company_name": "Test Labs"
    })
    
    if reg_res.status_code != 201:
        print(f"Registration FAILED: {reg_res.status_code} {reg_res.text}")
        return

    data = reg_res.json()
    token = data.get('token')
    print("Registration SUCCESS.")

    # 2. Upload an image
    print("Uploading image...")
    with open("c:/Users/VISSU/OneDrive/Pictures/Doondi/medical/medical/frontend/assets/sample_scan.png", "rb") as f:
        files = {"file": ("test.png", f, "image/png")}
        headers = {"Authorization": f"Bearer {token}"}
        up_res = requests.post(f"{BASE_URL}/images/upload", files=files, data={"department": "Radiology", "batch_name": "Test Batch"}, headers=headers)
    
    if up_res.status_code != 201:
        print(f"Upload FAILED: {up_res.status_code} {up_res.text}")
    else:
        print(f"Upload SUCCESS: {up_res.json()}")

if __name__ == "__main__":
    # Ensure app.py is running in background before this (simulated)
    # But for now, we just test the logic by trying to hit it.
    try:
        test_flow()
    except Exception as e:
        print(f"Error connecting: {e}")
