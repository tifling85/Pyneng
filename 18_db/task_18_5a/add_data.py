import sqlite3, yaml, glob, sys, re
from datetime import timedelta, datetime

def con_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def get_data_sw(file_cnf):
    with open (file_cnf) as f:
        templates = yaml.load(f)
    return [(i,j) for i,j in templates['switches'].items()]


def get_data_dhcp(lst_files):
    res_lst = []
    regex = r'(sw\d+)_'
    for filek in lst_files:
        hostname = re.search(regex, filek).group(1)
        with open(filek) as f:
            for line in f:
                tmp = line.split()
                if tmp[0].startswith('00:'):
                    res_lst.append((tmp[0], tmp[1], tmp[4], tmp[5], hostname, 1, str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) )
    return res_lst


def add_data(conn, data_sw):
    change_status(conn)
    if len(data_sw[0]) == 7:
        query = 'INSERT or REPLACE into dhcp values (?,?,?,?,?,?,?)'
    else:
        query = 'INSERT into switches values (?,?)'
    for i in data_sw:
        try:
            with conn:
                conn.execute(query, i)
        except sqlite3.IntegrityError as e:
            print('When adding data {} error occured: {}'.format(i, e))
    remove_old(conn)

def change_status(conn):
    query = 'UPDATE dhcp SET active = 0'
    conn.execute(query)


def remove_old(conn):
    week_ago = datetime.today().replace(microsecond=0) - timedelta(days=7)
    query = 'DELETE from dhcp where last_active < ?'
    with conn:
        conn.execute(query, (week_ago, ))


if __name__ == '__main__':
    if sys.argv[1] == '1':
        lst_files = glob.glob('sw*_dhcp_snooping.txt')
    elif sys.argv[1] == '2':
        lst_files = glob.glob('new_data/sw*_dhcp_snooping.txt')
    file_cnf = 'switches.yml'
    db_name = 'dhcp_snooping.db'
    conn = con_to_db(db_name)
    add_data(conn, get_data_dhcp(lst_files))

