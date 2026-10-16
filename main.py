
import json
import secrets
import string
from pathlib import Path

import streamlit as st


DATA_FILE = Path("passwords.json")


# -------------------- File Handling --------------------

def load_passwords():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, dict) else {}

    except (json.JSONDecodeError, OSError):
        st.error("Could not read the password file.")
        return {}


def save_passwords(passwords):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(passwords, file, indent=4)
        return True
    except OSError:
        st.error("Could not save the password file.")
        return False


# -------------------- Password Generator --------------------

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    character_groups = []

    if use_upper:
        character_groups.append(string.ascii_uppercase)

    if use_lower:
        character_groups.append(string.ascii_lowercase)

    if use_digits:
        character_groups.append(string.digits)

    if use_symbols:
        character_groups.append("!@#$%^&*()-_=+[]{}?")

    if not character_groups:
        return None

    # Include at least one character from each selected group.
    if length < len(character_groups):
        return None

    password_chars = [
        secrets.choice(group) for group in character_groups
    ]

    all_characters = "".join(character_groups)

    password_chars.extend(
        secrets.choice(all_characters)
        for _ in range(length - len(password_chars))
    )

    # Securely shuffle the generated characters.
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


# -------------------- App Setup --------------------

st.set_page_config(
    page_title="Password Manager",
    page_icon="🔐",
    layout="wide"
)

st.title("Password Manager")
st.caption("Generate and manage your saved passwords.")

passwords = load_passwords()

# Initialize session state.
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

if "delete_confirmation" not in st.session_state:
    st.session_state.delete_confirmation = ""


# -------------------- Navigation --------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Generate Password",
        "Save Password",
        "View Passwords",
        "Update Password",
        "Delete Password"
    ]
)

st.sidebar.metric("Saved Accounts", len(passwords))


# -------------------- Dashboard --------------------

if page == "Dashboard":
    st.subheader("Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Saved Accounts", len(passwords))

    with col2:
        st.metric("Password Generator", "Available")

    st.markdown("### Features")
    st.write("- Generate strong passwords")
    st.write("- Save website credentials")
    st.write("- View and search saved accounts")
    st.write("- Update existing credentials")
    st.write("- Delete saved accounts")


# -------------------- Generate Password --------------------

elif page == "Generate Password":
    st.subheader("Generate a Password")

    length = st.slider(
        "Password length",
        min_value=4,
        max_value=128,
        value=16
    )

    st.write("Choose the character types:")

    use_upper = st.checkbox("Uppercase letters (A-Z)", value=True)
    use_lower = st.checkbox("Lowercase letters (a-z)", value=True)
    use_digits = st.checkbox("Numbers (0-9)", value=True)
    use_symbols = st.checkbox("Symbols (!@#$...)", value=True)

    if st.button("Generate Password", type="primary"):
        result = generate_password(
            length,
            use_upper,
            use_lower,
            use_digits,
            use_symbols
        )

        if result is None:
            st.error(
                "Select at least one character type. "
                "The length must also be at least the number "
                "of selected character types."
            )
        else:
            st.session_state.generated_password = result

    if st.session_state.generated_password:
        st.success("Password generated.")

        st.code(st.session_state.generated_password)

        st.download_button(
            "Download Password",
            data=st.session_state.generated_password,
            file_name="generated_password.txt",
            mime="text/plain"
        )

        st.info(
            "To save this password in the manager, copy it "
            "and open the Save Password page."
        )


# -------------------- Save Password --------------------

elif page == "Save Password":
    st.subheader("Save a New Account")

    with st.form("save_password_form"):
        website = st.text_input("Website or account name")
        username = st.text_input("Username or email")
        new_password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button("Save Account")

    if submitted:
        website = website.strip()
        username = username.strip()

        if not website or not username or not new_password:
            st.error("Please fill in all fields.")

        elif website in passwords:
            st.error(
                "This account already exists. "
                "Use Update Password to change its details."
            )

        else:
            passwords[website] = {
                "username": username,
                "password": new_password
            }

            if save_passwords(passwords):
                st.success(f"Account '{website}' saved successfully.")


# -------------------- View Passwords --------------------

elif page == "View Passwords":
    st.subheader("Saved Accounts")

    search = st.text_input("Search by website or account name")

    matching_accounts = {
        website: details
        for website, details in passwords.items()
        if search.lower() in website.lower()
    }

    if not matching_accounts:
        st.info("No matching accounts found.")

    else:
        for website, details in matching_accounts.items():
            with st.expander(website):
                st.write("Username:", details.get("username", ""))

                st.text_input(
                    f"Password for {website}",
                    value=details.get("password", ""),
                    type="password",
                    key=f"view_{website}"
                )


# -------------------- Update Password --------------------

elif page == "Update Password":
    st.subheader("Update an Account")

    if not passwords:
        st.info("No saved accounts to update.")

    else:
        website = st.selectbox(
            "Select an account",
            list(passwords.keys())
        )

        current = passwords[website]

        with st.form("update_password_form"):
            username = st.text_input(
                "Username or email",
                value=current.get("username", "")
            )

            updated_password = st.text_input(
                "New password",
                value=current.get("password", ""),
                type="password"
            )

            update_submitted = st.form_submit_button(
                "Update Account"
            )

        if update_submitted:
            if not username.strip() or not updated_password:
                st.error("Username and password cannot be empty.")

            else:
                passwords[website] = {
                    "username": username.strip(),
                    "password": updated_password
                }

                if save_passwords(passwords):
                    st.success(
                        f"Account '{website}' updated successfully."
                    )


# -------------------- Delete Password --------------------

elif page == "Delete Password":
    st.subheader("Delete an Account")

    if not passwords:
        st.info("No saved accounts to delete.")

    else:
        website = st.selectbox(
            "Select an account to delete",
            list(passwords.keys())
        )

        st.warning(
            f"You are about to delete the account '{website}'."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this account."
        )

        if st.button("Delete Account", type="primary"):
            if not confirm:
                st.error("Please confirm before deleting.")

            else:
                del passwords[website]

                if save_passwords(passwords):
                    st.session_state.delete_confirmation = website
                    st.success(f"Account '{website}' deleted.")
