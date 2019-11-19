# -*- coding: utf-8 -*-

'''
Задание 25.2c

Скопировать класс CiscoTelnet из задания 25.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_25_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "i" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "i"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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

        def send_config_command(self, commands, strict = False):
            list_errors = ["Invalid input detected at '^' marker","Incomplete command" ]
            str_answ, err_answ = '', ''
            self.telnet.write(b'conf t\n')
            str_answ += self.telnet.read_until(b'#').decode('utf-8')
            if type(commands) == str:
                commands = commands.split('\n')
            for comm in commands:
                answ = self.send_show_command(comm)
                for err in list_errors:
                    if err in answ:
                        if strict:
                            raise ValueError(f'при выполнении команды {comm} на устройстве 192.168.100.1 возникла ошибка -> {err}\n')
                        err_answ += f'при выполнении команды {comm} на устройстве 192.168.100.1 возникла ошибка -> {err}\n'
                str_answ += answ
            self.telnet.write(b'exit\n')
            self.telnet.read_until(b'#')
            return err_answ + str_answ

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
    commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors+correct_commands
    #commands = ['interface loop55', 'ip address 5.5.5.5 255.255.255.255']
    r1 = CiscoTelnet(**r1_params)
    #pprint.pprint(r1.send_show_command('show clock', parse = True))
    print(r1.send_config_command(commands, strict = True))

