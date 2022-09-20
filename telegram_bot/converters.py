from exceptions import IncorrectValueError


def stats_converter(data: 'str', stat_type: 'str') -> list:
    if not data.strip():
        raise IncorrectValueError
    data = data.replace(',', '.').split()
    nums = []
    for num in data:
        try:
            nums.append(float(num))
        except ValueError:
            continue
    if stat_type == 'pressure':
        if len(nums) == 2:
            return sorted(nums)
        else:
            raise IncorrectValueError
    if len(nums) == 1:
        return nums
    else:
        raise IncorrectValueError
