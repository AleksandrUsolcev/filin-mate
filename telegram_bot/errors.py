import exceptions as exc

API_ERRORS = {
    'user_not_found': exc.UserNotFoundError,
    'stat_type_not_found': exc.StatTypeNotFoundError,
    'stat_incorrect_value': exc.IncorrectValueError
}
