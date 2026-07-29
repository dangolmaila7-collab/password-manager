"""Password Manager - command-line entry point."""
import os
import json
import getpass

from crypto import simple_hash
from vault import PasswordVault
from generator import generate_password
from entries import add_entry, view_entry, delete_entry, list_entries

VAULT_FILE = "vault.dat"
MASTER_FILE = "master.hash"


def set_master_password():
    pw = getpass.getpass("Create a master password: ")
    with open(MASTER_FILE, "w") as f:
        f.write(str(simple_hash(pw)))
    return pw


def verify_master_password():
    pw = getpass.getpass("Enter master password: ")
    with open(MASTER_FILE) as f:
        stored = f.read().strip()
    if str(simple_hash(pw)) == stored:
        return pw
    return None


def load_vault():
    vault = PasswordVault()
    if not os.path.exists(VAULT_FILE):
        return vault
    with open(VAULT_FILE) as f:
        data = json.load(f)
    for site, entry in data.items():
        vault.insert(site, (entry["username"], entry["password"]))
    return vault


def save_vault(vault):
    data = {}
    for site, (username, enc_pw) in vault.items():
        data[site] = {"username": username, "password": enc_pw}
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f)


def main():
    if not os.path.exists(MASTER_FILE):
        print("No master password set up yet.")
        master_password = set_master_password()
    else:
        master_password = verify_master_password()
        if master_password is None:
            print("Incorrect master password. Exiting.")
            return

    vault = load_vault()

    while True:
        print("\nPassword Manager")
        print("1. Add new entry")
        print("2. Generate a strong password")
        print("3. View entry")
        print("4. List saved sites")
        print("5. Delete entry")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_entry(vault, master_password)
            save_vault(vault)
        elif choice == "2":
            print(f"Suggested password: {generate_password()}")
        elif choice == "3":
            view_entry(vault, master_password)
        elif choice == "4":
            list_entries(vault)
        elif choice == "5":
            delete_entry(vault)
            save_vault(vault)
        elif choice == "6":
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()