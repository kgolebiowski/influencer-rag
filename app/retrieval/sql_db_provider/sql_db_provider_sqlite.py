import os
import sqlite3


class SQLiteProvider:
    def __init__(self, db_path='data/app_database.db'):
        self.db_path = db_path
        self.ddl_path = 'app/retrieval/sql_db_provider/resources/ddl.sql'

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        db_exists = os.path.exists(self.db_path)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute('PRAGMA foreign_keys = ON;') # Enable foreign keys
        self.cursor = self.conn.cursor()

        if not db_exists:
            self.create_schema()

    def create_schema(self):
        with open(self.ddl_path, 'r') as f:
            ddl_sql = f.read()

        self.cursor.executescript(ddl_sql)
        self.conn.commit()

    def run_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def add_channel(self, title, url):
        insert_query = """
        INSERT INTO channel (title, url)
        VALUES (?, ?);
        """
        self.cursor.execute(insert_query, (title, url))
        self.conn.commit()
        return self.cursor.lastrowid  # Returns the channelId of the newly added channel

    def add_movie(self, channel_id, title, url, keywords, summary, length, paragraphs):
        insert_movie_query = """
        INSERT INTO movie (channelId, title, url, keywords, summary, length)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        self.cursor.execute(insert_movie_query, (channel_id, title, url, keywords, summary, length))
        movie_id = self.cursor.lastrowid

        insert_paragraph_query = """
        INSERT INTO paragraph (movieId, content)
        VALUES (?, ?);
        """
        for paragraph in paragraphs:
            self.cursor.execute(insert_paragraph_query, (movie_id, paragraph))

        self.conn.commit()
        return movie_id

    def clear_all_data(self):
        self.cursor.execute('DELETE FROM channel;')
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
