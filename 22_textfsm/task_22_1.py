# -*- coding: utf-8 -*-
'''
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

'''
import textfsm, pprint

def parse_command_output(template, command_output):
    fsm = textfsm.TextFSM(open(template))
    return fsm.ParseText(command_output) 

if __name__ == '__main__':
    with open('output/sh_ip_int_br.txt') as f:
        command_output = f.read()
    result = parse_command_output('templates/sh_ip_int_br.template', command_output)
    pprint.pprint(result)