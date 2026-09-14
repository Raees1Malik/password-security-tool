import tkinter as tk
import os
import string
import secrets
import hashlib
import json
import datetime


#REGISTERS
def register():
    register_window = tk.Toplevel(window)
    register_window.title("Register")
    register_window.geometry("500x500")

    register_title = tk.Label(
        register_window,
        text="Register an account",
        font=("Arial", 18)
    )
    register_title.pack(pady=20)

    username_label = tk.Label(
        register_window,
        text="Username:",
        font=("Arial", 12)
    )
    username_label.pack(pady=5)

    username_entry = tk.Entry(register_window, width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(
        register_window,
        text="Password:",
        font=("Arial", 12)
    )
    password_label.pack(pady=10)

    password_entry = tk.Entry(
        register_window,
        width=30,
        show="*"
    )
    password_entry.pack(pady=5)

    confirm_label = tk.Label(
        register_window,
        text="Confirm Password:",
        font=("Arial", 12)
    )
    confirm_label.pack(pady=10)

    confirm_entry = tk.Entry(
        register_window,
        width=30,
        show="*"
    )
    confirm_entry.pack(pady=5)

    result_label = tk.Label(
        register_window,
        text="",
        font=("Arial", 12)
    )
    result_label.pack(pady=10)

# CREATE ACCOUNT
    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        if password != confirm_password:
            result_label.config(text="Passwords do not match.")
            return

        if username == "":
            result_label.config(text="Username cannot be empty.")
            return

        if password == "":
            result_label.config(text="Password cannot be empty.")
            return

        if os.path.exists("password_data.json"):
            result_label.config(text="Account already exists.")
            return

        score = 0

        if len(password) >= 8:
            score += 1

        if any(character.isupper() for character in password):
            score += 1

        if any(character.islower() for character in password):
            score += 1

        if any(character.isdigit() for character in password):
            score += 1

        if any(character in string.punctuation for character in password):
            score += 1

        result_label.config(
            text=f"Password score: {score}/5"
        )

        if score < 3:
            result_label.config(
                text="Password is too weak. Please choose a stronger password."
            )
            return

        salt = secrets.token_bytes(16)

        password_bytes = password.encode()

        combined = password_bytes + salt

        password_hash = hashlib.sha256(
            combined
        ).hexdigest()

        password_data = {
            "username": username,
            "salt": salt.hex(),
            "hash": password_hash,
            "account_locked": False
        }

        with open("password_data.json", "w") as file:
            json.dump(password_data, file)

        result_label.config(
            text="Registration successful."
        )

        with open("security_log.txt", "a") as log_file:
            log_file.write(
                str(datetime.datetime.now())
                + " - User registered: "
                + username
                + "\n"
            )

    create_button = tk.Button(
        register_window,
        text="Create Account",
        width=20,
        command=create_account
    )
    create_button.pack(pady=10)


# LOGIN
def login():
    login_window = tk.Toplevel(window)
    login_window.title("Login")
    login_window.geometry("500x400")

    login_title = tk.Label(
        login_window,
        text="Login",
        font=("Arial", 18)
    )
    login_title.pack(pady=20)

    username_label = tk.Label(
        login_window,
        text="Username:",
        font=("Arial", 12)
    )
    username_label.pack(pady=5)

    username_entry = tk.Entry(
        login_window,
        width=30
    )
    username_entry.pack(pady=5)

    password_label = tk.Label(
        login_window,
        text="Password:",
        font=("Arial", 12)
    )
    password_label.pack(pady=10)

    password_entry = tk.Entry(
        login_window,
        width=30,
        show="*"
    )
    password_entry.pack(pady=5)

    result_label = tk.Label(
        login_window,
        text="",
        font=("Arial", 12)
    )
    result_label.pack(pady=15)

    attempts_label = tk.Label(
        login_window,
        text="Attempts remaining: 3",
        font=("Arial", 10)
    )
    attempts_label.pack()

    def check_login():
        if not os.path.exists("password_data.json"):
            result_label.config(
                text="No account found. Please register first."
            )
            return

        with open("password_data.json", "r") as file:
            saved_data = json.load(file)

        if saved_data.get("account_locked", False):
            result_label.config(
                text="Account is locked."
            )
            return

        login_username = username_entry.get()
        login_password = password_entry.get()

        if login_username != saved_data["username"]:
            result_label.config(
                text="Username does not match."
            )
            return

        salt = bytes.fromhex(saved_data["salt"])

        password_bytes = login_password.encode()

        combined = password_bytes + salt

        login_hash = hashlib.sha256(
            combined
        ).hexdigest()

        if login_hash == saved_data["hash"]:
            result_label.config(
                text="Login successful. Welcome!"
            )

            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    str(datetime.datetime.now())
                    + " - User logged in: "
                    + login_username
                    + "\n"
                )

            return

        login_window.attempts -= 1

        attempts_label.config(
            text=f"Attempts remaining: {login_window.attempts}"
        )

        result_label.config(
            text="Password verification failed."
        )

        with open("security_log.txt", "a") as log_file:
            log_file.write(
                str(datetime.datetime.now())
                + " - Failed login attempt: "
                + login_username
                + "\n"
            )

        if login_window.attempts == 0:
            saved_data["account_locked"] = True

            with open("password_data.json", "w") as file:
                json.dump(saved_data, file)

            result_label.config(
                text="Account locked after 3 failed attempts."
            )

            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    str(datetime.datetime.now())
                    + " - Account locked: "
                    + login_username
                    + "\n"
                )

    login_window.attempts = 3

    login_button = tk.Button(
        login_window,
        text="Login",
        width=20,
        command=check_login
    )
    login_button.pack(pady=15)


