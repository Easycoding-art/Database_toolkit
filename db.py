import psycopg2
import os
import parser_file as p
import random
from Fake_data import GetFakeData
import pandas as pd

class My_DB() :
    def __init__(self, name, password, file_path) :
        self.__name = name
        self.__password = password
        self.__schema, self.__temporal_mode = p.parse_schema(file_path)

        conn = psycopg2.connect(dbname="postgres", user="postgres", password=password, host="localhost")
        cursor = conn.cursor()
        conn.autocommit = True
        try :
            # команда для создания базы данных
            sql = f"CREATE DATABASE {name}"
            # выполняем код sql
            cursor.execute(sql)
            print("База данных успешно создана")
            cursor.close()
            conn.close()
            con = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host="localhost")
            cur = con.cursor()
            tables_by_priority = p.table_priority(self.__schema)
            for table in tables_by_priority :
                query_text = p.get_query(table)
                cur.execute(query_text)
            if self.__temporal_mode == True :
                limitations = p.set_limitations(self.__schema)
                cur.execute(limitations)
            print("Таблицы созданы")
            con.commit()
            cur.close()
            con.close()
        except psycopg2.ProgrammingError as e:
            print("База данных уже существует")
            cursor.close()
            conn.close()
    def set_query(self, query) :
        con = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host="localhost")
        df = pd.read_sql(query, con)
        return df
    def fill_fake_data(self, interval, lang = "ru_RU", auto_fill = True, **kwargs) :
        tables = []
        ordered = p.table_priority(self.__schema)
        for table in ordered:
            t_name = table.get('name')
            fields = table.get('fields')
            tables.append({'table_name': t_name, 'columns' : fields})
        conn = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host="localhost")
        cursor = conn.cursor()
        # данные для добавления
        for table in tables :
            n = random.randint(interval[0], interval[1])
            table_name = table.get('table_name')
            columns =  table.get('columns')
            field_names = []
            for column in columns :
                field_names.append(column.get('field_name'))
            if auto_fill == True :
                expected = ['first_name', 'last_name','full_name',
                            'email', 'password', 'phone_number',
                            'job', 'company', 'date',
                            'url', 'website']
                created = list(filter(lambda x : x in expected, field_names))
                created_data = GetFakeData(created, lang, n)
                if not kwargs :
                    other_data = {}
                else :
                    other_data = {field_name.title() : kwargs.get(field_name)(n) for field_name in field_names if field_name not in expected}
                all_data = {**created_data, **other_data}
            else :
                all_data = [{field_name.title() : kwargs.get(field_name)(n)} for field_name in field_names]
            result = [tuple([all_data.get(field_name.title())[i] for field_name in field_names]) for i in range(n)]
            cursor.executemany(f'INSERT INTO "{table_name}" ({", ".join(field_names)}) VALUES ({", ".join(["%s"]*len(field_names))})', result)
        conn.commit()  
        print("Данные добавлены")
        cursor.close()
        conn.close()