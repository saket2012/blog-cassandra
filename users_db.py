from db_connection import get_session
import hashlib
from passlib.hash import sha256_crypt

keyspace = 'blog'

def create_user(username, password, display_name):
    hash_password = encode_password(password)
    session = get_session()
    session.set_keyspace(keyspace)

    session.execute("""INSERT INTO users (username, password, display_name) VALUES (%s, %s, %s)""", (
        username, hash_password, display_name))


def update_password(username, new_password):
    hash_password = encode_password(new_password)
    session = get_session()
    session.set_keyspace(keyspace)
    session.execute("""UPDATE users SET password = %s WHERE username = %s""", (
        hash_password, username))


def delete_user(username):
    session = get_session()
    session.set_keyspace(keyspace)
    session.execute("""DELETE FROM users WHERE username = %s""", (username,))


def get_user_details(username):
    session = get_session()
    session.set_keyspace(keyspace)
    rows = session.execute("""SELECT * FROM users WHERE username = %s""", (username,))
    if rows:
        return rows
    return False


def encode_password(password):
    hash_password = sha256_crypt.encrypt(password)
    return hash_password
