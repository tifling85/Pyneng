# -*- coding: utf-8 -*-

'''
Задание 27.2b

Дополнить класс MyNetmiko из задания 27.2a.

Переписать метод send_config_set netmiko, добавив в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_27_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

'''
from netmiko.cisco.cisco_ios import CiscoIosBase 

class ErrorInCommand(Exception):
    pass

class MyNetmiko(CiscoIosBase):

    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()
    
    def _check_error_in_command(self, command, result):
        errors = ['Invalid input detected at \'^\' marker', 'Incomplete command', 'Ambiguous command']
        for er in errors:
            if er in result:
                raise ErrorInCommand(f'Command "{command}" on {self.ip} except error {er}')
        return result

    def send_command(self, command):
        result = super().send_command(command)
        return self._check_error_in_command(command, result)
    
    def send_config_set(self, commands, **kwargs):
        if isinstance(commands, str):
            commands = [commands]
        output = ''
        for command in commands:
            result = super().send_config_set(command, **kwargs)
            self._check_error_in_command(command, result)
            output += result
        return output


if __name__ == '__main__':
    device_params = {
        'device_type': 'cisco_ios',
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
    }
    r1 = MyNetmiko(**device_params)
    print(r1.send_config_set(['sh ip int br', 'int loopback 33']))


