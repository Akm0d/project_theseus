import sqlite3
from pathlib import Path

def init():
    debug = True
    db_path = Path("attempts.db")
    if not db_path.is_file(): #if does not exist, format / create tables
        if debug: print("database does not exist, creating / formatting")
        conn = sqlite3.connect("attempts.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE devices (
                     uuid int NOT NULL,
                     name varchar NOT NULL,
                     time varchar NOT NULL,
                     attempt_count NOT NULL,
                     PRIMARY KEY (uuid))''')
        conn.commit()
        conn.close()
def insert(record): #one record at a time please :)
    conn = sqlite3.connect("attempts.db")
    c = conn.cursor()
    c.execute("REPLACE INTO devices VALUES (?,?,?,?)", record)
    conn.commit()
    conn.close
