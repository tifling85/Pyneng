import sqlite3, yaml, glob


def con_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def get_data_sw(file_cnf):
    with open (file_cnf) as f:
        templates = yaml.load(f)
    return [(i,j) for i,j in templates['switches'].items()]


def get_data_dhcp(lst_files):
    res_lst = []
    for filek in lst_files:
        hostname = filek.split('_')[0]
        with open(filek) as f:
            for line in f:
                tmp = line.split()
                if tmp[0].startswith('00:'):
                    res_lst.append((tmp[0], tmp[1], tmp[4], tmp[5], hostname))
    return res_lst


def add_data(conn, data_sw):
    if len(data_sw[0]) == 5:
        query = 'INSERT into dhcp values (?,?,?,?,?)'
    else:
        query = 'INSERT into switches values (?,?)'
    for i in data_sw:
        try:
            with conn:
                conn.execute(query, i)
        except sqlite3.IntegrityError as e:
            print('When adding data {} error occured: {}'.format(i, e))


if __name__ == '__main__':
    lst_files = glob.glob('sw*')
    file_cnf = 'switches.yml'
    db_name = 'dhcp_snooping.db'
    conn = con_to_db(db_name)
    add_data(conn, get_data_sw(file_cnf))
    add_data(conn, get_data_dhcp(lst_files))

