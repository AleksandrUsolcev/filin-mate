from exceptions import IncorrectValueError


def stats_converter(data: 'str', stat_type: 'str') -> list:
    if not data.strip():
        print('строка пустая')
    data = data.split()
    data = [float(num) for num in data if num.isdigit()]
    if stat_type == 'pressure':
        if len(data) == 2:
            return sorted(data)
        else:
            raise IncorrectValueError
    if len(data) == 1:
        return data
    else:
        raise IncorrectValueError
