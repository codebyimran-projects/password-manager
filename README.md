
# Password Manager and Generator

A Python-based password management application built with Streamlit. Generate strong passwords, save account credentials, view saved passwords, search accounts, update existing credentials, and delete accounts through a simple web interface.

## Features

- **Password Generator** — Generate random passwords up to 128 characters.
- **Custom Passwords** — Choose uppercase letters, lowercase letters, numbers, and symbols.
- **Save Passwords** — Store website names, usernames, emails, and passwords.
- **View Passwords** — View saved account details with masked passwords.
- **Search Accounts** — Find saved accounts by website name.
- **Update Accounts** — Update usernames and passwords.
- **Delete Accounts** — Delete accounts with confirmation.
- **Persistent Storage** — Save account data in a JSON file.
- **Streamlit Interface** — Manage accounts through a browser-based UI.

## Technologies Used

- Python
- Streamlit
- JSON
- `secrets` — Secure random password generation
- `string` — Character sets for password generation
- `pathlib` — File path handling

## Project Structure

```text
password-manager/
├── app.py
├── passwords.json
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/codebyimran-projects/password-manager.git
```

### 2. Open the Project Folder

```bash
cd password-manager
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## How to Use

1. Open the Dashboard to see your saved account count.
2. Navigate to **Generate Password** to create a custom password.
3. Open **Save Password** to store a website, username, and password.
4. Use **View Passwords** to browse or search saved accounts.
5. Open **Update Password** to modify existing account details.
6. Use **Delete Password** to remove an account after confirmation.

## Password Generation

The password generator supports:

- Uppercase letters: `A-Z`
- Lowercase letters: `a-z`
- Numbers: `0-9`
- Symbols: `!@#$%^&*`

Choose the desired length and character types to generate a password.

## Learning Objectives

This project demonstrates practical Python programming concepts:

- Functions and conditional statements
- Loops and dictionaries
- JSON file handling
- Exception handling
- Password generation with Python's `secrets` module
- Streamlit UI development
- Creating, reading, updating, and deleting records (CRUD operations)

## Security Notice

**This project is for educational purposes.**

The current version stores saved passwords in plain text in `passwords.json`. Masking a password in the interface does not encrypt the stored data.

Do not use this version to store real credentials. Encryption and master-password authentication should be implemented before using it as a real password manager.

## Future Improvements

- Master password authentication
- Encrypted password storage
- Password strength checker
- Copy-to-clipboard functionality
- Improved account search and filtering
- Secure backup and restore
- Password visibility toggle

## Author

**Muhammad Imran**

- Website: [codebyimran.com](https://codebyimran.com)


---


