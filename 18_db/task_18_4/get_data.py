import sqlite3,sys
from tabulate import tabulate


def con_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def get_data_dhcp(conn, args):
    
    if len(args) == 3:
        query = 'SELECT * from dhcp where {} = ? and active = 1'.format(args[1])
        result = conn.execute(query,(args[2],)).fetchall()
        print('Info about devices with parameters: {} {}'.format(args[1], args[2]))
        query1 = 'SELECT * from dhcp where {} = ? and active = 0'.format(args[1])
        result1 = conn.execute(query1,(args[2],)).fetchall()
    else:
        query = 'SELECT * from dhcp where active = 1'
        result = conn.execute(query).fetchall()
        print('Info about devices: ')
        query1 = 'SELECT * from dhcp where active = 0'
        result1 = conn.execute(query1).fetchall()

    if result:
        print('Active records: ')
        print(tabulate(result, tablefmt = 'github'))
    if result1:
        print('Inactive records: ')
        print(tabulate(result1, tablefmt = 'github'))


if __name__ == '__main__':
    db_name = 'dhcp_snooping.db'
    args = ['mac', 'ip', 'vlan', 'interface', 'switch']

    if len(sys.argv) in [1,3]:
        if len(sys.argv) == 1:
            get_data_dhcp(con_to_db(db_name), sys.argv)
        elif sys.argv[1] in args:
            get_data_dhcp(con_to_db(db_name), sys.argv)
        else:
            print('That argument not support. Please, use mac, ip, vlan, interface, switch')
    else:
        print('Input 0 or 2 arguments, pls')



    
