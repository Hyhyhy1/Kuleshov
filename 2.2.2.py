import csv
import re
import var_dump
import prettytable
from prettytable import PrettyTable

empty_file = False

def first_task():

    correct_input = True

    class DataSet:

        def __init__(self, file_name):
            setattr(self, 'file_name', file_name)
            setattr(self, 'vacancies_objects', self.csv_filer(file_name))

        def get_vacancies(self, file_name):
            with open(file_name, encoding='utf-8-sig') as csv_file:
                reader = csv.reader(csv_file)
                data = [row for row in reader]

            if not data[0]:
                print('Пустой файл')
                return

            titles = data.pop(0)

            return data, titles

        def csv_filer(self, file_name):
            data = self.get_vacancies(file_name)
            if not data:
                return
            global not_empty_file
            not_empty_file = True
            reader = data[0]
            list_naming = data[1]

            for i in range(len(list_naming)):
                remove_repeated_spaces(list_naming[i])

            fields_count = len(list_naming)
            result = []

            for vacancy in reader:
                if len(vacancy) != fields_count:
                    continue

                if contains_empty_fields(vacancy):
                    continue

                vacancy_data = dict(zip(list_naming, vacancy))
                result.append(Vacancy(vacancy_data))

            return result

    class Vacancy:

        def __init__(self, vacancy_dict):
            self.name = vacancy_dict['name']
            self.description = remove_repeated_spaces(clear_html(vacancy_dict['description']))
            self.key_skills = vacancy_dict['key_skills'].split('\n')
            self.experience_id = vacancy_dict['experience_id']
            self.premium = vacancy_dict['premium']
            self.employer_name = vacancy_dict['employer_name']
            self.salary = Salary({'salary_from': vacancy_dict['salary_from'], 'salary_to': vacancy_dict['salary_to'],
                                  'salary_gross': vacancy_dict['salary_gross'],
                                  'salary_currency': vacancy_dict['salary_currency']})
            self.area_name = vacancy_dict['area_name']
            self.published_at = vacancy_dict['published_at']

    class Salary:

        def __init__(self, salary_components):
            for key in salary_components:
                setattr(self, key, salary_components[key])

    def clear_html(vacancy_field):
        return re.sub(r"<.*?>", "", vacancy_field)

    def contains_empty_fields(vacancy):
        for field in vacancy:
            if not field or field.isspace():
                return True
        return False

    def remove_repeated_spaces(text):
        text = re.sub(r"\n", ', ', text)
        text = re.sub(r" +", " ", text)
        text = text.strip()
        return text

    file_name = input('Введите название файла: ')
    if not file_name:
        correct_input = False
    filtration_parameter = input('Введите параметр фильтрации: ')
    sorting_parametere = input('Введите параметр сортировки: ')
    is_reversed = input('Обратный порядок сортировки (Да / Нет): ')
    rows_range = input('Введите диапазон вывода: ')
    required_columns = input('Введите требуемые столбцы: ')

    if (correct_input):
        dataSet = DataSet(file_name)
    if (not_empty_file):
        var_dump.var_dump(dataSet)


