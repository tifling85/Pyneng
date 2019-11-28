# -*- coding: utf-8 -*-

'''
Задание 27.2c

Проверить, что метод send_command класса MyNetmiko из задания 27.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_27_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

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
    print(r1.send_command('sh ip int br', strip_command=False))
    print(r1.send_command('sh ip int br', strip_command=True))
