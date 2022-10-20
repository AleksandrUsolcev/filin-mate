from email.policy import default
from api import exceptions as exc
from core.models import StatsBaseModel
from django.db import models
from users.models import Patient


class StatType(StatsBaseModel):
    """Типы показателей"""

    FLOAT = 'float'
    INT = 'int'

    TYPES = (
        (FLOAT, 'Число с плавающей точкой'),
        (INT, 'Целое число'),
    )

    slug = models.SlugField(
        verbose_name='Уникальное название',
        max_length=32,
        unique=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=120
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=512,
        blank=True,
        null=True
    )
    data_type = models.CharField(
        verbose_name='Тип данных',
        choices=TYPES,
        max_length=10,
        default=FLOAT
    )
    min_value = models.FloatField(
        verbose_name='Минимальное значение'
    )
    max_value = models.FloatField(
        verbose_name='Максимальное значение'
    )
    important = models.BooleanField(
        verbose_name='Важное значение',
        default=False,
        blank=True
    )

    class Meta:
        verbose_name = 'Тип данных'
        verbose_name_plural = 'Типы данных'

    def __str__(self):
        return f'{self.name}'


class Stat(StatsBaseModel):
    """Показатели здоровья"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='Пациент',
        related_name='stats',
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        StatType,
        related_name='values',
        verbose_name='Тип',
        on_delete=models.CASCADE
    )
    data = models.FloatField(
        verbose_name='Показатель'
    )

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

    def __str__(self):
        return f'{self.type}: {self.data}'

    def save(self, *args, **kwargs):
        stat = self.data
        min_value = self.type.min_value
        max_value = self.type.max_value
        if (stat < min_value or stat > max_value):
            raise exc.StatIncorrectValueException
        super().save(*args, **kwargs)


class Note(StatsBaseModel):
    """Заметки"""
    patient = models.ForeignKey(
        Patient,
        related_name='notes',
        verbose_name='Пациент',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=512
    )

    class Meta:
        verbose_name = 'Заметки'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return f'{self.text[:24]}'


class Location(StatsBaseModel):
    """Местоположение"""
    patient = models.ForeignKey(
        Patient,
        related_name='locations',
        verbose_name='Пациент',
        on_delete=models.CASCADE
    )
    latitude = models.FloatField(
        verbose_name='Широта'
    )
    longitude = models.FloatField(
        verbose_name='Долгота'
    )

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположение'

    def __str__(self):
        return f'{self.latitude}, {self.longitude}'


class Weather(StatsBaseModel):
    """Погода"""
    # IN FUTURE
    # location = models.ForeignKey(
    #     Location,
    #     verbose_name='Местоположение',
    #     related_name='weathers',
    #     on_delete=models.CASCADE
    # )
    code = models.IntegerField(
        verbose_name='Вид осадков'
    )
    temp = models.FloatField(
        verbose_name='Температура по Цельсию'
    )
    pressure = models.PositiveIntegerField(
        verbose_name='Атмосферное давление'
    )
    humidity = models.PositiveBigIntegerField(
        verbose_name='Влажность воздуха %'
    )

    class Meta:
        verbose_name = 'Погода'
        verbose_name_plural = 'Погода'

    def __str__(self):
        return f'{self.temp} C, {self.pressure} р/с, {self.humidity}%'
