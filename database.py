import sqlite3
from flask import g


class Database:
    def __init__(self, app, database_path):
        self.app = app
        self.DATABASE_PATH = database_path
        app.teardown_appcontext(self.close_connection)

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.DATABASE_PATH)
            db.row_factory = sqlite3.Row
        return db

    def close_connection(self, exception=None):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def init_db(self):
        with self.app.app_context():
            db = self.get_db()
            with self.app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def query_db(self, query, args=(), one=False):
        cur = self.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        self.get_db().commit()
        return (rv[0] if rv else None) if one else rv

    def insert_activity(self, user_id, activity_type):
        query = "INSERT INTO user_activity (user_id, activity_type) VALUES (?, ?)"
        self.query_db(query, [user_id, activity_type])
