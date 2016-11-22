import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite')
DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


def add_collection(conn, c, list_name):
    """Adds collection to the db"""
    try:
        # creating the collections table
        c.execute('''CREATE TABLE {0}(DOCID TEXT, UNIQUE(DOCID));'''.format(list_name))
        conn.commit()
        return True
    except:
        return False


def connect(add_main=False):
    """Connects the db"""
    # connecting to the database
    # if database is not exist, it creates
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if add_main:
        add_collection(conn, c, 'MainCollection')
        # adding the main collection
        _add_docs_to_maincoll(conn, c)

    return conn, c


def get_collections(c):
    """Returns the exist collections"""
    c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    return c.fetchall()


def _add_docs_to_maincoll(conn, c):
    docs = [d for d in os.listdir(DOCS_PATH) if
            os.path.isdir(os.path.join(DOCS_PATH, d))]

    for doc in docs:
        c.execute('''INSERT OR IGNORE INTO MainCollection(DOCID) VALUES (?)''',
                  (doc,))
        conn.commit()


def add_doc_to_coll(conn, c, doc, coll):
    c.execute("SELECT * FROM {0} WHERE DOCID=?".format(coll), (doc,))
    data = c.fetchone()
    if data is None:
        c.execute('''INSERT OR IGNORE INTO {0}(DOCID) VALUES (?)'''.format(coll), (doc,))
        conn.commit()
        return True
    else:
        return False


def fetch_collection(c, coll):
    c.execute('''SELECT DOCID FROM {0}'''.format(coll))
    return c.fetchall()