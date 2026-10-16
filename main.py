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


