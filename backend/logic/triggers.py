import os
import sqlite3

# Definir la ruta a la base de datos
PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'backend', 'data')
DB_FILE = os.path.join(DIR_DATA, 'data.db')
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
conn.row_factory = sqlite3.Row  # Return rows as dictionaries

def create_urlaccess_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS urlaccess (
        AccessID INTEGER PRIMARY KEY,
        UrlID INTEGER,
        TimesAccess INTEGER
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()

def create_sqlite_trigger(conn):
    trigger_sql = """
    CREATE TRIGGER IF NOT EXISTS Insertar_url_crear_urlaccess
    AFTER INSERT ON url
    BEGIN
        INSERT INTO urlaccess (UrlID, TimesAccess)
        VALUES (NEW.ID, 0);
    END;

    CREATE TRIGGER IF NOT EXISTS Eliminar_url_eliminar_urlaccess
    AFTER DELETE ON url
    BEGIN
        DELETE FROM urlaccess WHERE UrlID = OLD.ID;
    END;
    """
    cursor = conn.cursor()
    cursor.executescript(trigger_sql)
    conn.commit()

create_urlaccess_table(conn)
create_sqlite_trigger(conn)