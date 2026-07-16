"""
Password Manager
-----------------
A command-line password manager that securely stores credentials using
Fernet (AES-128) symmetric encryption, protected by a master password.

Usage:
    python password_manager.py
"""

import base64
import json
import os
import secrets
import string
import sys

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DATA_FILE = "vault.json.enc"
SALT_FILE = "vault.salt"


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from the master password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390_000,
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


def get_or_create_salt() -> bytes:
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = secrets.token_bytes(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def load_vault(fernet: Fernet) -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as f:
        encrypted = f.read()
    if not encrypted:
        return {}
    try:
        decrypted = fernet.decrypt(encrypted)
    except InvalidToken:
        print("Incorrect master password or corrupted vault.")
        sys.exit(1)
    return json.loads(decrypted.decode())


def save_vault(fernet: Fernet, vault: dict) -> None:
    data = json.dumps(vault).encode()
    encrypted = fernet.encrypt(data)
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)


def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def add_entry(vault: dict) -> None:
    service = input("Service/site name: ").strip()
    username = input("Username/email: ").strip()
    choice = input("Generate a strong password automatically? (y/n): ").strip().lower()
    if choice == "y":
        password = generate_password()
        print(f"Generated password: {password}")
    else:
        password = input("Enter password: ").strip()
    vault[service] = {"username": username, "password": password}
    print(f"Saved credentials for '{service}'.")


def retrieve_entry(vault: dict) -> None:
    service = input("Service/site name to look up: ").strip()
    entry = vault.get(service)
    if not entry:
        print(f"No entry found for '{service}'.")
        return
    print(f"Service: {service}")
    print(f"Username: {entry['username']}")
    print(f"Password: {entry['password']}")


def list_services(vault: dict) -> None:
    if not vault:
        print("Vault is empty.")
        return
    print("Stored services:")
    for service in vault:
        print(f"  - {service}")


def delete_entry(vault: dict) -> None:
    service = input("Service/site name to delete: ").strip()
    if service in vault:
        del vault[service]
        print(f"Deleted entry for '{service}'.")
    else:
        print(f"No entry found for '{service}'.")


def main():
    print("=== Password Manager ===")
    master_password = input("Enter your master password: ").strip()
    salt = get_or_create_salt()
    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    vault = load_vault(fernet)

    menu = """
1. Add new entry
2. Retrieve entry
3. List all services
4. Delete entry
5. Save & exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_entry(vault)
        elif choice == "2":
            retrieve_entry(vault)
        elif choice == "3":
            list_services(vault)
        elif choice == "4":
            delete_entry(vault)
        elif choice == "5":
            save_vault(fernet, vault)
            print("Vault saved. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting without saving unsaved changes.")
