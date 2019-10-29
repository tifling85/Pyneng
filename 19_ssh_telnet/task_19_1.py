# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''
import netmiko, yaml

def send_show_command(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        return ssh.send_command(command)

if __name__ == '__main__':
    command = 'sh ip int br'
    with open('devices.yaml') as f:
        devices = yaml.load(f, Loader = yaml.FullLoader)
    for device in devices:
        print(send_show_command(device, command))

