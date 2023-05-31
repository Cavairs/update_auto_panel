import requests

url = "http://192.168.88.150/api/info"

payload = {}
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer roVerGKdIyMNLpAsF7UAK33XtaY0tmFAVquRzJvbSLWiKU7LcMCFmqBTpi7e0rz6'
}
params = {
    'username': 'admin',
    'password': '618cc4b2f29af196ab45e51b9880933f'
}

response = requests.request("GET", url, headers=headers, data=payload)

with open('test.json', 'w') as f:
    f.write(response.text)

print(response.text)
