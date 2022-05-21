import csv
import pandas as pd
import plotly.express as px

'''Создание дополнительного файла csv с изменение процентов на численное значение для отображения на графике'''
f = open('temporaryfile', 'w', encoding='cp1251', newline='') # Создание временного файла
with open('data_out.csv', 'r', encoding='cp1251', newline='') as db:

    writer = csv.writer(f, delimiter=';')
    for i in list(db):  # Перезапись во временный файл с переводом процентов в числа
        s = []
        for j in i.split(';'):
            if '%' in j:
                s.append(float(j.replace('%', '')))
            else:
                s.append(j)
        writer.writerow(s)


df = pd.read_csv('temporaryfile',  sep=';', encoding='cp1251', parse_dates=['Date/pos'], dayfirst=True, index_col='Date/pos')



loan_amount = px.line(df, x=df.index, y= df.columns[::2])  # Создание графика общей суммы
percent = px.line(df, x=df.index, y=df.columns[1::2])  # Создание графика по процентам

''' Переименование осей и ... '''

loan_amount.update_layout(title ='Loan amount',
                  xaxis_title='Date',
                  yaxis_title='Amount',
                  legend_title='Pos')

percent.update_layout(title ='Issuance percentage',
                  xaxis_title='Date',
                  yaxis_title='Percent, %',
                  legend_title='Pos')

loan_amount.show()
percent.show()