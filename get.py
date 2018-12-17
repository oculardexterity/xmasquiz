import requests

first_response = requests.get('http://localhost:5000/return-to-sender-really-quickly')
print(first_response.text)
second_response = requests.get('http://localhost:5000/return-to-sender-really-quickly/?answer='+first_response.text)
print(second_response.text)