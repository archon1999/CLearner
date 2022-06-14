# Generated by Django 4.0.4 on 2022-05-26 11:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonchapter',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='lessonchapter',
            name='lesson',
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'Тест', 'verbose_name_plural': 'Тесты'},
        ),
        migrations.AddField(
            model_name='lesson',
            name='text',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Текст'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Chapter',
        ),
        migrations.DeleteModel(
            name='LessonChapter',
        ),
    ]