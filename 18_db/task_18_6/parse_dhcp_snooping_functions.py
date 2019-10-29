import sqlite3, re, datetime, os, yaml, tabulate

def change_status(conn):
    query = 'UPDATE dhcp SET active = 0'
    conn.execute(query)


def remove_old(conn):
    week_ago = datetime.datetime.today().replace(microsecond=0) - datetime.timedelta(days=7)
    query = 'DELETE from dhcp where last_active < ?'
    with conn:
        conn.execute(query, (week_ago, ))


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
                    res_lst.append((tmp[0], tmp[1], tmp[4], tmp[5], hostname, 1, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) )
    return res_lst


def create_db(db_name, schema_filename):
    if os.path.exists(db_name):
        print('DB is exist!')
        return False
    con = sqlite3.connect(db_name)
    print('Creating DB...')
    with open(schema_filename) as f:
        schema = f.read()
    con.executescript(schema)
    return True


def add_data_switches(db_file, cfg_filename):
    conn = sqlite3.connect(db_file)
    data_sw = get_data_sw(cfg_filename[0])
    query = 'INSERT into switches values (?,?)'
    for i in data_sw:
        try:
            with conn:
                conn.execute(query, i)
        except sqlite3.IntegrityError as e:
            print('When adding data {} error occured: {}'.format(i, e))
 

def add_data(db_file, cfg_filename):
    conn = sqlite3.connect(db_file)
    change_status(conn)
    data_dhcp = get_data_dhcp(cfg_filename)
    query = 'INSERT or REPLACE into dhcp values (?,?,?,?,?,?,?)'
    for i in data_dhcp:
        try:
            with conn:
                conn.execute(query, i)
        except sqlite3.IntegrityError as e:
            print('When adding data {} error occured: {}'.format(i, e))
    remove_old(conn)


def get_data(db_file, field, value):
    conn = sqlite3.connect(db_file)
    for act,mess in {1:'Active records: ', 0:'Inactive records :'}.items():
        query = 'SELECT * from dhcp where {} = ? and active = {}'.format(field,act)
        result = conn.execute(query,(value,)).fetchall()
        if result:
            print('{}'.format(mess))
            print(tabulate.tabulate(result, tablefmt = 'github'))


def get_all_data(db_file):
    conn = sqlite3.connect(db_file)   
    print('Info about devices: ')
    for act,mess in {1:'Active records: ', 0:'Inactive records :'}.items(): 
        query = 'SELECT * from dhcp where active = {}'.format(act)
        result = conn.execute(query).fetchall()
        if result:
            print('{}'.format(mess))
            print(tabulate.tabulate(result, tablefmt = 'github'))



