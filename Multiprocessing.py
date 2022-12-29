import time

import pandas as pd
import os
from multiprocessing import Pool
from csv_splitter import split

vacancy_name = 'программист'

def join_dict(dict1, dict2):
    for i in dict2:
        if i in dict1:
            dict1[i] += dict2[i]
        else:
            dict1[i] = dict2[i]

    return dict1


def calculate_mean_city_salary(sum_salary_dict:dict, vacancy_count_dict:dict):
    for i in vacancy_count_dict:
        sum_salary_dict[i] = int(sum_salary_dict[i]/vacancy_count_dict[i])
    return sum_salary_dict


def analyze(filename):
    '''
    эта функция производит анализ csv файла

    :param filename : название чанка для анализа

    :return: кортеж вида (средняя зп, число вакансий, средняя зп для выбраной вакансии, количество вакансий для выбраной вакансии, словарь сумм зарплат по городам, словарь количества вакансий по городам)
    '''
    df = pd.read_csv(fr"splited_csv\\" + filename ).dropna()
    df['salary'] = (df['salary_from'] + df['salary_to'])/2
    df = df.drop(['salary_from', 'salary_to', 'published_at', 'salary_currency'], axis=1)
    df['name'] = df['name'].str.lower()
    vacancy_df = df[df['name'].str.contains(r'\b' + vacancy_name)]
    df = df.drop(['name'], axis=1)

    salary = int(df['salary'].mean())

    all_vacancies_count = len(df.index)

    vacancy_salary = int(vacancy_df['salary'].mean())

    vacancy_count = len(vacancy_df.index)

    city_salary = df.groupby(['area_name']).sum().round().to_dict('dict')['salary']
    city_count = df.groupby(['area_name']).count().to_dict('dict')['salary']
    #print(df.dtypes)
    #print(df.head())
    return (salary, all_vacancies_count, vacancy_salary, vacancy_count, city_salary, city_count)


def summarise(x):
    '''
    эта функция подготовливает и выводит в консоль данные, полученные в результате анализа чанков исходного csv
    :param x массив кортежей, полученных из метода analyze:
    '''
    salary_dict = dict()
    vacancies_count = dict()
    vacancy_salary = dict()
    vacancy_count = dict()
    city_salary = dict()
    city_count = dict()

    for i in range(len(x)):
        salary_dict[int(csvs[i].split('.')[0])] = x[i][0]
        vacancies_count[int(csvs[i].split('.')[0])] = x[i][1]
        vacancy_salary[int(csvs[i].split('.')[0])] = x[i][2]
        vacancy_count[int(csvs[i].split('.')[0])] = x[i][3]
        city_salary = join_dict(city_salary, x[i][4])
        city_count = join_dict(city_count, x[i][5])

    city_salary = dict(sorted(calculate_mean_city_salary(city_salary, city_count).items(), key=lambda item: item[1], reverse=True))
    all_vacancies_count = sum(city_count.values())

    for i in city_count:
        city_count[i] = float(format(city_count[i]/all_vacancies_count, '.10f'))
    city_count = dict(sorted(city_count.items(), key=lambda item: item[1], reverse=True))

    print('Динамика уровня зарплат по годам:', end=' ')
    print(salary_dict)
    print()
    print('Динамика количества вакансий по годам:', end=' ')
    print(vacancies_count)
    print()
    print('Динамика уровня зарплат по годам для выбранной профессии:', end=' ')
    print(vacancy_salary)
    print()
    print('Динамика количества вакансий по годам для выбранной профессии:', end=' ')
    print(vacancy_count)
    print()
    print('Уровень зарплат по городам (в порядке убывания):', end=' ')
    print(city_salary)
    print()
    print('Доля вакансий по городам (в порядке убывания):', end=' ')
    print(city_count)


if __name__ == '__main__':
    split(input("Введите название файла"))
    profession_name = input('Введите название профессии:')

    csvs = os.listdir(fr"C:\Users\Admin\Desktop\Прога\3 семестр\Python\Kuleshov\splited_csv")
    with Pool(8) as p:
        summarise(p.map(analyze, csvs))
