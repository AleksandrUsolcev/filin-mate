# Generated by Django 4.1 on 2022-09-01 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Location",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                ("latitude", models.FloatField(verbose_name="Широта")),
                ("longitude", models.FloatField(verbose_name="Долгота")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Stat",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("pulse", "Пульс"),
                            ("upper", "Верхнее давление"),
                            ("lower", "Нижнее давление"),
                            ("saturation", "Сатурация"),
                            ("sugar", "Сахар в крови (ммоль)"),
                            ("heat", "Температура тела"),
                            ("weight", "Вес (кг)"),
                            ("height", "Рост (см)"),
                            ("sleep", "Время сна"),
                        ],
                        max_length=20,
                        verbose_name="Показатель",
                    ),
                ),
                ("data", models.FloatField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Weather",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                ("temp", models.FloatField(verbose_name="Температура по Цельсию")),
                (
                    "pressure",
                    models.PositiveIntegerField(verbose_name="Атмосферное давление"),
                ),
                (
                    "humidity",
                    models.PositiveBigIntegerField(verbose_name="Влажность воздуха %"),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stats.location",
                        verbose_name="Местоположение",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
