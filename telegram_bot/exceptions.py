from settings import DIFF_TIME


class TimeDifferenceError(Exception):

    def __init__(self):
        self.message = ('Нельзя так часто добавлять показатели.\n'
                        f'Подождите {DIFF_TIME} мин или если ошиблись '
                        'измените предыдущий добавленный показатель ')

    def __str__(self):
        error = 'Попытка добавить показатель до истечения кулдауна'
        return error


class UserNotFoundError(Exception):

    def __init__(self):
        self.message = 'Указанный пользователь отсутствует в базе'

    def __str__(self):
        error = 'Отсутствие пользователя в базе'
        return error


class StatTypeNotFoundError(Exception):

    def __init__(self):
        self.message = 'Указанный тип показателя здоровья отсутствует в базе'

    def __str__(self):
        error = 'Отсутствие показателя здоровья'
        return error


class IncorrectValueError(Exception):

    def __init__(self):
        self.message = ('Некорректные данные, попробуйте снова, выбрав {stat} '
                        'или добавьте другие показатели')

    def __str__(self):
        error = 'Некорректные входные данные'
        return error
