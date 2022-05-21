import csv
from decimal import Decimal

data_out = open('data_out.csv', 'w', encoding='cp1251', newline='')     #Создание и запись data_out
with open('data.csv', 'r', encoding='cp1251', newline='') as data:
    sort_data = []  #создание списка без лишних записей
    for x in list(data)[1:]:
        sort_data.append(x.rstrip().split(';'))

    writer = csv.writer(data_out, delimiter=';')    #Создаем условие как записывать

    def sort_key_pos(e):    #сортировка для удобной выборки
        return int(e[1])
    sort_data = sorted(sort_data, key=sort_key_pos)

    header = []  # Создание шапки
    for i in sort_data:
        if int(i[1]) not in header:
            header.append(int(i[1]))
            header.append(str(i[1]))

    header = ['Date/pos'] + header
    writer.writerow(header)     #Добавление шапки в таблицу

    def sort_key_date(e):
        return e[3]

    sort_data = sorted(sort_data, key=sort_key_date)    #сортировка по дате

    # создание словаря
    s = {'Date/pos': ''}
    for i in sort_data:         #перебор в списке
        s[int(i[1])] = 0
        s[i[1]] = 0             #создание ключа в словаре со значением 0

    date_words = []             #создание списка дат
    for i in sort_data:         #перебор в списке
        date = i[3]
        s['Date/pos'] = date
        if date in date_words:
            continue
        date_words.append(date)
        for j in sort_data:
            if j[3] == date:
                s[int(j[1])] += (Decimal(j[2]))     #Внесение суммы в словарь
            else:
                continue

        total_amount = 0
        for k, v in list(s.items()):    #Расчет общей суммы за дату
            if type(v) == Decimal:
                total_amount += int(v)

        for q, w in list(s.items()):    #Расчет процентов от общей суммы за разрез даты
            if type(w) == Decimal:
                s[str(q)] = str(round((int(w) / total_amount) * 100, 2)) + '%'
            else:
                continue

        dict_writer = csv.DictWriter(data_out, fieldnames=header, delimiter=';')    #согласно чему будет внесена запись
        dict_writer.writerow(s) # Внесение записи в файл

        for i in s:     #обнуление данных в словаре
            s[i] = 0

data_out.close()