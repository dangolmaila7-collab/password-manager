"""Encryption helpers: a symmetric XOR cipher and a simple hash
function used to verify the master password without storing it
in plain text.
"""


def derive_key(master_password, length):
    """Extend the master password by repeating it until it is at
    least `length` characters long, then trim it to that length.
    """
    key = ""
    while len(key) < length:
        key += master_password
    return key[:length]


def xor_encrypt(text, master_password):
    """Encrypt `text` by XOR-ing each character with the matching
    character of a key derived from the master password.
    """
    key = derive_key(master_password, len(text))
    cipher = [chr(ord(t) ^ ord(k)) for t, k in zip(text, key)]
    return "".join(cipher)


def xor_decrypt(cipher_text, master_password):
    """XOR is its own inverse, so decryption reuses xor_encrypt."""
    return xor_encrypt(cipher_text, master_password)


def simple_hash(text):
    """A small djb2-style hash used only to verify the master
    password against a stored value, so the real password is
    never written to disk.
    """
    h = 5381
    for ch in text:
        h = (h * 33 + ord(ch)) % (2 ** 32)
    return h