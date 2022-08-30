# Generated by Django 4.1 on 2022-08-30 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Электронная почта"
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Администратор"),
                            ("editor", "Редактор"),
                            ("user", "Пользователь"),
                        ],
                        default="user",
                        max_length=10,
                        verbose_name="Роль",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=80, verbose_name="Имя"),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, max_length=80, verbose_name="Отчество"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=80, verbose_name="Фамилия"),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Номер телефона"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Администрация"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активен"),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата регистрации",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Все пользователи",
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "telegram",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="telegram id"
                    ),
                ),
                (
                    "age",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата рождения"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пациент",
                "verbose_name_plural": "Пациенты",
            },
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "patients",
                    models.ManyToManyField(
                        blank=True,
                        related_name="doctors",
                        to="users.patient",
                        verbose_name="Пациенты",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Врач",
                "verbose_name_plural": "Врачи",
            },
        ),
    ]
