import requests

token = "user"  # Replace with your actual token

headers = {"Authorization": f"Bearer {token}"}
url = "http://0.0.0.0:7001/protected"  # Replace with your actual API endpoint

response = requests.get(url, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        print("Access granted:", data)
    except ValueError:
        print("Response is not in JSON format")
else:
    print("Access denied:", response.status_code, response.text)