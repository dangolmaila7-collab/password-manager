"""Simple tests for the custom hash table and the XOR cipher.
Run with: python3 test_vault.py
"""
from vault import PasswordVault
from crypto import xor_encrypt, xor_decrypt


def test_insert_and_get():
    v = PasswordVault()
    v.insert("github.com", ("atipdev", "encrypted123"))
    assert v.get("github.com") == ("atipdev", "encrypted123")
    print("test_insert_and_get passed")


def test_missing_key_returns_none():
    v = PasswordVault()
    assert v.get("doesnotexist.com") is None
    print("test_missing_key_returns_none passed")


def test_delete_removes_entry():
    v = PasswordVault()
    v.insert("site.com", ("user", "pw"))
    v.delete("site.com")
    assert v.get("site.com") is None
    print("test_delete_removes_entry passed")


def test_encrypt_decrypt_roundtrip():
    original = "Sup3r$ecret!"
    key = "master123"
    encrypted = xor_encrypt(original, key)
    decrypted = xor_decrypt(encrypted, key)
    assert decrypted == original
    assert encrypted != original
    print("test_encrypt_decrypt_roundtrip passed")


if __name__ == "__main__":
    test_insert_and_get()
    test_missing_key_returns_none()
    test_delete_removes_entry()
    test_encrypt_decrypt_roundtrip()
    print("\nAll tests passed.")