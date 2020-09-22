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

# Create user and bank
alice = User()
bob = User()
bank = Bank()
mike = User() # malicious user

# validate Issuance
first_coin = bank.issue(alice.public_key)
message = create_transfer_message(b'', alice.public_key)
bank.public_key.verify(first_coin.transfers[0].signature, message)

# make some more transactions
alice_to_bob_msg = create_transfer_message(first_coin.transfers[-1].signature, bob.public_key)
alice_to_bob = Transfer(alice.private_key.sign(alice_to_bob_msg),
                        bob.public_key)
first_coin.transfers.append(alice_to_bob)

bob_to_bank_msg = create_transfer_message(first_coin.transfers[-1].signature, bank.public_key)
bob_to_bank = Transfer(bob.private_key.sign(bob_to_bank_msg),
                       bank.public_key)
first_coin.transfers.append(bob_to_bank)

# verify good transactions
first_coin.validate(bank)

# malicious transaction
bob_to_mike_msg = create_transfer_message(first_coin.transfers[-1].signature, mike.public_key)
bob_to_mike = Transfer(mike.private_key.sign(bob_to_mike_msg),
                       mike.public_key)
first_coin.transfers.append(bob_to_bank)

# check malicious transaction
first_coin.validate(bank)
