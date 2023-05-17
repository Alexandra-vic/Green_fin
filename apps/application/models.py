from django.db import models
from django.core.validators import RegexValidator


TYPE_CHOICES = (
    ("Установка экобокса", "Установка экобокса"),
    ("Вывоз мусора", "Вывоз мусора"),
    ("Демонтаж экобокс", "Демонтаж экобокс"),
)


STATUS_CHOICES = (
    ("Не начато", "Не начато"),
    ("В процессе", "В процессе"),
    ("Завершено", "Завершено"),
)


class Application(models.Model):
    type = models.CharField(
        max_length=25, choices=TYPE_CHOICES,
        default=None, verbose_name='Тип работ',
    )
    comment = models.TextField(
        verbose_name='Комментарий', blank=True, null=True,
    )
    address = models.CharField(
        max_length=125, verbose_name='Ваш адрес',
    )
    date = models.CharField(
        max_length=70, verbose_name='Время выполения работ'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default="Не начато", verbose_name='Статус',
    )
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата'
    )

    def __str__(self):
        return f'{self.type} {self.status}'
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Team(models.Model):
    name = models.CharField(
        max_length=65, verbose_name='Название бригады'
    )
    phone = models.CharField(
        max_length=15, validators=[RegexValidator(r'^[0-9()+]+$', 'Enter a valid phone number.')],
        verbose_name='Номер телефона',
    )
    quantity = models.IntegerField(verbose_name='Количество сотрудников')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Бригада'
        verbose_name_plural = 'Бригады'
