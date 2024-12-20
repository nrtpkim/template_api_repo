from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests


# Path to your service account JSON file
service_account_file = 'cpf-aiml-cv-dc196caa1a60.json'

# Load the service account credentials
credentials = service_account.IDTokenCredentials.from_service_account_file(
    service_account_file,
    target_audience="https://kim-test-api-service-560622642415.asia-southeast1.run.app"  # Replace with your Cloud Run service URL
)

# Refresh the credentials to get a valid identity token
auth_request = Request()
credentials.refresh(auth_request)

# Print the Identity Token
identity_token = credentials.token
print(f"Identity Token: {identity_token}")







import requests

# Cloud Run service URL
cloud_run_url = "https://kim-test-api-service-560622642415.asia-southeast1.run.app/api-key-auth?val_1=123&val_2=456"

# Set Authorization header with the identity token
headers = {
    "Authorization": f"Bearer {identity_token}",
    "fromApp" : "AXONS-MOVE"
}

# Make the POST request to Cloud Run
response = requests.get(cloud_run_url, headers=headers)

# Check the response
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")