# -*- coding: utf-8 -*-

'''
Задание 27.2d

Дополнить класс MyNetmiko из задания 27.2c или задания 27.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.

Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_27_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_command(self, command, **kwargs):
        result = super().send_command(command, **kwargs)
        return self._check_error_in_command(command, result)
    
    def send_config_set(self, commands, ignore_errors=True, **kwargs):
        if isinstance(commands, str):
            commands = [commands]
        output = ''
        for command in commands:
            result = super().send_config_set(command, **kwargs)
            if not ignore_errors:
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
    print(r1.send_config_set('lo', ignore_errors=True))

