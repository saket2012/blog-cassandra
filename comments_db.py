import datetime
import time
from db_connection import get_session

keyspace = 'blog'


def get_data_id():
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT MAX(data_id) AS id FROM blogdata""")
    for row in rows:
        id = row.id
    return id


def get_article_id(id):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * FROM blogdata where data_id = %s and datatype = %s""",(int(id), 'A'))
    if rows:
        return True
    return False


def post_comment(data_id, username, comment):
    session = get_session()
    session.set_keyspace(keyspace)
    unix = int(time.time())
    datatype = 'C'
    post_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    last_updated_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    session.execute("""INSERT INTO blogdata (data_id, username, comment, datatype, post_time, last_updated_time) VALUES (%s, %s, %s, %s, %s, %s)""", (
        int(data_id), username, comment, datatype, post_time, last_updated_time))


def count_comments(id):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT COUNT(*) from blogdata WHERE data_id = %s and datatype = %s""", (int(id), 'C'))
    n_comments = rows[0]
    return n_comments


def get_comments(id, no_of_comments):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * from blogdata where data_id = %s AND datatype = %s LIMIT %s""", (
        int(id), 'C', int(no_of_comments)))
    if rows:
        return rows
    return False

def get_comment(id):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT data_id as id FROM blogdata WHERE data_id = %s AND datatype = %s""", (int(id), 'C'))
    for row in rows:
        id = row.id
    return id

def delete_comment(id, username):
    session = get_session()
    session.set_keyspace(keyspace)
    session.execute("""DELETE FROM blogdata WHERE data_id = %s AND datatype = %s""", (int(id), 'C'))
