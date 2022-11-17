import csv
import re
import var_dump


not_empty_file = False
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
                              'salary_gross': vacancy_dict['salary_gross'], 'salary_currency': vacancy_dict['salary_currency']})
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
    text = re.sub(r"\n",', ', text)
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
    dataSet = DataSet('vacancies.csv')
if(not_empty_file):
    var_dump.var_dump(dataSet)