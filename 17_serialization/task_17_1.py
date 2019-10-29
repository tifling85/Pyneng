# -*- coding: utf-8 -*-
'''
Задание 17.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
'''

import glob, re, csv

data_filenames = glob.glob('sh_vers*')
#print(sh_version_files)

headers = ['hostname', 'ios', 'image', 'uptime']


def parse_sh_version(sh_version):
    res_tuple = ()
    regex = r'Cisco IOS .+? Version (?P<ios>\S+?),.+router uptime is (?P<uptime>.+? minutes).+System image file is "(?P<image>\S+)"' 
    matches = re.match(regex, sh_version, re.DOTALL)
    return matches.group('ios'), matches.group('image'), matches.group('uptime')


def write_inventory_to_csv(data_filenames, csv_filename):
    res_lst = []
    res_lst.append(headers)
    regname = r'_(\S+)\.'
    for filen in data_filenames:
        hostname = re.search(regname, filen).group()
        with open(filen) as f:
            res_lst.append(list(parse_sh_version(f.read())))
    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        for data in res_lst:
            writer.writerow(data)


if __name__ == '__main__':
    write_inventory_to_csv(data_filenames, 'csv_out.csv')


