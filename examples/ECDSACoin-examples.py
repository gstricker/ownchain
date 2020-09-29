from coinchains import ECDSACoin as ec
from coinchains.utils import from_disk, to_disk
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
alice = ec.User()
bob = ec.User()
bank = ec.Bank()
mike = ec.User() # malicious user

# validate Issuance
first_coin = bank.issue(alice.public_key)
message = ec.create_transfer_message(b'', alice.public_key)
bank.public_key.verify(first_coin.transfers[0].signature, message)

# make some more transactions
alice_to_bob_msg = ec.create_transfer_message(first_coin.transfers[-1].signature, bob.public_key)
alice_to_bob = ec.Transfer(alice.private_key.sign(alice_to_bob_msg),
                        bob.public_key)
first_coin.transfers.append(alice_to_bob)

# check ownership
first_coin.is_owner(alice.public_key)
first_coin.is_owner(bob.public_key)

# one more transaction
bob_to_bank_msg = ec.create_transfer_message(first_coin.transfers[-1].signature, bank.public_key)
bob_to_bank = ec.Transfer(bob.private_key.sign(bob_to_bank_msg),
                       bank.public_key)
first_coin.transfers.append(bob_to_bank)

# verify good transactions
first_coin.validate(bank)

# check ownership again
first_coin.is_owner(bob.public_key) # check Bob again, now False
first_coin.is_owner(bank.public_key) # True owner

# malicious transaction
bob_to_mike_msg = ec.create_transfer_message(first_coin.transfers[-1].signature, mike.public_key)
bob_to_mike = ec.Transfer(mike.private_key.sign(bob_to_mike_msg),
                       mike.public_key)
first_coin.transfers.append(bob_to_mike)

# check malicious transaction
first_coin.validate(bank)

# Check serialization
filename = "./coin.ecdscoin"
to_disk(first_coin, filename)
my_coin_2 = from_disk(filename)
my_coin_2.validate(bank)

# This comparis does not work as they are not identical (see memory address)
first_coin.is_owner(mike.public_key)
my_coin_2.is_owner(mike.public_key)
mike.public_key == my_coin_2.transfers[-1].public_key

# However this shows those are actually the same public keys, derived from
# the same private key
mike.public_key.to_string() == my_coin_2.transfers[-1].public_key.to_string()
 




