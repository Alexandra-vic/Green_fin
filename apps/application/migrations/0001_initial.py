# Generated by Django 4.2.1 on 2023-05-22 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Установка экобокса', 'Установка экобокса'), ('Вывоз мусора', 'Вывоз мусора'), ('Демонтаж экобокса', 'Демонтаж экобокса')], default=None, max_length=25, verbose_name='Тип работ')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('address', models.CharField(max_length=125, verbose_name='Ваш адрес')),
                ('date', models.CharField(max_length=70, verbose_name='Время выполения работ')),
                ('status', models.CharField(choices=[('Не начато', 'Не начато'), ('В процессе', 'В процессе'), ('Завершено', 'Завершено')], default='Не начато', max_length=20, verbose_name='Статус')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
