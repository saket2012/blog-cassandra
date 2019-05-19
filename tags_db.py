import datetime
import time

from db_connection import get_session

keyspace = 'blog'


def post_tag(data_id, username, tag_name, url):
    session = get_session()
    session.set_keyspace(keyspace)
    data_type = "T"
    unix = int(time.time())
    post_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    last_updated_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    session.execute("""INSERT INTO blogdata (data_id, datatype, username, url, tag, post_time, last_updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
            int(data_id), data_type, username, url, tag_name, post_time, last_updated_time))


def get_tag_details(url):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * FROM blogdata WHERE url = %s and datatype = %s ALLOW FILTERING""", (url, 'T'))
    if rows:
        return True
    return False


def get_article_by_id(id):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * FROM blogdata WHERE data_id = %s AND datatype = %s ALLOW FILTERING""", (int(id), 'A'))
    if rows:
        return rows
    return False


def delete_tag(url):
    session = get_session()
    session.set_keyspace(keyspace)
    session.execute("""DELETE FROM blogdata WHERE url = %s AND datatype = %s ALLOW FILTERING""", (url, 'T'))


def get_tag_by_url(url):
    conn = get_db_tags()
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM tags where url = ?""", (url,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        return rows
    except Exception as e:
        return e


def get_tag_by_tag_name(tag_name):
    conn = get_db_tags()
    c = conn.cursor()
    try:
        c.execute("""SELECT tag_name, url FROM tags where tag_name = ?""", (tag_name,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        row_headers = [x[0] for x in c.description]
        tags = []
        for tag in rows:
            tags.append(dict(zip(row_headers, tag)))
        return tags
    except Exception as e:
        return e


def get_tags_by_url(url):
    conn = get_db_tags()
    c = conn.cursor()
    try:
        c.execute("""SELECT tag_name, url FROM tags where url = ?""", (url,))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        row_headers = [x[0] for x in c.description]
        tags = []
        for tag in rows:
            tags.append(dict(zip(row_headers, tag)))
        return tags
    except Exception as e:
        return e


def get_tags_metadata(n):
    conn = get_db_tags()
    c = conn.cursor()

    c.execute(
        """SELECT tag, title, url  FROM tags ORDER BY post_time LIMIT ?""", (n,))
    row_headers = [x[0] for x in c.description]
    rows = c.fetchall()
    tags = []

    for tag in rows:
        tags.append(dict(zip(row_headers, tag)))
    return tags
