import sqlite3
import logging

logger = logging.getLogger('WhoCallsUltimate')

class DatabaseManager:
    def __init__(self, db_name='who_calls.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            return False
            
    def setup_tables(self):
        """Создание таблиц базы данных"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS phones (
                    id INTEGER PRIMARY KEY,
                    number TEXT UNIQUE,
                    city TEXT,
                    used INTEGER DEFAULT 0,
                    last_used TEXT
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    website TEXT,
                    phone TEXT,
                    success INTEGER,
                    duration REAL,
                    income REAL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    category TEXT,
                    key TEXT,
                    value TEXT,
                    PRIMARY KEY (category, key)
                )
            ''')
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания таблиц: {e}")
            return False
            
    def close(self):
        """Закрытие соединения с базой данных"""
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                logger.error(f"Ошибка закрытия базы данных: {e}")