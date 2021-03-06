# Generated by Django 4.0.4 on 2022-05-30 15:29

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_testquestionresult_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='lesson',
            managers=[
                ('lessons', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='practice',
            managers=[
                ('practics', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(1, 'Вопрос с выбором ответа'), (2, 'Вопрос с вводом ответа'), (3, 'Вопрос на соотвествие'), (4, 'Вопрос на упорядочение'), (5, 'Вопрос на классификацию')]),
        ),
        migrations.AlterField(
            model_name='questionoption',
            name='option_secondary',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительный вариант'),
        ),
        migrations.AlterField(
            model_name='test',
            name='duration',
            field=models.DurationField(verbose_name='Длительность'),
        ),
        migrations.AlterField(
            model_name='test',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
