# Generated by Django 4.2.1 on 2023-05-15 10:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=155, verbose_name='Наш адрес')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^[0-9()+]+$', 'Enter a valid phone number.')], verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Наш email')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=70, verbose_name='Адрес')),
                ('time', models.CharField(max_length=70, verbose_name='Часы работы')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^[0-9()+]+$', 'Enter a valid phone number.')], verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Точка приема',
                'verbose_name_plural': 'Точки приема',
            },
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65, verbose_name='Заголовок')),
                ('image', models.ImageField(upload_to='articles/%Y/%m/%d/', verbose_name='Изображение')),
                ('description', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Правила сортировки',
                'verbose_name_plural': 'Правила сортировки',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Секция деятельности',
                'verbose_name_plural': 'Секция деятельности',
            },
        ),
    ]
