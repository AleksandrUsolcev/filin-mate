from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = {
        'error': 'user_not_found',
        'detail': 'Пользователя с такими данными не существует'
    }


class InvalidPasswordException(APIException):
    status_code = 400
    default_detail = {
        'error': 'invalid_password',
        'detail': 'Неверный пароль'
    }


class TokenPermissionException(APIException):
    status_code = 403
    default_detail = {
        'error': 'token_no_permission',
        'detail': 'У данного пользователя нет прав для получения токена'
    }


class WrongTypeParamException(APIException):
    status_code = 400
    default_detail = {
        'error': 'stat_type_not_found',
        'detail': 'Отсутствует указанный тип показателя здоровья'
    }


class StatIncorrectValueException(APIException):
    status_code = 403
    default_detail = {
        'error': 'stat_incorrect_value',
        'detail': 'Некорректное значение'
    }

# class DataNotFoundException(APIException):
#     status_code = 404
#     default_detail = 'Данные отсутствуют'
