import requests

url = "http://3.110.124.223:8000/recommend"
data = {"query": "Need a test for customer service and communication"}
response = requests.post(url, json=data)

print(response.json())
