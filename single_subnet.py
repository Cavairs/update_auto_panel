import os
import platform
import threading
import socket
from datetime import datetime
import requests
import json

devices = []


def getMyIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def scan_Ip(ip):
    addr = net + str(ip)
    comm = ping_com + addr
    response_cmd = os.popen(comm).read()
    url = 'http://' + addr + '/api/info'

    try:
        r = requests.get(url, timeout=1)
        if 'TTL' in response_cmd:
            info = r.json()
            info['ip_adress'] = addr
            key_remover = ('device_serial_number', 'commit', 'hybrid_enable',
                           'device_type', 'frontend_version', 'commit_hash')
            for k in key_remover:
                info.pop(k, None)
            # если устройство модели АА07
            if info['device_model'] == 'aa-07' or info['device_model'] == 'aa07fbv' or info['device_model'] == 'aa07bd' or info['device_model'] == 'aa07fb2m' or info['device_model'] == 'aa07':
                print(addr, '--> Ping OK')
                print(info)
                devices.append(info)

                with open('devices.json', 'a', encoding='utf-8') as f:
                    result = {
                        'count': len(devices),
                        'devices': devices
                    }
                    json.dump(result, f, ensure_ascii=False, indent=4)
                    f.write('\n',)
    except:
        pass


net = getMyIp()
print('Твой IP:', net)
net_split = net.split('.')
a = '.'
ip_f = int(input('Подсеть: '))
net = net_split[0] + a + net_split[1] + a + str(ip_f) + a
print(net)
ip_pool = range(1, 255)

oc = platform.system()
if (oc == 'Windows'):
    ping_com = 'ping -n 5 '
else:
    ping_com = 'ping -c 1 '

t1 = datetime.now()
print('Scanning in progress...')

for ip in ip_pool:
    if ip == int(net_split[3]):
        continue  # исключаем IP адреса Бас системы из сканирования
    potoc = threading.Thread(target=scan_Ip, args=(ip,))
    # time.sleep(3)
    potoc.start()

potoc.join()
t2 = datetime.now()
total = t2 - t1

print('Scanning completed in:', total)
