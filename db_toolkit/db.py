import psycopg2
import os
import db_toolkit.parser_file as p
import random
from db_toolkit.fake_data import GetFakeData
import pandas as pd

class DB_Creator() :
    def __init__(self, name, password, file_path=None, dev_mode=False, host="localhost") :
        self.__name = name
        self.__password = password
        self.__host = host
        if file_path == None :
            self.__schema, self.__temporal_mode = None, None
        else :
            self.__schema, self.__temporal_mode = p.parse_schema(file_path)
        if self.__schema != None :
            conn = psycopg2.connect(dbname="postgres", user="postgres", password=password, host=self.__host)
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
            except psycopg2.ProgrammingError as e:
                print("База данных уже существует")
                cursor.close()
                conn.close()
            else:
                try :
                    con = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host=self.__host)
                    cur = con.cursor()
                    tables_by_priority = p.table_priority(self.__schema)
                    text = ''
                    for table in tables_by_priority :
                        query_text = p.get_query(table)
                        text = text + '\n' + query_text
                        cur.execute(query_text)
                    if self.__temporal_mode == True :
                        limitations = p.set_limitations(self.__schema)
                        text = text + '\n' + limitations
                        cur.execute(limitations)
                    if dev_mode == True :
                        os.mkdir(f'{self.__name}_logs.txt')                        
                        file = open(f'{self.__name}_logs/{self.__name}_tables.txt', 'w')
                        file.write(text)
                        file.close()
                    print("Таблицы созданы")
                    con.commit()
                    cur.close()
                    con.close()
                except psycopg2.ProgrammingError as e:
                    print(e)
                    cursor.close()
                    conn.close()
    def set_query(self, query) :
        con = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host=self.__host)
        df = pd.read_sql(query, con)
        return df
    def fill_fake_data(self, interval_dict, lang = "ru_RU", auto_fill = True, **kwargs) :
        if self.__schema != None :
            tables = []
            ordered = p.table_priority(self.__schema)
            for table in ordered:
                t_name = table.get('name')
                fields = table.get('fields')
                tables.append({'table_name': t_name, 'columns' : fields})
            conn = psycopg2.connect(dbname=self.__name, user="postgres", password=self.__password, host=self.__host)
            cursor = conn.cursor()
            # данные для добавления
            for table in tables :
                table_name = table.get('table_name')
                interval = interval_dict.get(table_name)
                n = random.randint(interval[0], interval[1])
                columns = table.get('columns')
                field_names = []
                field_specials = {}
                for column in columns :
                    field_names.append(column.get('field_name'))
                    field_specials.update(
                        {column.get('field_name') : column.get('field_specials')})
                field_names = list(filter(lambda x: 'auto_inkrement' not in field_specials.get(x),
                                        field_names))
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
                field_names = [f'"{name}"' for name in field_names]
                cursor.executemany(f'INSERT INTO "{table_name}" ({", ".join(field_names)}) VALUES ({", ".join(["%s"]*len(field_names))})', result)
            conn.commit()  
            print("Данные добавлены")
            cursor.close()
            conn.close()
        else:
            print("Схема не задана!")