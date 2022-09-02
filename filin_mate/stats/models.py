from core.models import StatsBaseModel
from django.core.exceptions import ValidationError
from django.db import models
from users.models import Patient


class Stat(StatsBaseModel):
    """Показатели здоровья"""
    class StatsTypes(models.TextChoices):
        pulse = 'pulse', 'Пульс'
        upper = 'upper', 'Верхнее давление'
        lower = 'lower', 'Нижнее давление'
        saturation = 'saturation', 'Сатурация'
        sugar = 'sugar', 'Сахар в крови (ммоль)'
        heat = 'heat', 'Температура тела'
        weight = 'weight', 'Вес (кг)'
        height = 'height', 'Рост (см)'
        sleep = 'sleep', 'Время сна'

    validators = {
        'pulse': ['Некорректное значение пульса', 30, 300],
        'upper': ['Некорректное значение давления', 20, 300],
        'lower': ['Некорректное значение давления', 20, 300],
        'saturation': ['Некорректное значение сатурации', 1, 100],
        'sugar': ['Некорректное значение сахара в крови', 0, 70],
        'heat': ['Некорректное значение температуры тела', 31, 44],
        'weight': ['Некорректное значение веса', 2, 450],
        'height': ['Некорректное значение роста', 40, 260],
        'sleep': ['Некорректное значение времени сна', 1, 24],
    }

    patient = models.ForeignKey(
        Patient,
        related_name='stats',
        verbose_name='Пациент',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        verbose_name='Тип',
        choices=StatsTypes.choices,
        max_length=20,
    )
    data = models.FloatField(
        verbose_name='Показатель'
    )

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

    def __str__(self):
        return f'{self.data}'

    def save(self, *args, **kwargs):
        val = self.validators
        stat = self.data
        if self.type in val.keys():
            if (stat < val[self.type][1] or stat > val[self.type][2]):
                raise ValidationError(val[self.type][0])
        super().save(*args, **kwargs)


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
