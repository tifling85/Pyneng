# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''
from jinja2 import Environment, FileSystemLoader
import os, yaml, pprint

def generate_config(template, data_dict):
    pprint.pprint(data_dict )
    print('\n'*2)
    env = Environment(loader=FileSystemLoader(os.path.dirname(template)), trim_blocks=True, lstrip_blocks=True)
    temp = env.get_template(os.path.basename(template))
    return temp.render(data_dict)
    
if __name__ == '__main__':
    template = os.path.abspath("templates/for.txt")
    with open('data_files/for.yml') as f:
        data_dict = yaml.load(f)
    str_conf = generate_config(template, data_dict)
    print(str_conf)
