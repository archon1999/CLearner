from django.contrib import admin

from .models import (Group, Lesson, Practice, Question, Student, Test,
                     TestQuestion, QuestionOption, TestPassResult)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'group', 'date_of_birth']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_number', 'department', 'get_students_count']


class QuestionOptionAdminInline(admin.TabularInline):
    model = QuestionOption
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    inlines = [QuestionOptionAdminInline]


class TestQuestionAdminInline(admin.TabularInline):
    model = TestQuestion
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration']
    inlines = [TestQuestionAdminInline]


@admin.register(TestPassResult)
class TestPassResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test', 'solved', 'created']
    list_filter = ['test']
