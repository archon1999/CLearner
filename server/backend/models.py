"""В этом файле описаны модели для представления таблиц базы данных"""

from django.db import models
from django.contrib import admin
from django.utils import timezone
from ckeditor.fields import RichTextField


# Класс для описания таблица "Теория"
class Lesson(models.Model):
    # Атрибуты
    lessons = models.Manager()
    title = models.CharField(max_length=255, verbose_name='Название')
    text = RichTextField(verbose_name='Текст')
    example = RichTextField(verbose_name='Пример')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def get_full_text(self):
        text = '<h3>' + self.title + '</h3><br><br>'
        text += self.text
        text += '<br><br>'
        return text

    def __str__(self):
        return self.title


# Класс для описания таблица "Практика"
class Practice(models.Model):
    practics = models.Manager()
    title = models.CharField(max_length=255, verbose_name='Название')
    text = RichTextField(verbose_name='Текст')
    example = RichTextField(verbose_name='Пример решение задачи')

    def get_full_text(self):
        text = '<h3>' + self.title + '</h3><br><br>'
        text += self.text
        text += '<br><br>'
        text += '<h4>Пример: </h4><br>'
        text += self.example + '<br><br>'
        return text

    class Meta:
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'

    def __str__(self):
        return self.title


class Group(models.Model):
    department = models.CharField(max_length=255, verbose_name='Отделение')
    course_number = models.IntegerField(verbose_name='Номер курса')

    @admin.display(description='Количество студентов')
    def get_students_count(self):
        return self.students.count()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.department + f'({self.course_number})'


class Student(models.Model):
    students = models.Manager()
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='students')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return self.get_full_name()


def question_image_directory_path(instance, filename):
    return f'backend/tests/{instance.id}.jpg'


class Question(models.Model):
    class Type(models.IntegerChoices):
        ANSWER_CHOICE = 1, 'Вопрос с выбором ответа'
        ANSWER_INPUT = 2, 'Вопрос с вводом ответа'
        CONFORMITY = 3, 'Вопрос на соотвествие'
        STREAMLING = 4, 'Вопрос на упорядочение'
        CLASSIFICATION = 5, 'Вопрос на классификацию'

    questions = models.Manager()
    type = models.IntegerField(choices=Type.choices)
    text = RichTextField(verbose_name='Текст')
    image = models.ImageField(
        upload_to=question_image_directory_path,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return str(self.id)


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='options')
    option_main = models.CharField(max_length=255, verbose_name='Вариант')
    option_secondary = models.CharField(max_length=255,
                                        verbose_name='Дополнительный вариант',
                                        null=True,
                                        blank=True)
    is_answer = models.BooleanField(verbose_name='Является ли ответом?')

    class Meta:
        verbose_name = 'Вариант вопроса'
        verbose_name_plural = 'Варианты вопроса'

    def __str__(self):
        return str(self.question) + f'({self.option_main})'


class Test(models.Model):
    tests = models.Manager()
    title = models.CharField(max_length=255, verbose_name='Название')
    duration = models.DurationField(verbose_name='Длительность')

    def get_questions_count(self):
        return self.questions.all().count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestQuestion(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы теста'
        ordering = ['test__id']

    def __str__(self):
        return f'{self.test} - {self.question.text}'


class TestPassResult(models.Model):
    results = models.Manager()
    test = models.ForeignKey(
        Test,
        verbose_name='Тест',
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    student = models.ForeignKey(
        Student,
        verbose_name='Студент',
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    solved = models.IntegerField(default=0,
                                 verbose_name='Решено')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата прохождения')

    class Meta:
        verbose_name = 'Результат прохождение теста'
        verbose_name_plural = 'Результаты прохождение теста'

    @property
    def remaining_time(self):
        passed_seconds = int((timezone.now() - self.created).total_seconds())
        duration = self.test.duration
        seconds = duration.seconds
        remaining_seconds = seconds - passed_seconds
        return remaining_seconds

    @property
    def finished(self):
        return self.remaining_time <= 0

    def __str__(self):
        return f'{self.student} - {self.test} ({self.solved})'


class TestQuestionResult(models.Model):
    test_result = models.ForeignKey(
        TestPassResult,
        on_delete=models.CASCADE,
        related_name='test_question_results',
    )
    test_question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Результат одного вопроса теста'
        verbose_name_plural = 'Результаты одного вопроса теста'
