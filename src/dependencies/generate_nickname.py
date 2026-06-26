from random import choices
from string import ascii_uppercase, digits


async def generate_nickname() -> str:

    prefix = "Пришелец-"
    words = choices(ascii_uppercase, k=4)
    numbers = choices(digits, k=7)
    nickname = prefix + "".join(words) + "".join(numbers)

    return nickname
