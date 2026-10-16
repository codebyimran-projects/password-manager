import random
import string



password = {}

try:
    with open("passwords.json", "r") as file:
        for line in file:
            key, value = line.strip().split(":")
            password[key] = value
except FileNotFoundError:
    pass


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


