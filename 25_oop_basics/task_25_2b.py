# -*- coding: utf-8 -*-

'''
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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

        def send_config_command(self, commands):
            str_answ = ''
            self.telnet.write(b'conf t\n')
            str_answ += self.telnet.read_until(b'#').decode('utf-8')
            if type(commands) == str:
                commands = commands.split('\n')
            for comm in commands:
                str_answ += self.send_show_command(comm)
            self.telnet.write(b'exit\n')
            self.telnet.read_until(b'#')
            return str_answ

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
    commands = ['interface loop55', 'ip address 5.5.5.5 255.255.255.255']
    r1 = CiscoTelnet(**r1_params)
    #pprint.pprint(r1.send_show_command('show clock', parse = True))
    print(r1.send_config_command(commands))

