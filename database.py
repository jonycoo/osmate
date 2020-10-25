import sqlite3
from sqlite3 import Error
import logging


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DBLite(metaclass=SingletonMeta):
    connection = None
    db_courser = None

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.connection = sqlite3.connect(db_file)
            self.db_courser = self.connection.cursor()
            self.create_table()
            self.connection.commit()
        except Error as e:
            self.logger.error(e)
            print(e)

    def create_table(self):
        self.db_courser.execute('''CREATE TEMP TABLE credentials 
        (TG_UID INTEGER PRIMARY KEY, client_key CHAR(20), client_secret CHAR(20));''')

    def insert_credentials(self, tg_uid, key, secret):
        """key and secret can be null"""
        try:
            self.db_courser.execute(
                "INSERT INTO credentials(TG_UID, client_key, client_secret) VALUES (:uid, :key, :secret);",
                {"uid": tg_uid, "key": key, "secret": secret})
        except sqlite3.IntegrityError as e:
            raise e

    def update_credentials(self, tg_uid, key, secret):
        self.db_courser.execute(
            "UPDATE OR FAIL credentials SET client_key = :key, client_secret = :secret WHERE TG_UID = :uid;",
            {"key": key, "secret": secret, "uid": tg_uid})
        if not self.db_courser.rowcount:
            raise sqlite3.IntegrityError('No such record')

    def delete_credentials(self, tg_uid):
        self.db_courser.execute(
            "DELETE FROM credentials WHERE TG_UID = :uid;", {"uid": tg_uid})
        if not self.db_courser.rowcount:
            raise sqlite3.IntegrityError('No such record')

    def select_credentials(self, tg_uid):
        data = self.db_courser.execute("SELECT client_key, client_secret FROM credentials WHERE TG_UID = :uid;",
                                       {"uid": tg_uid})
        return data.fetchone()
