from django.db import models
from apps.users.models import User


TYPE_CHOICES = (
    ("Установка экобокса", "Установка экобокса"),
    ("Вывоз мусора", "Вывоз мусора"),
    ("Демонтаж экобокса", "Демонтаж экобокса"),
)


STATUS_CHOICES = (
    ("Новая", "Новая"),
    ("В процессе", "В процессе"),
    ("Выполнено", "Выполнено"),
)


class Application(models.Model):
    type = models.CharField(
        max_length=25, choices=TYPE_CHOICES,
        default=None, verbose_name='Тип работ',
    )
    comment = models.TextField(
        verbose_name='Комментарий', blank=True, null=True,
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default="Новая", verbose_name='Статус',
    )
    started_create = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата открытия'
    )
    finished_application = models.DateTimeField(
        auto_now=False, verbose_name='Дата закрытия'
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'CLIENT'}, 
        related_name='applications_as_client',
        verbose_name='Клиент',
    )
    operator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'OPERATOR'},
        related_name='applications_as_operator',
        verbose_name='Оператор', blank=True,
    )
    brigade = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True, 
        limit_choices_to={'user_type': 'BRIGADE'},
        related_name='applications_as_brigade',
        verbose_name='Бригада',
    )
    finished_by_client = models.BooleanField(
        default=False, verbose_name='Отметить как Выпонено клиентом ',
    )
    finished_by_brigade = models.BooleanField(
        default=False, verbose_name='Отметить как Выпонено бригадой ',
    )
    finished_by_operator = models.BooleanField(
        default=False, verbose_name='Отметить как Выпонено оператором ',
    )

    def __str__(self):
        return f'{self.type} {self.status}'
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
