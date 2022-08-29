from django.db import models
from core.models import StatsBaseModel


class Pressure(StatsBaseModel):
    """Давление"""
    lower = models.PositiveIntegerField(
        verbose_name='Нижнее',
    )
    upper = models.PositiveIntegerField(
        verbose_name='Верхнее',
    )

    def __str__(self):
        return f'{self.upper} на {self.lower}'


class Pulse(StatsBaseModel):
    """Пульс"""
    data = models.PositiveIntegerField(
        verbose_name='Показатель пульса',
    )

    def __str__(self):
        return f'{self.data} уд/м'


class Saturation(StatsBaseModel):
    """Сатурация"""
    data = models.PositiveIntegerField(
        verbose_name='Показатель сатурации',
    )

    def __str__(self):
        return f'{self.data}'


class BloodSugar(StatsBaseModel):
    """Сахар в крови"""
    data = models.FloatField(
        verbose_name='Ммоль',
    )

    def __str__(self):
        return f'{self.data} ммоль'


class BodyHeat(StatsBaseModel):
    """Температура тела"""
    data = models.FloatField(
        verbose_name='Температура по Цельсию',
    )

    def __str__(self):
        return f'{self.data} C'


class Weight(StatsBaseModel):
    """Вес"""
    data = models.FloatField(
        verbose_name='Вес (кг)',
    )

    def __str__(self):
        return f'{self.data} кг'


class Height(StatsBaseModel):
    """Рост"""
    data = models.PositiveIntegerField(
        verbose_name='Рост (см)'
    )

    def __str__(self):
        return f'{self.data} см'


class SleepTime(StatsBaseModel):
    """Время сна"""
    data = models.FloatField(
        verbose_name='Время сна (час)'
    )

    def __str__(self):
        return f'{self.data} ч.'


class Location(StatsBaseModel):
    """Местоположение"""
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
