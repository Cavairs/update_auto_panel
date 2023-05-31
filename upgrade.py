import requests
import json
from pprint import pprint
import zipfile

# login = tokens(ip)

def tokens (ip):
        ip = device['ip_adress']
        url = f'http://{ip}/api/v1/login'
        payload={}
        params = {'username': 'admin',
                  'password': 'e10adc3949ba59abbe56e057f20f883e' }
        response = requests.request("GET", url, params=params, data=payload)
        get_token = response.json()
        token =(get_token['token'])
        return token

# def backup (ip)



with open('devices_single_subnet.json', 'r', encoding='utf-8') as f:
       data = json.load(f)
       for device in data["devices"]:
         if device['device_model'] == "aa07mf":
               curent_ip = device['ip_adress']
               login = tokens(device['ip_adress'])
               url = f"http://{curent_ip}/api/v1/system/settings/tables"
               payload={}
               headers = {
               'Accept': 'application/json',
               'Authorization': f'Bearer {login}'}
               response = requests.request("GET", url, headers=headers, data=payload)
               with open(f"{device['ip_adress']}_backup.zip", 'wb') as f:  
                   f.write(response.content)


                     

               
        

              



           
              


              
       
              
