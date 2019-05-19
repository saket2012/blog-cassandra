import datetime
import time

from db_connection import get_session

keyspace = 'blog'

def post_article(data_id, username, text, title, url):
    session = get_session()
    session.set_keyspace(keyspace)
    unix = int(time.time())
    data_type = "A"
    post_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    last_updated_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    session.execute("""INSERT INTO blogdata (data_id, username, text, title, url, datatype, post_time, last_updated_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (data_id, username, text, title, url, data_type, post_time, last_updated_time))


def get_data_id():
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT MAX(data_id) AS id FROM blogdata""")
    for row in rows:
        id = row.id
    return id

def get_article_details(username, id):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * FROM blogdata where username = %s AND data_id = %s ALLOW FILTERING""",
        (username, int(id)))
    if rows:
        return True
    return False


def get_article_by_id(id):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * FROM blogdata where data_id = %s AND datatype = %s ALLOW FILTERING""", (int(id), 'A'))
    if rows:
        return rows
    return False

#
# def get_article_by_url(url):
#     conn = get_db_articles()
#     c = conn.cursor()
#     try:
#         c.execute("""SELECT * FROM articles where url = ?""", (url,))
#         rows = c.fetchall()
#         if len(rows) == 0:
#             return False
#         return rows
#     except Exception as e:
#         return e
#
#
def edit_article(title, text, id):
    session = get_session()
    session.set_keyspace(keyspace)
    unix = int(time.time())
    data_type = "A"
    last_updated_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    session.execute("""UPDATE blogdata SET title = %s, text = %s, last_updated_time = %s WHERE data_id = %s AND datatype = %s""",
                  (title, text, last_updated_time, int(id), data_type))



def delete_article(id):
    session = get_session()
    session.set_keyspace(keyspace)
    data_type = "A"
    session.execute("""DELETE FROM blogdata WHERE data_id = %s AND datatype = %s""", (int(id), data_type))


# def get_article(title):
#     conn = get_db_articles()
#     c = conn.cursor()
#     try:
#         c.execute("""SELECT * FROM articles WHERE title = ? ORDER BY post_time desc""", (title,))
#         rows = c.fetchall()
#         if len(rows) == 0:
#             return False
#         return rows
#     except Exception as e:
#         return e
#
#
def get_n_articles(n):
    session = get_session()
    session.set_keyspace(keyspace)
    data_type = "A"
    rows = session.execute("""SELECT text, username, title, url, post_time, last_updated_time FROM blogdata \
        WHERE datatype = %s ORDER BY data_id DESC LIMIT %s""", (data_type, int(n)))
    if rows:
        return rows
    return False


def get_articles_metadata(n):
    session = get_session()
    session.set_keyspace(keyspace)
    data_type = "A"
    rows = session.execute("""SELECT username, title, text, url, post_time FROM blogdata \
        WHERE datatype = %s ORDER BY data_id DESC LIMIT %s""", (data_type, int(n)))
    if rows:
        return rows
    return False
