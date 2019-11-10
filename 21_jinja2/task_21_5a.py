# -*- coding: utf-8 -*-
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''
import netmiko, yaml, pprint, os
from jinja2 import Environment, FileSystemLoader

def show_int_br(params):
    with netmiko.ConnectHandler(**params) as ssh:
        ssh.enable()
        return ssh.send_command('show ip interface brief | include Tunnel')

def create_cfg(src_template, dst_template, data):
    env = Environment(loader=FileSystemLoader(os.path.dirname(src_template)), trim_blocks=True, lstrip_blocks=True)
    temp1 = env.get_template(os.path.basename(src_template))
    temp2 = env.get_template(os.path.basename(dst_template))
    return (temp1.render(data), temp2.render(data))

def send_command(params, config):
    with netmiko.ConnectHandler(**params) as ssh:
        ssh.enable()
        return ssh.send_config_set(config)

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    src_tun = show_int_br(src_device_params)
    dst_tun = show_int_br(dst_device_params)
    tun_nums = []
    for line in (src_tun+'\n'+dst_tun).splitlines():
        if not (line.split()[0][6:]).isdigit() and line == []:
            continue
        tun_nums.append(int(line.split()[0][6:]))
    if not tun_nums:
        data['tum_nums'] = 0
    else:
        data['tun_num'] = max(tun_nums)+1
    configs = create_cfg(src_template, dst_template, vpn_data_dict)
    results = []
    results.append(send_command(src_device_params, configs[0]))
    results.append(send_command(dst_device_params, configs[1]))
    return results


data = {
    'tun_num': None,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}

with open('devices.yaml') as f:
    src_device_params, dst_device_params  = yaml.load(f, Loader = yaml.FullLoader)
src_template = os.path.abspath("templates/gre_ipsec_vpn_1.txt")
dst_template = os.path.abspath("templates/gre_ipsec_vpn_2.txt")
output_str = configure_vpn(src_device_params, dst_device_params, src_template, dst_template, data)
print(output_str)
