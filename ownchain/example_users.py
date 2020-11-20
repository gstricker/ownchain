"""
A few functions to simulate users in the system

Contains the following constants:
    * alice_private_key
    * bob_private_key

Contains the following functions:
    * user_private_key
    * user_public_key
"""

from ecdsa import SigningKey, SECP256k1

alice_private_key = SigningKey.from_secret_exponent(1, curve=SECP256k1)

bob_private_key = SigningKey.from_secret_exponent(2, curve=SECP256k1)

def user_private_key(name):
    name_to_key = {
        "alice": alice_private_key,
        "bob": bob_private_key
    }
    return name_to_key[name]

def user_public_key(name):
    private_key = user_private_key(name)
    return private_key.get_verifying_key()
