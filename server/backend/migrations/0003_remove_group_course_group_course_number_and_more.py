# Generated by Django 4.0.4 on 2022-05-26 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_remove_lessonchapter_chapter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='course',
        ),
        migrations.AddField(
            model_name='group',
            name='course_number',
            field=models.IntegerField(default=1, verbose_name='Номер курса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='', max_length=255, verbose_name='Пароль'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(default='', max_length=255, verbose_name='Юзернейм'),
            preserve_default=False,
        ),
    ]
