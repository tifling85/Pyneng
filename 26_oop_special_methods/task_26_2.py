# -*- coding: utf-8 -*-

'''
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
'''

import telnetlib, textfsm, pprint
import clitable

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
            
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.telnet.close()


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
    #r1 = CiscoTelnet(**r1_params)
    #pprint.pprint(r1.send_show_command('show clock', parse = True))
    #print(r1.send_config_command(commands, strict = True))

    with CiscoTelnet(**r1_params) as r1:
        print(r1.send_show_command('sh clock'))
        raise ValueError('Возникла ошибка')
