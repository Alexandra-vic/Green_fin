from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from apps.common.models import AbstractBaseModel


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


class User(AbstractUser, AbstractBaseModel):
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


class Operator(AbstractBaseModel):
    operator = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='operators')
    email = models.EmailField(
        verbose_name='email address',
        max_length=60, unique=True,
    )
    full_name = models.CharField(max_length=200, verbose_name='ФИО')

    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'

    def __str__(self):
        return self.full_name


class Brigade(AbstractBaseModel):
    name = models.CharField(
        max_length=255, unique=True, verbose_name='Название бригады')
    members = models.CharField(
        max_length=255, verbose_name='Список участников бригады')

    class Meta:
        verbose_name = 'Бригада'
        verbose_name_plural = 'Бригады'

    def __str__(self):
        return self.name


class Client(AbstractBaseModel):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=60, unique=True,
    )
    company_name = models.CharField(
        max_length=100, verbose_name='Название компании')
    address = models.CharField(max_length=150, verbose_name='Адрес компании')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='clients')




class PasswordResetRequest(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
