import psycopg2
import os

class My_DB() :
    def __init__(self, name, password) :
        self.__name = name
        self.__password = password
        conn = psycopg2.connect(dbname="postgres", user="postgres", password=password, host="localhost")
        cursor = conn.cursor()
        conn.autocommit = True
        try :
            # команда для создания базы данных
            sql = f"CREATE DATABASE {name}"
            # выполняем код sql
            cursor.execute(sql)
            print("База данных успешно создана")
        except psycopg2.ProgrammingError as e:
            print("База данных уже существует")
        cursor.close()
        conn.close()
    def set_query(self, query) :
        conn = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host="localhost")
        cursor = conn.cursor()
        # создаем таблицу people
        cursor.execute(query)
        try :
            result = cursor.fetchall()
        except psycopg2.ProgrammingError :
            result = 'None'
        # поддверждаем транзакцию
        conn.commit()
        cursor.close()
        conn.close()
        return result
    def set_tables(self, ordered_tables, folder) :
        for name in ordered_tables :
            print(name)
            file = open(f'Schemas/{folder}/{name}.txt', 'r')
            query_text = file.read()
            self.set_query(query_text)
            file.close()
    def fill_data(self, *args) :
        for table in args :
            for query in table :
                print(query)
                self.set_query(query)