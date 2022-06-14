# Generated by Django 4.0.4 on 2022-05-27 12:01

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_questionoption_testpassresult_remove_test_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestQuestionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.questionoption')),
            ],
            options={
                'verbose_name': 'Результат одного вопроса теста',
                'verbose_name_plural': 'Результаты одного вопроса теста',
            },
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.AlterModelOptions(
            name='testpassresult',
            options={'verbose_name': 'Результат прохождение теста', 'verbose_name_plural': 'Результаты прохождение теста'},
        ),
        migrations.AlterModelOptions(
            name='testquestion',
            options={'ordering': ['test__id'], 'verbose_name': 'Вопрос теста', 'verbose_name_plural': 'Вопросы теста'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
        migrations.RemoveField(
            model_name='test',
            name='questions_count',
        ),
        migrations.AddField(
            model_name='lesson',
            name='example',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Пример'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='test',
            name='duration',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='testpassresult',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results', to='backend.test'),
        ),
        migrations.DeleteModel(
            name='TestPassResultOne',
        ),
        migrations.AddField(
            model_name='testquestionresult',
            name='test_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.testquestion'),
        ),
        migrations.AddField(
            model_name='testquestionresult',
            name='test_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_question_results', to='backend.testpassresult'),
        ),
    ]
