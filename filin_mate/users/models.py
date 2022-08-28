from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        blank=True,
        max_length=80
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        blank=True,
        max_length=80
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=True,
        max_length=80
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        blank=True,
        max_length=20
    )
    is_staff = models.BooleanField(
        verbose_name='Администрация',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )
    created = models.DateTimeField(
        verbose_name='Дата регистрации',
        default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
