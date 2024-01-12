import db

if __name__ == "__main__" :
    #name = input()
    #password = input()
    #folder = input()
    name = 'avito3'
    password = '1234'
    folder = 'config'
    db = db.My_DB(name, password)

    db.set_tables(['category', 'type', 'region', 'city', 
                    'user',  'advert', 'purchase', 'message', 'review'], folder)