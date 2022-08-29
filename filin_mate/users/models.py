from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь"""

    ADMIN = 'admin'
    EDITOR = 'editor'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (EDITOR, 'Редактор'),
        (USER, 'Пользователь'),
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        max_length=10,
        default='user'
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

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_editor(self):
        return self.role == self.EDITOR

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Все пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)


class Doctor(models.Model):
    """Врач"""

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    # and experience, education, position fields

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.user.email


class Patient(models.Model):
    """Пациент"""

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    doctors = models.ManyToManyField(
        Doctor,
        blank=True,
        verbose_name='Лечащие врачи',
        related_name='patients'
    )
    age = models.DateField(
        verbose_name='Дата рождения'
    )

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    def __str__(self):
        return self.user.email
