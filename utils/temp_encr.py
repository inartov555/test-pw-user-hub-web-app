"""
It's a temporary solution. We need a compiled program to hide the encryption/decription
algorithm.

HOW TO USE:
    1. Uncomment the commented out lines in the bottom of the file
    2. Update data = "YOUR_PASSWORD", set account's password instead of the YOUR_PASSWORD
    3. Run the script in the terminal like this: python3 temp_encr.py
    4. Copy the value after [ENCRYPTED]
"""

import os
import base64

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


PASSWORD = "a;lstrYEDES&^&$&%"
PBKDF2_ITERS = 200000


def derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERS) -> bytes:
    """
    Deriving a key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(plaintext: str, password: str = PASSWORD) -> str:
    """
    Encrypting the text
    """
    _plaintext = plaintext.encode("utf-8")
    salt = os.urandom(16)  # store this with ciphertext
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # unique per encryption
    ct = aesgcm.encrypt(nonce, _plaintext, None)
    encr = salt + nonce + ct
    return base64.b64encode(encr).decode("ascii")


def decrypt(package: str, password: str = PASSWORD) -> str:
    """
    Decrypting the text
    """
    _package = base64.b64decode(package.encode("ascii"))
    salt, nonce, ct = _package[:16], _package[16:28], _package[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    decr = aesgcm.decrypt(nonce, ct, None)
    return decr.decode("utf-8")

# pylint: disable-next=pointless-string-statement
'''
data = "YOUR_PASSWORD"
encrypted = encrypt(data)
decrypted = decrypt(encrypted)
print(f"[ENCRYPTED] {encrypted}")
# DECRYPTED line is just for method checking 
print(f"[DECRYPTED] {decrypted}")
'''
