import nmap
import json
from datetime import datetime


nmap_scanner = nmap.PortScanner()
net_prefix = '192.168.'
net_list = [f'{net_prefix}{i}.0/24' for i in range(224, 233)]

devices = []


def scan_Ip(addr):
    try:
        results = nmap_scanner.scan(addr, arguments='-sS -p 80 -Pn')
        if 'tcp' in results['scan'][addr]:
            state = results['scan'][addr]['tcp'][80]['state']
            if state == 'open':
                info = {}
                info['ip_adress'] = addr
                for k in results['scan'][addr]['tcp'][80]:
                    info[k] = results['scan'][addr]['tcp'][80][k]
                key_remover = ('product', 'name', 'cpe',
                               'version', 'extrainfo')
                for k in key_remover:
                    info.pop(k, None)
                if info['name'] == 'http':
                    print(addr, ' --> HTTP Server Found')
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
                    print(addr, ' --> Open Port, but Not HTTP')

            else:
                print(addr, ' --> Port 80 is Closed')
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


t1 = datetime.now()
print('Scanning in progress...')

for net in net_list:
    hosts = nmap_scanner.rangehosts(net)
    for addr in hosts:
        scan_Ip(addr)

t2 = datetime.now()
total = t2 - t1

print('Scanning completed in:', total)
