import random
import string


def generate_code(length=8):
    letters_digits = string.ascii_letters + string.digits

    code = ''.join(random.choice(letters_digits) for i in range(length))

    return code
