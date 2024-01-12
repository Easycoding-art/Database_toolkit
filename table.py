from prettytable import PrettyTable

def print_table(arrays) :
    mytable = PrettyTable()
    arrays = list(map(lambda x : list(x), arrays))
    mytable.add_rows(arrays)
    print(mytable)