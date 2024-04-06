from faker import Faker
import random
import wikipedia
def GetFakeData(data_types, language, n) :
    fake = Faker(language)
    result = {}
    if 'full_name' in data_types :
        arr1 = [fake.name() for i in range(n)]
        result = result | {'Full_Name' : arr1}
    if 'phone_number' in data_types :
        arr2 = [fake.phone_number() for i in range(n)]
        result = result | {'Phone_Number' : arr2}
    if 'email' in data_types :
        arr3 = [fake.ascii_free_email() for i in range(n)]
        result = result | {'Email' : arr3}
    if 'url' in data_types :
        arr4 = [fake.uri() for i in range(n)]
        result = result | {'URL' : arr4}
    if 'date' in data_types :
        arr5 = [fake.date_time() for i in range(n)]
        result = result | {'Date' : arr5}
    if 'password' in data_types :
        arr6 = [fake.password(length = random.randint(10,20)) for i in range(n)]
        result = result | {'Password' : arr6}
    if 'first_name' in data_types :
        arr7 = [fake.first_name() for i in range(n)]
        result = result | {'First_Name' : arr7}
    if 'last_name' in data_types :
        arr8 = [fake.last_name() for i in range(n)]
        result = result | {'Last_Name' : arr8}
    if 'job' in data_types :
        arr9 = [fake.job() for i in range(n)]
        result = result | {'Job' : arr9}
    if 'website' in data_types :
        arr10 = [fake.hostname() for i in range(n)]
        result = result | {'Website' : arr10}
    if 'company' in data_types :
        arr11 = [fake.company() for i in range(n)]
        result = result | {'Company' : arr11}
    return result

def GetRandomText(n, *patterns) :
    result_arr = []
    file = open('words.txt', 'r', encoding='utf-8')
    text = file.read()
    file.close()
    arr = text.split()
    for i in range(0, 10) :
        random.shuffle(arr)
    for k in range(n) :
        print(k)
        word = arr[random.randint(0, len(arr))]
        try :
            wikipedia.set_lang("ru")
            result = wikipedia.summary(word, sentences=random.randint(1, 3))
        except wikipedia.exceptions.DisambiguationError :
            result = word
        except wikipedia.exceptions.PageError :
            result = word
        if len(patterns) != 0 :
            if random.randint(0, 4) == 1 :
                print('sss')
                res_arr = result.split()
                for patttern in patterns :
                    res_arr.insert(random.randint(0, len(res_arr)), patttern)
                result = ' '.join(res_arr)
                if 'è' in result :
                    result = word
        result_arr.append(result)
    return result_arr