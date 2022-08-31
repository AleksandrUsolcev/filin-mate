from core.models import StatsBaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import Patient


class Pressure(StatsBaseModel):
    """Давление"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='pressures',
        on_delete=models.CASCADE
    )
    lower = models.PositiveIntegerField(
        verbose_name='Нижнее',
        validators=[
            MinValueValidator(30),
            MaxValueValidator(250)
        ]
    )
    upper = models.PositiveIntegerField(
        verbose_name='Верхнее',
        validators=[
            MinValueValidator(30),
            MaxValueValidator(250)
        ]
    )

    def __str__(self):
        return f'{self.upper} на {self.lower}'


class Pulse(StatsBaseModel):
    """Пульс"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='pulses',
        on_delete=models.CASCADE
    )
    data = models.PositiveIntegerField(
        verbose_name='Показатель пульса',
        validators=[
            MinValueValidator(20),
            MaxValueValidator(300)
        ]
    )

    def __str__(self):
        return f'{self.data} уд/м'


class Saturation(StatsBaseModel):
    """Сатурация"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='saturations',
        on_delete=models.CASCADE
    )
    data = models.PositiveIntegerField(
        verbose_name='Показатель сатурации',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    def __str__(self):
        return f'{self.data}'


class BloodSugar(StatsBaseModel):
    """Сахар в крови"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='sugars',
        on_delete=models.CASCADE
    )
    data = models.FloatField(
        verbose_name='Ммоль',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(70)
        ]
    )

    def __str__(self):
        return f'{self.data} ммоль'


class BodyHeat(StatsBaseModel):
    """Температура тела"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='heats',
        on_delete=models.CASCADE
    )
    data = models.FloatField(
        verbose_name='Температура по Цельсию',
        validators=[
            MinValueValidator(33),
            MaxValueValidator(43)
        ]
    )

    def __str__(self):
        return f'{self.data} C'


class Weight(StatsBaseModel):
    """Вес"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='weights',
        on_delete=models.CASCADE
    )
    data = models.FloatField(
        verbose_name='Вес (кг)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(600)
        ]
    )

    def __str__(self):
        return f'{self.data} кг'


class Height(StatsBaseModel):
    """Рост"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='heights',
        on_delete=models.CASCADE
    )
    data = models.PositiveIntegerField(
        verbose_name='Рост (см)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(260)
        ]
    )

    def __str__(self):
        return f'{self.data} см'


class SleepTime(StatsBaseModel):
    """Время сна"""
    patient = models.ForeignKey(
        Patient,
        verbose_name='sleeps',
        on_delete=models.CASCADE
    )
    data = models.FloatField(
        verbose_name='Время сна (час)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24)
        ]
    )

    def __str__(self):
        return f'{self.data} ч.'


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


class Weather(models.Model):
    """Погода"""
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
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
