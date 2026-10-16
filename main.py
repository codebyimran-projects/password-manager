import random
import string



password = {}

try:
    with open("passwords.txt", "r") as file:
        for line in file:
            key, value = line.strip().split(":")
            password[key] = value
except FileNotFoundError:
    pass


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


while True:
    print("1. Generate a new password")
    print("2. View saved passwords")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        length = int(input("Enter the desired password length: "))
        new_password = generate_password(length)
        print(f"Generated password: {new_password}")
        save_choice = input("Do you want to save this password? (y/n): ")
        if save_choice.lower() == 'y':
            key = input("Enter a name for this password: ")
            password[key] = new_password
            with open("passwords.txt", "w") as file:
                for k, v in password.items():
                    file.write(f"{k}:{v}\n")
            print("Password saved successfully.")
    elif choice == "2":
        if not password:
            print("No saved passwords.")
        else:
            for key, value in password.items():
                print(f"{key}: {value}")
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")