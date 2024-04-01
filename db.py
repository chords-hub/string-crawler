import psycopg2
import psycopg2.extras
import os

class DatabaseHandler:
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_CHORDS_NAME')
        self.db_port = os.getenv('DB_PORT', '25059') 
        self.connect_timeout = 10
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                connect_timeout=self.connect_timeout
            )
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except psycopg2.OperationalError as e:
            print(f"Error connecting to the database: {e}")
            return False
        return True

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        if not self.cursor:
            print("Database connection is not established.")
            return None
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def add_artist_if_not_exists(self, artist_name):
        query = "SELECT * FROM artists WHERE name = %s"
        result = self.execute_query(query, (artist_name,))
        if not result:
            insert_query = "INSERT INTO artists (name) VALUES (%s) RETURNING id"
            self.cursor.execute(insert_query, (artist_name,))
            self.conn.commit()
            return self.cursor.fetchone()[0]
        else:
            return result[0]['id']
    
    def add_song_if_not_exists(self, artist_id, song_title, firebase_id):
        query = "SELECT * FROM songs WHERE artist_id = %s AND title = %s"
        result = self.execute_query(query, (artist_id, song_title))
        if not result:
            insert_query = "INSERT INTO songs (artist_id, title, firebase_id) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_query, (artist_id, song_title, firebase_id))
            self.conn.commit()
        return result

