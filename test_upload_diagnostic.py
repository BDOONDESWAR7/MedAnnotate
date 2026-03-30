import requests
import io

def test_upload():
    # 1. Login as company
    login_res = requests.post('http://localhost:5000/api/auth/login', json={
        'email': 'syntaxsociety@gmail.com',
        'password': '123456'
    })
    
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return

    token = login_res.json().get('token')
    headers = {'Authorization': f'Bearer {token}'}

    # 2. Try upload
    files = {'file': ('test_xray.jpg', b'dummy_bytes_for_image_test_123', 'image/jpeg')}
    data = {'department': 'Radiology', 'batch_name': 'Test-Restart'}
    
    res = requests.post('http://localhost:5000/api/images/upload', headers=headers, files=files, data=data)
    
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

if __name__ == '__main__':
    test_upload()
