import ipaddress
import os
import requests
import json
from datetime import datetime
  
net_prefix1 = '192.168.224.' 
net_prefix2 = '192.168.225.' 
net_prefix3 = '192.168.226.' 
net_prefix4 = '192.168.227.' 
net_prefix5 = '192.168.228.' 
 
 
devices = [] 
  
def scan_Ip(addr):  
    comm = f'ping -n 1 {addr}'  
    response_cmd = os.popen(comm).read()  
    url = f'http://{addr}/api/info' 
     
    try: 
        r = requests.get(url, timeout=1) 
        if 'TTL' in response_cmd: 
            info = r.json() 
            info['ip_adress'] = addr 
            key_remover = ('device_serial_number', 'commit', 'hybrid_enable' , 'device_type', 'frontend_version', 'commit_hash') 
            for k in key_remover: 
                info.pop(k, None) 
            if info['device_model'] == 'aa-07' or info['device_model'] =='aa07fbv' or info['device_model'] =='aa07bd':  # если устройство модели АА07 
                print(addr, ' --> Ping OK') 
                print(info) 
                devices.append(info) 
 
                with open('devices.json', 'w', encoding='utf-8') as f: 
                     result = { 
                     'count': len(devices), 
                     'devices': devices 
                                       } 
                     json.dump(result, f, ensure_ascii=False, indent=4) 
                     f.write('\n',) 
            else: 
                print(addr, ' --> Not found')          
    except: 
        pass 
  
  
net_prefix = '192.168.'  
net_list = [ f'{net_prefix}{i}.0/24' for i in range(224, 228) ] 
  
t1 = datetime.now()  
print('Scanning in progress...')  
 
 
 
for net in net_list:  
    for addr in ipaddress.ip_network(net).hosts():
        scan_Ip(str(addr))
  
t2 = datetime.now()  
total = t2 - t1  
  
print('Scanning completed in:', total) 
print("Devices found:", devices)