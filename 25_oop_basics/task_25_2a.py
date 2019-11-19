# -*- coding: utf-8 -*-

'''
Задание 25.2a

Скопировать класс CiscoTelnet из задания 25.2 и изменить метод send_show_command добавив два параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после обработки с помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод
* templates - путь к каталогу с шаблонами



Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_25_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command('sh ip int br', parse=False)
Out[4]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

In [5]: r1.send_show_command('sh ip int br', parse=True)
Out[5]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '190.16.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.100',
  'address': '10.100.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.200',
  'address': '10.200.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.300',
  'address': '10.30.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback0',
  'address': '10.1.1.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback55',
  'address': '5.5.5.5',
  'status': 'up',
  'protocol': 'up'}]
'''

import telnetlib, textfsm, pprint
from textfsm import clitable

class CiscoTelnet():

        def __init__(self, ip, username, password, secret):
            self.telnet = telnetlib.Telnet(ip)
            self.telnet.read_until(b'Username')
            self.telnet.write(b'cisco\n')
            self.telnet.read_until(b'Password')
            self.telnet.write(b'cisco\n')
            self.telnet.read_until(b'>')
            self.telnet.write(b'enable\n')
            self.telnet.read_until(b'Password')
            self.telnet.write(b'cisco\n')
            self.telnet.read_until(b'#')

        def send_show_command(self, command, parse=False, templates='templates/'):
            if not parse:
                return self._write_line(command).decode('utf-8')
            command_output = self._write_line(command).decode('utf-8')
            cli_table = clitable.CliTable('index', templates)
            attributes_dict = {'Command':command}
            cli_table.ParseCmd(command_output, attributes_dict)
            res_lst =  [list(row) for row in cli_table]
            header_lst = list(cli_table.header)
            return [(dict(zip(header_lst, fsm_el))) for fsm_el in res_lst]
            #fsm = textfsm.TextFSM(open(templates))
            #fsm_lst = fsm.ParseText(command_output)
            #return [(dict(zip(fsm.header, fsm_el))) for fsm_el in fsm_lst]

        def _write_line(self, command):
            command_b = (command + '\n').encode('utf-8')
            self.telnet.write(command_b)
            return self.telnet.read_until(b'#')



if __name__ == '__main__':
    r1_params = {
                'ip': '192.168.100.1',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco'}
    r1 = CiscoTelnet(**r1_params)
    pprint.pprint(r1.send_show_command('show clock', parse = True))
