from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = 'Пользователя с такими данными не существует'


class InvalidPasswordException(APIException):
    status_code = 400
    default_detail = 'Неверный пароль'


class TokenPermissionException(APIException):
    status_code = 403
    default_detail = 'У данного пользователя нет прав для получения токена'


class MissingPatientParamException(APIException):
    status_code = 400
    default_detail = 'Не указан обязательный параметр patient__telegram'


class MissingTypeParamException(APIException):
    status_code = 400
    default_detail = 'Не указан обязательный параметр type'


class WrongTypeParamException(APIException):
    status_code = 400
    default_detail = 'Некорректный тип показателя здоровья'


class WrongDataValueException(APIException):
    status_code = 400
    default_detail = 'Некорректное значение'
