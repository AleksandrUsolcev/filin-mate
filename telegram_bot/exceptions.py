class TimeDifferenceError(Exception):
    """Ограничение по времени добавления элементов"""
    pass


class UserNotFoundError(Exception):
    """Указанного пользователя не существует"""
    pass


class StatTypeNotFoundError(Exception):
    """Указанного типа показателя здоровья не существует"""
    pass


class IncorrectValueError(Exception):
    """Некорректное значение данных"""
    pass