#UNLOCK
def unlock_account():
    unlock_window = tk.Toplevel(window)
    unlock_window.title("Unlock Account")
    unlock_window.geometry("500x350")

    unlock_title = tk.Label(
        unlock_window,
        text="Unlock Account",
        font=("Arial", 18)
    )
    unlock_title.pack(pady=20)

    code_label = tk.Label(
        unlock_window,
        text="Admin unlock code:",
        font=("Arial", 12)
    )
    code_label.pack(pady=10)

    code_entry = tk.Entry(
        unlock_window,
        width=30,
        show="*"
    )
    code_entry.pack(pady=5)

    result_label = tk.Label(
        unlock_window,
        text="",
        font=("Arial", 12)
    )
    result_label.pack(pady=15)

    def unlock():
        if not os.path.exists("password_data.json"):
            result_label.config(
                text="No account found."
            )
            return

        with open("password_data.json", "r") as file:
            saved_data = json.load(file)

        if not saved_data.get("account_locked", False):
            result_label.config(
                text="Account is not locked."
            )
            return

        admin_code = "ADMIN_1234"

        entered_code = code_entry.get()

        entered_hash = hashlib.sha256(
            entered_code.encode()
        ).hexdigest()

        admin_hash = hashlib.sha256(
            admin_code.encode()
        ).hexdigest()

        if entered_hash == admin_hash:
            saved_data["account_locked"] = False

            with open("password_data.json", "w") as file:
                json.dump(saved_data, file)

            result_label.config(
                text="Account unlocked successfully."
            )

            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    str(datetime.datetime.now())
                    + " - Account unlocked\n"
                )

        else:
            result_label.config(
                text="Incorrect unlock code."
            )

    unlock_button = tk.Button(
        unlock_window,
        text="Unlock Account",
        width=20,
        command=unlock
    )
    unlock_button.pack(pady=10)



window = tk.Tk()

window.title("Password Security Tool")
window.geometry("500x400")

title_label = tk.Label(
    window,
    text="Password Security Tool",
    font=("Arial", 22)
)
title_label.pack(pady=40)

subtitle_label = tk.Label(
    window,
    text="Secure Account Management",
    font=("Arial", 12)
)
subtitle_label.pack(pady=10)

register_button = tk.Button(
    window,
    text="Register",
    width=25,
    command=register
)
register_button.pack(pady=10)

login_button = tk.Button(
    window,
    text="Login",
    width=25,
    command=login
)
login_button.pack(pady=10)

unlock_button = tk.Button(
    window,
    text="Unlock Account",
    width=25,
    command=unlock_account
)
unlock_button.pack(pady=10)

exit_button = tk.Button(
    window,
    text="Exit",
    width=25,
    command=window.destroy
)
exit_button.pack(pady=10)

window.mainloop()
