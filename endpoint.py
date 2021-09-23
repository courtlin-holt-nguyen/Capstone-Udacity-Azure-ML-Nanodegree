import requests
import json

# URL for the web service, should be similar to:
# 'http://8530a665-66f3-49c8-a953-b82a2d312917.eastus.azurecontainer.io/score'
scoring_uri = "http://f515466b-999c-4e85-87d7-89a671163cb9.eastus2.azurecontainer.io/score"

# If the service is authenticated, set the key or token
key = "I7ZPDaYLEdGhsjFA3Mu3yk698fjizohD"

# Two sets of data to score, so we get two results back
data = {
    "data": [
        {
        "gender":"Male",
        "age":67.0,
        "hypertension":0,
        "heart_disease":1,
        "ever_married":True,
        "work_type":"Private",
        "Residence_type":"Urban",
        "avg_glucose_level":228.69,
        "bmi":36.6,
        "smoking_status":"formerly smoked"
        }
    ]
}
# Convert to JSON string
input_data = json.dumps(data)
with open("data.json", "w") as _f:
    _f.write(input_data)

# Set the content type
headers = {"Content-Type": "application/json"}
# If authentication is enabled, set the authorization header
headers["Authorization"] = f"Bearer {key}"

# Make the request and display the response
resp = requests.post(scoring_uri, input_data, headers=headers)
print(resp.json())
