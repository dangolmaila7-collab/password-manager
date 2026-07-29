"""Functions for adding, viewing, listing and deleting entries in
the password vault.
"""
import getpass

from crypto import xor_encrypt, xor_decrypt
from generator import generate_password


def add_entry(vault, master_password):
    """Ask the user for a site and username, then either generate
    a password or read one from input, encrypt it, and store it.
    """
    site = input("Website / service name: ")
    username = input("Username: ")
    choice = input("Auto-generate password? (y/n): ")
    if choice.lower() == "y":
        plain_pw = generate_password()
        print(f"Generated password: {plain_pw}")
    else:
        plain_pw = getpass.getpass("Enter password: ")
    enc_pw = xor_encrypt(plain_pw, master_password)
    vault.insert(site, (username, enc_pw))
    print(f"Saved entry for '{site}'.")


def view_entry(vault, master_password):
    """Look up a site and decrypt/display its stored credentials."""
    site = input("Website / service name: ")
    result = vault.get(site)
    if result is None:
        print("No entry found for that site.")
        return
    username, enc_pw = result
    plain_pw = xor_decrypt(enc_pw, master_password)
    print(f"Username: {username}")
    print(f"Password: {plain_pw}")


def delete_entry(vault):
    """Remove an entry for the given site, if it exists."""
    site = input("Website / service name: ")
    if vault.delete(site):
        print(f"Deleted entry for '{site}'.")
    else:
        print("No entry found for that site.")


def list_entries(vault):
    """Print all stored site names, or a message if the vault is empty."""
    entries = vault.items()
    if not entries:
        print("Vault is empty.")
        return
    print("\nStored sites:")
    for site, _ in entries:
        print(f" - {site}")