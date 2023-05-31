import ipaddress
import os
import requests
import json
from datetime import datetime
import threading


net_prefix = '192.168.'
net_list = [f'{net_prefix}{i}.0/24' for i in range(224, 233)]

devices = []
lock = threading.RLock()  # объект блокировки


def scan_Ip(addr):
    comm = f'ping -n 3 {addr}'
    response_cmd = os.popen(comm).read()
    url = f'http://{addr}/api/info'
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    try:
        r = requests.request("GET", url, headers=headers,
                             data=payload, timeout=5)

        if 'TTL' in response_cmd and r.status_code == 200:
            info = r.json()
            info['ip_adress'] = addr
            key_remover = ('device_serial_number', 'commit', 'hybrid_enable',
                           'device_type', 'frontend_version', 'commit_hash')
            for k in key_remover:
                info.pop(k, None)
            # если устройство модели АА07
            if info['device_model'] == 'aa-07' or info['device_model'] == 'aa07fbv' or info['device_model'] == 'aa07bd' or info['device_model'] == 'aa07fb2m' or info['device_model'] == 'aa07':
                print(addr, ' --> Ping OK')
                print(info)
                with lock:
                    # получение блокировки и изменение общего ресурса devices
                    devices.append(info)

                with open('devices.json', 'w', encoding='utf-8') as f:
                    with lock:
                        result = {
                            'count': len(devices),
                            'devices': devices
                        }
                        json.dump(result, f, ensure_ascii=False, indent=4)
                        f.write('\n',)
        else:
            print(addr, ' --> Ping FAILED')
    except requests.exceptions.Timeout:
        print(f"Timeout при обращении к {url}")
    except requests.exceptions.ConnectionError:
        print(
            f"Ошибка соединения при обращении к {url}")
    except json.JSONDecodeError as e:
        print(
            f"Ошибка декодирования JSON при обращении к {url}")
        print(f"Response text: {r.text}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


t1 = datetime.now()
print('Scanning in progress...')
threads_list = []

for net in net_list:
    for addr in ipaddress.ip_network(net).hosts():
        thread = threading.Thread(target=scan_Ip, args=(str(addr),))
        threads_list.append(thread)
        thread.start()

for thread in threads_list:
    thread.join()

t2 = datetime.now()
total = t2 - t1


print('Scanning completed in:', total)
