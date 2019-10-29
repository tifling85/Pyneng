# -*- coding: utf-8 -*-
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''

from draw_network_graph import draw_topology
import yaml
from pprint import pprint

def transform_topology(file_yaml):
    res_dict = {}
    with open(file_yaml) as f:
        template = yaml.load(f)
    for dev, ports in template.items():
        for port, neigh in ports.items():
            for n_dev, n_port in neigh.items():
                if not res_dict.get((n_dev, n_port)):
                    res_dict[(dev, port)] = (n_dev, n_port)
    return res_dict


if __name__ == '__main__':
    dict_topol = transform_topology('to_yaml.yaml')
    draw_topology(dict_topol)




