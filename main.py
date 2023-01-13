#homework OOP-2
class Student:
    def __init__(self, name, surname, gender='М'):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lect(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _calc_avg(self):
        # вычисление средней оценки по всем курсам (согласно п.2 задания 3)
        if len(self.grades) == 0:
            return 0
        lst = [sum(v) / len(v) for v in self.grades.values()]
        return sum(lst) / len(lst)

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self._calc_avg():2.1f}\n' +\
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" +\
            f"Завершенные курсы: {', '.join(self.finished_courses)}\n"
        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Сравнение можно выполнить только с объектом класса Student.')
            return
        return self._calc_avg() < other._calc_avg()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.avg_grade = 0

    def _calc_avg(self):
        # вычисление средней оценки по всем курсам (согласно п.2 задания 3)
        if len(self.grades) == 0:
            return 0
        lst = [sum(v) / len(v) for v in self.grades.values()]
        self.avg_grade = sum(lst) / len(lst)
        return self.avg_grade

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self._calc_avg():2.1f}\n'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Сравнение можно выполнить только с объектом класса Lecturer.')
            return
        return self._calc_avg() < other._calc_avg()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\n'
        return res

    def __lt__(self, other):
        if not isinstance(other, Reviewer):
            print('Сравнение можно выполнить только с объектом класса Reviewer.')
            return
        return self.surname < other.surname


import random

lect, rev, stud = [], [], []
names = ['Гаврила', 'Иван', 'Петр', 'Федор', 'Кирилл', 'Сергей', 'Семен']
surnames = ['Иванов', 'Петров', 'Федоров', 'Кириллов', 'Сергеев', 'Семенов', 'Дзержинский', 'Троцкий', 'Берия',
            'Хрущев', 'Андропов', 'Брежнев']

def random_object(cls):
    new_obj = cls(random.choice(names), surnames.pop(random.randint(0, len(surnames) - 1)))
    if not isinstance(new_obj, Student):
        new_obj.courses_attached += ['Python', 'Java']
    return new_obj

def random_list_init():
    # инициализация лекторов и аспирантов
    for _ in range(3):
        lect.append(random_object(Lecturer))
        rev.append(random_object(Reviewer))
        #print(lect[i])
    # инициализация студентов
    for i in range(5):
        new_student = random_object(Student)
        new_student.add_courses('Git')
        if i % 2 == 0:
            new_student.add_courses('Введение в программирование')
        new_student.courses_in_progress += ['Python', 'Java']
        stud.append(new_student)
        # проставление студентами оценок лекторам
        for lec in lect:
            new_student.rate_lect(lec, 'Python', random.randint(6, 10))
            new_student.rate_lect(lec, 'Java', random.randint(6, 10))
        #print(stud[i])
    # проставление аспирантами оценок студентам
    for asp in rev:
        for st in stud:
            asp.rate_hw(st,'Python', random.randint(6, 10))
            asp.rate_hw(st, 'Java', random.randint(6, 10))

def print_list(selector):
    # функция для демонстрации перегруженного метода __str__ для всех классов (п.1 задание 3)
    # для сортировки списков используются перегруженные методы __lt__ (п.2 задание 3)
    list_dict = {'лекторов': lect, 'аспирантов': rev, 'студентов': stud}
    lst = list_dict[selector]
    title = f'***** Список всех {selector} (всего: {len(lst)}) *****\n'
    print(title)
    if selector != 'аспирантов':
        lst = sorted(lst, key=lambda x: -x._calc_avg())
    else:
        lst = sorted(lst)
    for el in lst:
        print(el)
    print('*' * len(title))
def show_rev_list():
    print_list('аспирантов')

def show_lect_list():
    print_list('лекторов')

def show_stud_list():
    print_list('студентов')

def avg_students_grade_for_course(students, course):
    # функция для подсчета средней оценки студентов по курсу (п.1 задание 4)
    lst = [grade for st in students for grade in st.grades[course]]
    print(f'Курс: {course}  средний балл студентов: {(sum(lst) / len(lst)):2.1f}')

def avg_lecturers_grade_for_course(lecturers, course):
    # функция для подсчета средней оценки лекторов по курсу (п.2 задание 4)
    lst = [grade for lc in lecturers for grade in lc.grades[course]]
    print(f'Курс: {course}  средний балл лекторов: {(sum(lst) / len(lst)):2.1f}')

def avg_grades_for_course(course):
    print('***** Средние оценки по курсу *****')
    avg_students_grade_for_course(stud, course)
    avg_lecturers_grade_for_course(lect, course)
    print('*' * 35)

def avg_grades_for_python():
    avg_grades_for_course('Python')

def avg_grades_for_java():
    avg_grades_for_course('Java')

def react_on_kbd_command(com):
    if com == 'x':
        return
    com_dict = {
        '1': show_lect_list,
        '2': show_rev_list,
        '3': show_stud_list,
        '4': avg_grades_for_python,
        '5': avg_grades_for_java
    }
    if not com in com_dict.keys():
        print('Неизвестная команда')
        return
    return com_dict[com]()

random_list_init()
command = 'x'
while command != '0':
    react_on_kbd_command(command)
    print('0 - выход из программы\n1 - список всех лекторов\n2 - список всех аспирантов\n3 - список всех студентов\n'
          '4 - средние оценки всех студентов и лекторов по курсу Python\n'
          '5 - средние оценки всех студентов и лекторов по курсу Java\n'
          'введите команду: ')
    command = input()
print('До свидания!')


