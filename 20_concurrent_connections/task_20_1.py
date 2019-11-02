# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''

from concurrent.futures import ThreadPoolExecutor
import subprocess, logging

logging.basicConfig(format = '%(threadName)s %(levelname)s: %(message)s',level=logging.INFO)


def ping_ip_address(ip):
    logging.info(f'Checking {ip}...')
    return subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def ping_ip_addresses(ip_list, limit=3):
    res_tuple = ([],[])
    avail, notavail = res_tuple
    with ThreadPoolExecutor(max_workers = limit) as executor:
        res_iter = executor.map(ping_ip_address, ip_list)
    for res in res_iter:
        if res.returncode == 0:
            avail.append(res.args[3])
        else:
            notavail.append(res.args[3])
    return res_tuple

if __name__ == '__main__':
    ip_list = ['8.8.8.8', '233.8.8.8','192.168.100.2','192.168.100.4']
    print(ping_ip_addresses(ip_list))


