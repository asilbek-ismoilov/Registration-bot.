import time
import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = (), fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        try:
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        except sqlite3.DatabaseError as e:
            print(f"Error executing SQL: {e}")
        finally:
            connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        full_name TEXT,
        telegram_id INTEGER UNIQUE,
        name TEXT,
        surname TEXT,
        phone TEXT
        );
        """
        self.execute(sql, commit=True)

    def create_table_course(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Cours(
        name TEXT,
        description TEXT
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id: int, full_name: str, name: str = "name", surname: str = "surname", phone: str = "998999999999"):
        sql = """
        INSERT INTO Users(telegram_id, full_name, name, surname, phone) 
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
        full_name=excluded.full_name,
        name=excluded.name,
        surname=excluded.surname,
        phone=excluded.phone;
        """
        self.execute(sql, parameters=(telegram_id, full_name, name, surname, phone), commit=True)

    def add_course(self, name: str, description: str):
        sql = """
        INSERT INTO Cours(name, description) VALUES(?, ?)
        """
        self.execute(sql, parameters=(name, description), commit=True)

    def all_course_name(self):
        sql = """SELECT name FROM Cours;"""
        return self.execute(sql, fetchall=True)

    def get_courses(self, name):
        sql = """SELECT * FROM Cours WHERE name = ?"""
        return self.execute(sql, parameters=(name,), fetchall=True)
    
    def delete_courses(self, name):
        time.sleep(0.1) 
        sql = """DELETE FROM Cours WHERE name = ?"""
        return self.execute(sql, parameters=(name,), commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users;"
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def update_user_name(self, telegram_id: int, name: str):
        sql = "UPDATE Users SET name = ? WHERE telegram_id = ?"
        self.execute(sql, parameters=(name, telegram_id), commit=True)

    def update_user_surname(self, telegram_id: int, surname: str):
        sql = "UPDATE Users SET surname = ? WHERE telegram_id = ?"
        self.execute(sql, parameters=(surname, telegram_id), commit=True)

    def update_user_phone(self, telegram_id: int, phone: str):
        sql = "UPDATE Users SET phone = ? WHERE telegram_id = ?"
        self.execute(sql, parameters=(phone, telegram_id), commit=True)

    def select_user_by_id(self, telegram_id: int):
        sql = "SELECT * FROM Users WHERE telegram_id = ?"
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def all_users_id(self):
        return self.execute("SELECT telegram_id FROM Users;", fetchall=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")