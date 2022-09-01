from core.models import StatsBaseModel
from django.db import models
from users.models import Patient


class Stat(StatsBaseModel):
    """Показатели здоровья"""
    TYPES = (
        ('pulse', 'Пульс'),
        ('upper', 'Верхнее давление'),
        ('lower', 'Нижнее давление'),
        ('saturation', 'Сатурация'),
        ('sugar', 'Сахар в крови (ммоль)'),
        ('heat', 'Температура тела'),
        ('weight', 'Вес (кг)'),
        ('height', 'Рост (см)'),
        ('sleep', 'Время сна'),
    )

    patient = models.ForeignKey(
        Patient,
        verbose_name='stats',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        verbose_name='Показатель',
        choices=TYPES,
        max_length=20,
    )
    data = models.FloatField()

    def __str__(self):
        return f'{self.data}'


class Location(StatsBaseModel):
    """Местоположение"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='locations',
        on_delete=models.CASCADE
    )
    latitude = models.FloatField(
        verbose_name='Широта'
    )
    longitude = models.FloatField(
        verbose_name='Долгота'
    )

    def __str__(self):
        return f'{self.latitude}, {self.longitude}'


class Weather(StatsBaseModel):
    """Погода"""
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.CASCADE
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

    def __str__(self):
        return f'{self.temp} C, {self.pressure} р/с, {self.humidity}%'
