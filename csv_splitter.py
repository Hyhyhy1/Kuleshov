import csv
import pandas as pd


def split(file_name):
    '''
    эта функция разбивает csv файл file_name на чанки но годам
    :param file_name : название файла csv, который нужно разбить на чанки
    '''
    data = pd.read_csv(file_name)
    temp = data.groupby(data["published_at"].str.split('-').str[0])\
        .apply(lambda x: x.to_csv(fr"C:\Users\Admin\Desktop\Прога\3 семестр\Python\Kuleshov\splited_csv\{x.name}.csv", index=False))


if __name__ == "__main__":
    split("vacancies_by_year.csv")