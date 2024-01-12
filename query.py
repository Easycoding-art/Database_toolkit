import table
import db

if __name__ == "__main__" :
    name = input()
    password = input()
    db = db.My_DB(name, password)
    result = db.set_query(input())
    table.print_table(result)