def second_task():
    class Vacancy:

        def __init__(self, vacancy_dict):
            for key in vacancy_dict:
                setattr(self, key, vacancy_dict[key])

        def form_salary(self):
            salary_from = '{:,}'.format(int(float(getattr(self, 'salary_from')))).replace(',', ' ')
            salary_to = '{:,}'.format(int(float(getattr(self, 'salary_to')))).replace(',', ' ')
            salary_gross = 'Без вычета налогов' if getattr(self, 'salary_gross') == 'Да' else 'С вычетом налогов'
            setattr(self, 'salary',
                    f'{salary_from} - {salary_to} ({getattr(self, "salary_currency")}) ({salary_gross})')
            delattr(self, 'salary_gross')

        def format_date(self):
            temp = getattr(self, 'published_at')[:10].split('-')
            temp = temp[::-1]
            self.published_at = '.'.join(temp)

    def clear_html(vacancy_field):
        return re.sub(r"<.*?>", "", vacancy_field)

    def form_row(vacancy):
        return [vacancy.name, vacancy.description, vacancy.key_skills,
                vacancy.experience_id, vacancy.premium, vacancy.employer_name,
                vacancy.salary, vacancy.area_name, vacancy.published_at]

    def contains_empty_fields(vacancy):
        for field in vacancy:
            if not field or field.isspace():
                return True
        return False

    def build_table(data_vacancies, dict_naming):
        table = PrettyTable()
        table_sizes = {'№': 20}
        table_names = ['№']
        for key in dict_naming:
            table_names.append(dict_naming[key])
            table_sizes[dict_naming[key]] = 20

        table.field_names = table_names
        table.align = 'l'
        table._max_width = table_sizes
        table.hrules = prettytable.ALL

        for index in range(len(data_vacancies)):
            vacancy_data = [index + 1]
            vacancy = formatter(data_vacancies[index])
            vacancy_data += form_row(vacancy)
            table.add_row(vacancy_data)

        return table

    def remove_repeated_spaces(text):
        text = re.sub(r" +", " ", text)
        text = text.strip()
        return text

    def replace_boolean_values(text):
        text = re.sub("True", 'Да', text)
        text = re.sub("TRUE", 'Да', text)
        text = re.sub("False", 'Нет', text)
        text = re.sub("FALSE", 'Нет', text)
        return text

    def request_parser(text):
        text = text.split(": ")
        if text[0] == "Навыки":
            text[1] = text[1].split(", ")
        return text

    def string_reducer(text):
        if len(text) > 100:
            text = text[:100]
            text += '...'
        return text

    def csv_reader(file_name):
        with open(file_name, encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)
            data = [row for row in reader]

        if not data:
            print('Пустой файл')
            return

        titles = data.pop(0)
        if not data:
            print("Нет данных")
            return

        return data, titles

    def csv_filer(reader, list_naming):
        for i in range(len(list_naming)):
            remove_repeated_spaces(list_naming[i])

        fields_count = len(list_naming)
        result = []

        for vacancy in reader:
            if len(vacancy) != fields_count:
                continue

            if contains_empty_fields(vacancy):
                continue

            vacancy_data = dict(zip(list_naming, vacancy))
            result.append(Vacancy(vacancy_data))

        return result

    def formatter(vacancy):
        vacancy_attributes = [a for a in dir(vacancy) if not a.startswith('__') and not callable(getattr(vacancy, a))]
        for attribute in vacancy_attributes:
            setattr(vacancy, attribute, string_reducer(remove_repeated_spaces(clear_html(getattr(vacancy, attribute)))))

        vacancy.premium = replace_boolean_values(vacancy.premium)
        vacancy.salary_gross = replace_boolean_values(vacancy.salary_gross)
        vacancy.experience_id = experience_replacements.get(vacancy.experience_id)
        vacancy.salary_currency = currency_replacements.get(vacancy.salary_currency)
        vacancy.key_skills = re.sub('\n', "\n", vacancy.key_skills)
        vacancy.format_date()
        vacancy.form_salary()
        return vacancy

    def print_vacancies(data_vacancies, dict_naming, request_parameters):
        table = build_table(data_vacancies, dict_naming)

        # мне очень не нравится как это выглядит, но это единственный способ, как я могу это сделать
        if len(row_numbers[0]) == 0 and len(column_names[0]) == 0:
            table = table

        elif len(row_numbers[0]) == 0 and len(column_names[0]) != 0:
            fields = list(set(names_replacements.values()) - set(['№'] + column_names))
            for field in fields:
                table.del_column(field)

        elif len(row_numbers) == 1 and len(row_numbers[0]) != 0 and len(column_names[0]) == 0:
            for i in range(1, int(row_numbers[0])):
                table.del_row(0)

        elif len(row_numbers) == 1 and len(row_numbers[0]) != 0 and len(column_names[0]) != 0:
            for i in range(1, int(row_numbers[0])):
                table.del_row(0)

            fields = list(set(names_replacements.values()) - set(['№'] + column_names))
            for field in fields:
                table.del_column(field)

        elif len(row_numbers) == 2 and len(column_names[0]) == 0:
            for i in range(1, int(row_numbers[0])):
                table.del_row(0)

            for i in range(0, len(data_vacancies) + 1 - int(row_numbers[1])):
                table.del_row(int(row_numbers[1]) - int(row_numbers[0]))

        else:
            for i in range(1, int(row_numbers[0])):
                table.del_row(0)

            for i in range(0, len(data_vacancies) + 1 - int(row_numbers[1])):
                table.del_row(int(row_numbers[1]) - int(row_numbers[0]))

            fields = list(set(names_replacements.values()) - set(['№'] + column_names))
            for field in fields:
                table.del_column(field)

        # это можно сделать более компактным и простым?..
        if not request_parameters:
            print(table)
            return

        if ":" not in request_parameters:
            print('Формат ввода некорректен')
            return

        request_parameters = request_parser(request_parameters)
        if request_parameters[0] not in ['Название', 'Описание', 'Навыки', 'Опыт работы',
                                         'Премиум-вакансия', 'Идентификатор валюты оклада', 'Компания',
                                         'Оклад', 'Название региона', 'Дата публикации вакансии']:
            print('Параметр поиска некорректен')
            return

        if request_parameters[0] == 'Название' or request_parameters[0] == 'Описание' or \
                request_parameters[0] == 'Компания' or request_parameters[0] == 'Дата публикации вакансии' \
                or request_parameters[0] == 'Опыт работы' or request_parameters[0] == 'Премиум-вакансия' \
                or request_parameters[0] == 'Название региона':

            found_values_count = 0
            for row_number in range(0, len(table.rows)):
                vacancy = data_vacancies[row_number]

                if getattr(vacancy, reversed_name_replacements[request_parameters[0]]) != string_reducer(
                        request_parameters[1]):
                    table.del_row(found_values_count)
                else:
                    found_values_count += 1  # Компания: БИГЦЕНТР

        elif request_parameters[0] == 'Навыки':
            found_values_count = 0
            for row_number in range(0, len(table.rows)):
                vacancy_skills = getattr(data_vacancies[row_number], reversed_name_replacements[request_parameters[0]])
                flag = False

                for skill in request_parameters[1]:
                    if skill not in vacancy_skills:
                        flag = True
                        break

                if flag:
                    table.del_row(found_values_count)
                else:
                    found_values_count += 1

        elif request_parameters[0] == 'Оклад':
            found_values_count = 0
            for row_number in range(0, len(table.rows)):
                vacancy = data_vacancies[row_number]
                if vacancy.salary_from <= request_parameters[1] <= vacancy.salary_to:
                    found_values_count += 1
                else:
                    table.del_row(found_values_count)

        elif request_parameters[0] == 'Идентификатор валюты оклада':
            found_values_count = 0
            for row_number in range(0, len(table.rows)):
                vacancy = data_vacancies[row_number]
                if vacancy.salary_currency == request_parameters[1]:
                    found_values_count += 1
                else:
                    table.del_row(found_values_count)

        if len(table.rows) > 0:
            print(table)
        else:
            print('Ничего не найдено')

    names_replacements = {'name': 'Название',
                          'description': 'Описание',
                          'key_skills': 'Навыки',
                          'experience_id': 'Опыт работы',
                          'premium': 'Премиум-вакансия',
                          'employer_name': 'Компания',
                          'salary': 'Оклад',
                          'area_name': 'Название региона',
                          'published_at': 'Дата публикации вакансии'}

    reversed_name_replacements = {'Название': 'name',
                                  'Описание': 'description',
                                  'Навыки': 'key_skills',
                                  'Опыт работы': 'experience_id',
                                  'Премиум-вакансия': 'premium',
                                  'Компания': 'employer_name',
                                  'Оклад': 'salary',
                                  'Название региона': 'area_name',
                                  'Дата публикации вакансии': 'published_at'}

    experience_replacements = {"noExperience": "Нет опыта",
                               "between1And3": "От 1 года до 3 лет",
                               "between3And6": "От 3 до 6 лет",
                               "moreThan6": "Более 6 лет"}

    currency_replacements = {"AZN": "Манаты",
                             "BYR": "Белорусские рубли",
                             "EUR": "Евро",
                             "GEL": "Грузинский лари",
                             "KGS": "Киргизский сом",
                             "KZT": "Тенге",
                             "RUR": "Рубли",
                             "UAH": "Гривны",
                             "USD": "Доллары",
                             "UZS": "Узбекский сум"}

    table_data = csv_reader(input())
    # table_data = csv_reader('vacancies.csv')
    request_parameters = input()
    row_numbers = input().split(' ')
    column_names = input().split(', ')
    if table_data is not None:
        print_vacancies(csv_filer(table_data[0], table_data[1]), names_replacements, request_parameters)


def main():
    action = input()

    if action == 'Статистика':
        first_task()
    elif action == 'Вакансии':
        second_task()
    else:
        print('Некорректный ввод')


main()