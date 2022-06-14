import os
import random
import tkinter
from tkinter import font, END, Toplevel, Frame, Menu, CENTER, NO, messagebox, LEFT
from tkinter.ttk import Treeview
from functools import partial

from tk_html_widgets import HTMLLabel
from PIL import Image, ImageTk

import config

from backend.models import Lesson, Practice, Question, Student, Test, TestPassResult


MAIN_COLOR = '#f9f9f9'


# Главное окно
class Window(Frame):
    # Запуск программы, инициализация
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.widgets: list[tkinter.Widget] = []
        self.test_widgets: list[tkinter.Widget] = []
        self.auth_user: Student = Student.students.first()
        self.test_data = []
        self.last_test_pass_result: TestPassResult = None
        self.question_index = 0

        self.title = 'Электронное учебное пособие'
        self.title_html = '<h1>ЭЛЕКТРОННОЕ УЧЕБНОЕ ПОСОБИЕ<br>'
        self.title_html += '<b>АРХИТЕКТУРА АППАРАТНЫХ СРЕДСТВ</b></h1>'

        master.configure(background=MAIN_COLOR)
        # Название программы
        master.title(self.title)
        # Размеры программы
        master.geometry('780x600+400+100')
        master.resizable(width=False, height=False)

        # Меню
        menu = Menu(self.master)
        self.master.config(menu=menu)

        main_menu = Menu(menu)
        main_menu.add_command(label='Теория', command=self.show_lessons)
        main_menu.add_command(label='Практика', command=self.show_practics)
        main_menu.add_command(label='Контроль', command=self.student_auth)

        help_menu = Menu(menu)
        help_menu.add_command(label='Инструкция',
                              command=self.instruction_menu)
        help_menu.add_command(label='О программе',
                              command=self.about_menu)
        help_menu.add_command(label='Об авторе',
                              command=self.about_author_menu)

        menu.add_cascade(label='Меню', menu=main_menu)
        menu.add_cascade(label='Помощь', menu=help_menu)

    def instruction_menu(sef):
        message = 'Для прохождения тестов необходимо в пункте меню'
        message += ' выбрать "Контроль"\nПосле этого программа '
        message += 'предлагает авторизоваться.'
        message += ' Вам нужно ввести имя и фамилию в поле ввода '
        message += 'и нажать на кнопку "Авторизоваться".\n'
        message += 'После этого вы должны выбрать необходимый тест из списка '
        message += 'и нажать на кнопку "тест". '
        message += 'На прохождения теста дается определенное время, после '
        message += 'истечение которого завершается тест и программа '
        message += 'показывает результат прохождения теста.'
        messagebox.showinfo(title='Инструкция',
                            message=message)

    def about_menu(sef):
        message = 'Данный программный продукт предназначен для получения знаний в области архитектурных аппаратных \nсредств и в последующем их закреплении в виде тестирования.'
        messagebox.showinfo(title='О программе',
                            message=message)

    def about_author_menu(sef):
        message = 'Программу выполнил:\nКурсант 431 группы\nЦукуров Семен Андреевич.'
        messagebox.showinfo(title='Об авторе',
                            message=message)

    def clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()

        self.widgets.clear()

    def clear_test_widgets(self):
        for widget in self.test_widgets:
            widget.destroy()

        self.test_widgets.clear()

    def student_auth(self):
        # Авторизация студента
        form = Toplevel(self.master)
        form.configure(background=MAIN_COLOR)
        form.geometry('400x280+600+200')
        form.resizable(width=False, height=False)
        label = tkinter.Label(form,
                              background=MAIN_COLOR,
                              text='Авторизация',
                              font=font.Font(size=15))
        label.place(x=135, y=30)

        first_name_label = tkinter.Label(form,
                                         background=MAIN_COLOR,
                                         text='Имя:',
                                         font=font.Font(size=10))
        first_name_label.place(x=60, y=100)
        last_name_label = tkinter.Label(form,
                                        background=MAIN_COLOR,
                                        text='Фамилия:',
                                        font=font.Font(size=10))
        last_name_label.place(x=60, y=150)

        def check(string_var):
            s = string_var.get()
            if s and not s[-1].isalpha():
                messagebox.showinfo('Внимание', 'Только буквы', parent=form)
                string_var.set(s[:len(s)-1])

        first_name_var = tkinter.StringVar(name='first_name')
        first_name_var.trace("w", lambda *args: check(first_name_var))
        first_name_entry = tkinter.Entry(form,
                                         textvariable=first_name_var,
                                         width=30)
        first_name_entry.place(x=140, y=100)

        tkinter.Label(form,
                      text='(заполните поле буквами)',
                      background=MAIN_COLOR,
                      font=font.Font(size=8, slant=font.ITALIC)
                      ).place(x=150, y=120)

        last_name_var = tkinter.StringVar(name='last_name')
        last_name_var.trace("w", lambda *args: check(last_name_var))
        last_name_entry = tkinter.Entry(form,
                                        textvariable=last_name_var,
                                        width=30)
        last_name_entry.place(x=140, y=150)

        tkinter.Label(form,
                      text='(заполните поле буквами)',
                      background=MAIN_COLOR,
                      font=font.Font(size=8, slant=font.ITALIC)
                      ).place(x=150, y=170)

        def auth_button_click():
            nonlocal first_name_var, last_name_var, form
            first_name = first_name_var.get()
            last_name = last_name_var.get()
            student = Student.students.filter(first_name=first_name,
                                              last_name=last_name)[0]
            if not student:
                messagebox.showerror('Ошибка', 'Неверные данные!', parent=form)
                return

            self.auth_user = student
            form.destroy()
            self.show_tests()

        auth_button = tkinter.Button(form,
                                     text='Войти',
                                     command=auth_button_click)
        auth_button.place(x=200, y=200)

    def lesson_on_select(self, event):
        # При выборе лекции
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        lesson = Lesson.lessons.get(title=value)
        form = Toplevel(self.master)
        form.configure(background=MAIN_COLOR)
        form.geometry('1000x600+200+100')
        form.resizable(width=False, height=False)
        html_label = HTMLLabel(form, html=lesson.get_full_text(),
                               background=MAIN_COLOR)
        html_label.place(x=10, y=10, width=980, height=590)

    def show_lessons(self):
        # Показать список лекции
        self.clear_widgets()

        label = tkinter.Label(text='Теория', font=font.Font(size=20),
                              background=MAIN_COLOR)
        label.place(x=320, y=60)

        back_to_main_button = tkinter.Button(text='Назад',
                                             width=10,
                                             height=1,
                                             background='white',
                                             command=self.show_main_form)
        back_to_main_button.place(x=20, y=20)

        lessons = Lesson.lessons.all()
        lessons_listbox = tkinter.Listbox(width=93, height=20)
        lessons_listbox.place(x=100, y=150)
        lessons_listbox.bind('<<ListboxSelect>>', self.lesson_on_select)
        for lesson in lessons:
            lessons_listbox.insert(END, lesson.title)

        self.widgets.append(label)
        self.widgets.append(back_to_main_button)
        self.widgets.append(lessons_listbox)

    def practice_on_select(self, event):
        # При выборе практики
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        practice = Practice.practics.get(title=value)
        form = Toplevel(self.master)
        form.configure(background=MAIN_COLOR)
        form.geometry('1000x600+200+100')
        html_label = HTMLLabel(form, html=practice.get_full_text(),
                               background=MAIN_COLOR)
        html_label.place(x=10, y=10, width=980, height=590)

    def show_practics(self):
        # Меню Практика
        self.clear_widgets()

        label = tkinter.Label(text='Практика', font=font.Font(size=20),
                              background=MAIN_COLOR)
        label.place(x=320, y=60)

        back_to_main_button = tkinter.Button(text='Назад',
                                             width=10,
                                             height=1,
                                             background='white',
                                             command=self.show_main_form)
        back_to_main_button.place(x=20, y=20)

        practics = Practice.practics.all()
        practics_listbox = tkinter.Listbox(width=93, height=20)
        practics_listbox.place(x=100, y=150)
        practics_listbox.bind('<<ListboxSelect>>', self.practice_on_select)
        for practice in practics:
            practics_listbox.insert(END, practice.title)

        self.widgets.append(label)
        self.widgets.append(back_to_main_button)
        self.widgets.append(practics_listbox)

    def finish_test(self):
        self.test_finished = True
        result = self.last_test_pass_result
        test = result.test
        test_data = self.test_data
        solved = 0
        for index, test_question in enumerate(test.questions.all()):
            question = test_question.question
            ok = False
            if question.type == Question.Type.ANSWER_CHOICE:
                user_answers = sorted(test_data[index])
                answers = []
                for option in question.options.all():
                    answers.append([option.option_main, option.is_answer])
                answers.sort()
                ok = (user_answers == answers)
            elif question.type == Question.Type.ANSWER_INPUT:
                answers = []
                user_answer = test_data[index].strip()
                for option in question.options.all():
                    answers.append(option.option_main.strip())

                ok = (user_answer in answers)
            elif question.type == Question.Type.CONFORMITY:
                user_answers = []
                for a, b in zip(test_data[index][0], test_data[index][1]):
                    user_answers.append([a, b])

                answers = []
                for option in question.options.all():
                    answers.append([option.option_main.strip(),
                                    option.option_secondary.strip()])

                ok = (sorted(answers) == sorted(user_answers))
            elif question.type == Question.Type.STREAMLING:
                user_answers = test_data[index]
                answers = []
                for option in question.options.all():
                    answers.append(option.option_main)

                ok = (answers == user_answers)

            solved += ok

        result.solved = solved
        result.save()
        questions_count = test.get_questions_count()
        message = f'Ваш результат {solved}/{questions_count}'
        messagebox.showinfo(title='Тест закончен',
                            message=message)
        self.clear_test_widgets()
        self.show_tests()

    def option_type_1_changed(self, question_index, option_index):
        checked = self.test_data[question_index][option_index][1]
        self.test_data[question_index][option_index][1] = not checked

    def option_type_2_changed(self, question_index, text):
        self.test_data[question_index] = text

    def option_type_3_changed(self, question_index, option_index, delta):
        options_count = len(self.test_data[question_index])
        i = option_index
        j = (option_index+delta) % options_count
        options = self.test_data[question_index]
        options[i], options[j] = options[j], options[i]
        self.show_question(self.question_index)

    def option_type_4_changed(self, question_index, option_index, delta):
        options_count = len(self.test_data[question_index][1])
        i = option_index
        j = (option_index+delta) % options_count
        options = self.test_data[question_index][1]
        options[i], options[j] = options[j], options[i]
        self.show_question(self.question_index)

    def show_prev_question(self):
        test = self.last_test_pass_result.test
        questions_count = test.get_questions_count()
        self.question_index = (self.question_index-1) % questions_count
        self.show_question(self.question_index)

    def show_next_question(self):
        test = self.last_test_pass_result.test
        questions_count = test.get_questions_count()
        self.question_index = (self.question_index+1) % questions_count
        self.show_question(self.question_index)

    def show_question(self, question_index):
        self.clear_test_widgets()

        test = self.last_test_pass_result.test
        test_questions = test.questions.all()
        question = test_questions[question_index].question

        text = question.text.strip()
        text = text.removeprefix('<p>')
        text = text.removesuffix('</p>')
        html = f'<h3>{question_index+1}. {text}</h3>'
        question_text_label = HTMLLabel(html=html,
                                        background=MAIN_COLOR)
        question_text_label.place(x=50, y=140)

        self.test_widgets.append(question_text_label)

        test_options = self.test_data[question_index]
        if question.type == Question.Type.ANSWER_CHOICE:
            y = 220
            option_index = 0
            for option, checked in test_options:
                command = partial(self.option_type_1_changed,
                                  question_index, option_index)
                var = tkinter.BooleanVar()
                var.set(checked)
                check_button = tkinter.Checkbutton(text=option,
                                                   background=MAIN_COLOR,
                                                   command=command,
                                                   variable=var)
                check_button.place(x=40, y=y)
                self.test_widgets.append(check_button)
                y += 50
                option_index += 1
        elif question.type == Question.Type.ANSWER_INPUT:
            var = tkinter.StringVar()
            text = self.test_data[question_index]
            var.set(text)
            input = tkinter.Entry(width=25, textvariable=var)
            input.place(x=300, y=300)
            var.trace('w', lambda name, index, mode,
                      sv=var: self.option_type_2_changed(question_index,
                                                         var.get()))
            self.test_widgets.append(input)
        elif question.type == Question.Type.STREAMLING:
            y = 220
            option_index = 0
            test_options = self.test_data[question_index]
            for option in test_options:
                command = partial(self.option_type_3_changed,
                                  question_index, option_index, -1)
                up_button = tkinter.Button(text='↑',
                                           width=2,
                                           command=command)
                up_button.place(x=40, y=y)
                command = partial(self.option_type_3_changed,
                                  question_index, option_index, 1)
                down_button = tkinter.Button(text='↓',
                                             width=2,
                                             command=command)
                down_button.place(x=70, y=y)
                label = tkinter.Label(text=option,
                                      background=MAIN_COLOR)
                label.place(x=100, y=y)
                y += 70
                self.test_widgets.append(up_button)
                self.test_widgets.append(down_button)
                self.test_widgets.append(label)
                option_index += 1
        elif question.type == Question.Type.CONFORMITY:
            y = 220
            option_index = 0
            options1 = self.test_data[question_index][0]
            options2 = self.test_data[question_index][1]
            test_options = zip(options1, options2)
            for option_main, option_secondary in test_options:
                text_main = tkinter.Text(width=38, height=4)
                text_main.insert(END, option_main)
                text_main.configure(state='disabled')
                text_main.place(x=50, y=y)

                text_secondary = tkinter.Text(width=38, height=4)
                text_secondary.insert(END, option_secondary)
                text_secondary.configure(state='disabled')
                text_secondary.place(x=380, y=y)
                command = partial(self.option_type_4_changed,
                                  question_index, option_index, -1)
                up_button = tkinter.Button(text='↑',
                                           width=2,
                                           command=command)
                up_button.place(x=700, y=y)
                command = partial(self.option_type_4_changed,
                                  question_index, option_index, 1)
                down_button = tkinter.Button(text='↓',
                                             width=2,
                                             command=command)
                down_button.place(x=730, y=y)
                y += 80
                self.test_widgets.append(up_button)
                self.test_widgets.append(down_button)
                self.test_widgets.append(text_main)
                self.test_widgets.append(text_secondary)
                option_index += 1

    def start_test(self, test_index):
        self.test_finished = False
        self.clear_widgets()
        test = Test.tests.all()[test_index]
        self.test_data.clear()
        for test_question in test.questions.all():
            question = test_question.question
            if question.type == Question.Type.ANSWER_CHOICE:
                question_data = []
                for option in question.options.all():
                    question_data.append([option.option_main, False])

                random.shuffle(question_data)
                self.test_data.append(question_data)
            elif question.type == Question.Type.ANSWER_INPUT:
                self.test_data.append('')
            elif question.type == Question.Type.STREAMLING:
                options = []
                for option in question.options.all():
                    options.append(option.option_main)
                random.shuffle(options)
                self.test_data.append(options)
            elif question.type == Question.Type.CONFORMITY:
                options1 = []
                options2 = []
                for option in question.options.all():
                    options1.append(option.option_main)
                    options2.append(option.option_secondary)

                random.shuffle(options1)
                random.shuffle(options2)
                self.test_data.append([options1, options2])

        label = tkinter.Label(text=test.title,
                              font=font.Font(size=20),
                              background=MAIN_COLOR)
        label.place(x=280, y=60)

        self.last_test_pass_result = TestPassResult.results.create(
            test=test,
            student=self.auth_user,
        )
        self.timer_label = tkinter.Label(text='',
                                         background=MAIN_COLOR,
                                         font=font.Font(size=12))
        self.timer_label.place(x=50, y=50)
        self.update_clock()

        prev_button = tkinter.Button(text='←',
                                     width=5,
                                     background=MAIN_COLOR,
                                     command=self.show_prev_question)
        prev_button.place(x=550, y=560)
        next_button = tkinter.Button(text='→',
                                     width=5,
                                     background=MAIN_COLOR,
                                     command=self.show_next_question)
        next_button.place(x=600, y=560)
        finish_button = tkinter.Button(text='Закончить тест',
                                       background=MAIN_COLOR,
                                       command=self.finish_test)
        finish_button.place(x=650, y=560)

        self.widgets.append(self.timer_label)
        self.widgets.append(label)
        self.widgets.append(prev_button)
        self.widgets.append(next_button)
        self.widgets.append(finish_button)

        self.question_index = 0
        self.show_question(0)

    def update_clock(self):
        result = self.last_test_pass_result
        seconds = result.remaining_time
        if seconds <= 0:
            self.finish_test()
        else:
            if not self.test_finished:
                minutes, seconds = seconds // 60, seconds % 60
                text = '{:02}:{:02}'.format(minutes, seconds)
                self.timer_label.configure(text=text)
                self.master.after(1000, self.update_clock)

    def show_tests(self):
        # Показать тесты
        self.clear_widgets()

        label = tkinter.Label(text='Контроль', font=font.Font(size=20),
                              background=MAIN_COLOR)
        label.place(x=320, y=60)

        back_to_main_button = tkinter.Button(text='Назад',
                                             width=10,
                                             height=1,
                                             background='white',
                                             command=self.show_main_form)
        back_to_main_button.place(x=20, y=20)

        tests_table = Treeview(height=20)
        tests_table.column("#0", width=0,  stretch=NO)
        tests_table['columns'] = ('title', 'duration', 'questions_count')
        tests_table.heading('title', text='Название', anchor=CENTER)
        tests_table.heading('duration', text='Время', anchor=CENTER)
        tests_table.heading('questions_count', text='Вопросы', anchor=CENTER)
        tests_table.column('title', width=300)
        tests_table.column('duration', anchor=CENTER, width=200)
        tests_table.column('questions_count', anchor=CENTER, width=150)

        tests = Test.tests.all()
        for i, test in enumerate(tests):
            values = [test.title, test.duration, test.get_questions_count()]
            tests_table.insert(parent='', index=END, iid=i, text='',
                               values=values)

        tests_table.place(x=60, y=120)

        auth_label = tkinter.Label(text=self.auth_user.get_full_name(),
                                   background=MAIN_COLOR)
        auth_label.place(x=650, y=30)

        def on_start():
            if not tests_table.selection():
                messagebox.showerror('Ошибка', 'Выберите тест!')
                return

            test_index = int(tests_table.selection()[0])
            self.start_test(test_index)

        start_button = tkinter.Button(text='Начать тест',
                                      command=on_start)
        start_button.place(x=640, y=560)

        self.widgets.append(label)
        self.widgets.append(back_to_main_button)
        self.widgets.append(tests_table)
        self.widgets.append(auth_label)
        self.widgets.append(start_button)

    def show_main_form(self):
        # Показать главное меню
        self.clear_widgets()

        logo_name = 'logo2.png'
        logo_path = os.path.join(os.path.dirname(__file__), logo_name)
        img = Image.open(logo_path)
        img = img.resize((200, 200))
        image = ImageTk.PhotoImage(img)

        label = tkinter.Label(image=image, background=MAIN_COLOR)
        label.image = image
        label.place(x=270, y=20)
        """ lessons_button = tkinter.Button(text='Теория',
                                        width=20,
                                        height=2,
                                        background='white',
                                        command=self.show_lessons)
        lessons_button.place(x=100, y=200)
        practice_button = tkinter.Button(text='Практика',
                                         width=20,
                                         height=2,
                                         background='white',
                                         command=self.show_practics)
        practice_button.place(x=300, y=200)
        tests_button = tkinter.Button(text='Тесты',
                                      width=20,
                                      height=2,
                                      background='white',
                                      command=self.student_auth)
        tests_button.place(x=500, y=200) """

        info_label = HTMLLabel(html=self.title_html,
                               background=MAIN_COLOR,
                               foreground=MAIN_COLOR)
        info_label.place(x=140, y=230)

        info_label2 = HTMLLabel(html='<b>Троицк, 2022</b>',
                                background=MAIN_COLOR)
        info_label2.place(x=340, y=520)
        
        info_label2.config(fontsize='50')

        self.widgets.append(label)
        # self.widgets.append(lessons_button)
        # self.widgets.append(practice_button)
        # self.widgets.append(tests_button)
        self.widgets.append(info_label)
        self.widgets.append(info_label2)


def main():
    root = tkinter.Tk()
    app = Window(root)
    app.show_main_form()
    root.mainloop()


if __name__ == "__main__":
    main()
