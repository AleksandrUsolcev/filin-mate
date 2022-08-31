from rest_framework.exceptions import APIException
from stats import models as stats

from . import serializers as srl

STATS_TYPES = {
    'pulse': [stats.Pulse, srl.PulseSerializer],
    'saturation': [stats.Saturation, srl.SaturationSerializer],
    'pressure': [stats.Pressure, srl.PressureSerializer],
    'sugar': [stats.BloodSugar, srl.BloodSugarSerializer],
    'heat': [stats.BodyHeat, srl.BodyHeatSerializer],
    'weight': [stats.Weight, srl.WeightSerializer],
    'height': [stats.Height, srl.HeightSerializer],
    'sleep': [stats.SleepTime, srl.SleepTimeSerializer],
    'location': [stats.Location, srl.LocationSerializer],
}


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = 'Пользователя с такими данными не существует'


class InvalidPasswordException(APIException):
    status_code = 400
    default_detail = 'Неверный пароль'


class TokenPermissionException(APIException):
    status_code = 403
    default_detail = 'У данного пользователя нет прав для получения токена'


class MissingUserParamException(APIException):
    status_code = 400
    default_detail = 'Не указан обязательный параметр user'


class MissingTypeParamException(APIException):
    status_code = 400
    default_detail = 'Не указан обязательный параметр type'


class WrongTypeParamException(APIException):
    status_code = 400
    default_detail = ('Неверное значение параметра type. Выберите один из '
                      'параметров: ' + ', '.join(list(STATS_TYPES.keys())))
