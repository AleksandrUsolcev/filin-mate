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


class MissingUserParamException(APIException):
    status_code = 400
    default_detail = 'Не указан обязательный параметр user'


class MissingTypeParamException(APIException):
    status_code = 400
    default_detail = 'Не указан обязательный параметр type'
