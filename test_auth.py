import requests

url = "http://localhost:8000/auth/register"
payload = {
    "email": "test@example.com",
    "password": "password123"
}
headers = {
    "Content-Type": "application/json"
}

print(f"Testing POST {url} with payload {payload}")
try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to server. Is it running?")
except Exception as e:
    print(f"Error: {e}")
