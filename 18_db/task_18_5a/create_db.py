import sqlite3, os


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


if __name__ == '__main__':
    db_name = 'dhcp_snooping.db'
    schema_filename = 'dhcp_snooping_schema.sql'
    create_db(db_name, schema_filename)

