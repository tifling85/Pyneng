# -*- coding: utf-8 -*-
'''
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
'''

import netmiko, yaml

def send_show_command(device, command):
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            return ssh.send_command(command)
    except netmiko.ssh_exception.NetMikoAuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e

if __name__ == '__main__':
    command = 'sh ip int br'
    with open('devices.yaml') as f:
        devices = yaml.load(f, Loader = yaml.FullLoader)
    for device in devices:
        print(send_show_command(device, command))
