from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager,  Group, Permission)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=60, unique=True,
    )
    ROLE_CHOICES = [
        ('OPERATOR', 'Оператор'),
        ('BRIGADE', 'Бригада'),
        ('CLIENT', 'Клиент'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Operator(AbstractUser):
    operator = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='operator_profile')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    groups = models.ManyToManyField(
        Group, verbose_name='Группы', related_name='operator_profiles'
    )
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='Права доступа',
        related_name='operator_profiles'
    )

    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'

    def __str__(self):
        return self.full_name


class Brigade(AbstractUser):
    name = models.CharField(
        max_length=255, unique=True, verbose_name='Название бригады')
    members = models.CharField(
        max_length=255, verbose_name='Список участников бригады')
    groups = models.ManyToManyField(
        Group, verbose_name='Группы', related_name='brigade_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='Права доступа',
        related_name='brigade_user_permissions'
    )

    class Meta:
        verbose_name = 'Бригада'
        verbose_name_plural = 'Бригады'

    def __str__(self):
        return self.name


class Client(AbstractUser):
    company_name = models.CharField(
        max_length=100, verbose_name='Название компании')
    address = models.CharField(max_length=150, verbose_name='Адрес компании')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='client_profile')
    groups = models.ManyToManyField(
        Group, verbose_name='Группы', related_name='client_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='Права доступа',
        related_name='client_user_permissions'
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.company_name
