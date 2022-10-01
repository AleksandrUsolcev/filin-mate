from aiogram.utils.helper import Helper, HelperMode, ListItem


class StatStates(Helper):
    mode = HelperMode.snake_case

    PULSE = ListItem()
    SATURATION = ListItem()
    PRESSURE = ListItem()
    SUGAR = ListItem()
    HEAT = ListItem()
    SLEEP = ListItem()
    WEIGHT = ListItem()
    HEIGHT = ListItem()
    HEALTH = ListItem()
    MENTAL = ListItem()
