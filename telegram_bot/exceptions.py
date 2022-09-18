from settings import DIFF_TIME


class TimeDifferenceError(Exception):

    def __str__(self):
        error = ('Нельзя так часто добавлять показания.\n'
                 f'Подождите {DIFF_TIME} мин или измените предыдущий '
                 'добавленный показатель, если ошиблись.')
        return error


class UserNotFoundError(Exception):

    def __str__(self):
        error = ('Указанный пользователь отсутствует в базе.')
        return error


class StatTypeNotFoundError(Exception):

    def __str__(self):
        error = ('Указанный тип показателя здоровья отсутствует в базе.')
        return error


class IncorrectValueError(Exception):

    def __str__(self):
        error = ('Некорректные данные, попробуйте снова.')
        return error
