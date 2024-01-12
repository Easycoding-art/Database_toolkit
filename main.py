import db
import random
from Fake_data import GetFakeData, GetRandomText
people = [i+1 for i in range(100)]
adverts = [i+1 for i in range(100)]
cities = [1, 2, 3, 4]
types = [1, 2]
categories = [1, 2, 3, 4]
def delete_trash(str, symbols) :
    for a in symbols :
        str = str.replace(a, '')
    return str
def region() :
    return ["INSERT INTO region(name) VALUES ('Central'), ('Siberia'), ('East')"]
def category() :
    return ["INSERT INTO category(name) VALUES ('toys'), ('cars'), ('animals'), ('flats')"]
def type() :
    return ["INSERT INTO type(name) VALUES ('goods'), ('services')"]
def city() :
    return ["INSERT INTO city(region, name) VALUES (1, 'Moscow'), (1, 'St. Petersburg'), (2, 'Novosibirsk'), (3, 'Vladivostok')"]
def advert(n) :
    fake_data = GetFakeData(['date', 'url'], n)
    prices = [random.randint(0, 100000) for i in range(n)]
    values_comb = [people, cities, fake_data.get('Date'), ['a', 'b', 'c', 'd'], 
              prices, types, GetRandomText(n), fake_data.get('URL'), categories, ['TRUE']]
    func = lambda  a : random.choice(values_comb[a])
    values_arr = [f"({func(0)}, {func(1)}, '{func(2)}', '{func(3)}', {func(4)}, {func(5)}, '{func(6)}', '{func(7)}', {func(8)}, {func(9)})"
              for i in range(n)]
    values_str = ', '.join(values_arr)
    return[f"INSERT INTO advert(seller, city, date, name, price, type, data, image, category, status) VALUES {values_str}"]
def user(n) :
    fake_data = GetFakeData(['name', 'email', 'password', 'phone_number'], n)
    values_comb = [fake_data.get('Name'),fake_data.get('Email'), 
                   fake_data.get('Password'), fake_data.get('Phone_number')]
    func = lambda  a : random.choice(values_comb[a])
    password = delete_trash(func(2), [' ', ')', '(', '"'])
    values_arr = [f"('{func(0)}', '{func(1)}', '{password}', '{func(3)}')"
              for i in range(n)]
    values_str = ', '.join(values_arr)
    return [f'INSERT INTO "user"(full_name, email, password, phone_number) VALUES {values_str}']
def purchase(n):
    fake_data = GetFakeData(['date'], n)
    prices = [random.randint(0, 100000) for i in range(n)]
    values_comb = [people, adverts, fake_data.get('Date'), prices]
    func = lambda  a : random.choice(values_comb[a])
    values_arr = [f"({func(0)}, {func(1)}, '{func(2)}', {func(3)})"
              for i in range(n)]
    values_str = ', '.join(values_arr)
    return [f"INSERT INTO purchase(buyer, advert, date, price) VALUES {values_str}"]
def message(n) :
    fake_data = GetFakeData(['date', 'url'], n)
    values_comb = [people, people, GetRandomText(n), fake_data.get('URL'), fake_data.get('Date')]
    func = lambda  a : random.choice(values_comb[a])
    values_arr = [f"({func(0)}, {func(1)}, '{func(2)}', '{func(3)}', '{func(4)}')"
              for i in range(n)]
    values_str = ', '.join(values_arr)
    return [f"INSERT INTO message(sender, recipient, text, image, date) VALUES {values_str}"]
def review(n) :
    fake_data = GetFakeData(['url'], n)
    scores = [random.randint(0, 10) for i in range(n)]
    values_comb = [adverts, people, GetRandomText(n, 'отличный товар'), scores, fake_data.get('URL')]
    func = lambda  a : random.choice(values_comb[a])
    values_arr = [f"({func(0)}, {func(1)}, '{func(2)}', {func(3)}, '{func(4)}')" for i in range(n)]
    values_str = ', '.join(values_arr)
    return [f"INSERT INTO review(advert, sender, text, score, image) VALUES {values_str}"]

if __name__ == "__main__" :
    #name = input()
    #password = input()
    name = 'avito3'
    password = '1234'
    db = db.My_DB(name, password)
    
    db.fill_data(category(), type(), region(), city(), 
                   user(100),  advert(100), purchase(100), message(100), review(100))