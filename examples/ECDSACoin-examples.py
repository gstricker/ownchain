from ecdsa import SigningKey, SECP256k1

# generate key-pair
private_key = SigningKey.generate(curve = SECP256k1)
public_key = private_key.get_verifying_key()

# Messages (messages must in be in byte format)
true_message = b'I am a correct message'
false_message = b'I am a wrong message'

# Signature
signature = private_key.sign(true_message)
signature_2 = private_key.sign(false_message)

# Test signature
public_key.verify(signature, true_message)
public_key.verify(signature, false_message) #throws error

signature == signature_2

