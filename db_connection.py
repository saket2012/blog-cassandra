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
        CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT,
        display_name TEXT,
        PRIMARY KEY (username))""")

    session.execute("""
        CREATE TABLE IF NOT EXISTS articles(
        username text,
        text text,
        author text,
        title text,
        url text,
        post_time text,
        last_updated_time text,
        PRIMARY KEY (url))""")
