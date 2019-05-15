from cassandra.cluster import Cluster

keyspace = "blog"


def get_session():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()

    db = session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % keyspace)
    return session

def create_tables():
    session = get_session()
    session.set_keyspace(keyspace)
    session.execute("""
        CREATE COLUMNFAMILY IF NOT EXISTS users(
        username TEXT,
        password TEXT,
        display_name TEXT,
        PRIMARY KEY (username))""")

    session.execute("""
        CREATE COLUMNFAMILY IF NOT EXISTS blogdata(
        data_id INT,
        username TEXT,
        text TEXT,
        title TEXT,
        url TEXT,
        tag TEXT,
        comment TEXT,
        datatype TEXT,
        post_time TEXT,
        last_updated_time TEXT,
        PRIMARY KEY (datatype, data_id))""")
