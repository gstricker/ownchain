from copy import deepcopy
from ecdsa import SigningKey, SECP256k1
from ownchain.bankcoin import Transfer, Bank
from ownchain.utils import serialize

# Create accounts
alice_private_key = SigningKey.generate(curve=SECP256k1)
alice_public_key = alice_private_key.get_verifying_key()
bob_private_key = SigningKey.generate(curve=SECP256k1)
bob_public_key = bob_private_key.get_verifying_key()

# Test
def test_valid_transfers():
    """Issue a coin and transfer it twice
    """

    # Bank issues coin to Alice
    bank = Bank()
    coin = bank.issue(alice_public_key)
    initial_coin_copy = deepcopy(coin)

    assert bank.fetch_coins(alice_public_key) == [initial_coin_copy]
    assert bank.fetch_coins(bob_public_key) == []

    # Alice constructs tranfer to Bob but doesn't tell the bank
    coin.transfer(
        owner_private_key=alice_private_key,
        recipient_public_key=bob_public_key)

    # Check the central bank database -- with untold transfer
    assert bank.fetch_coins(alice_public_key) == [initial_coin_copy]
    assert bank.fetch_coins(bob_public_key) == []

    # Alice tells bank about transfer, bank updates the balance
    bank.observe_coin(coin)
    assert bank.fetch_coins(alice_public_key) == []
    assert bank.fetch_coins(bob_public_key) == [coin]

    # Bob sends to back to Alice, bank updates again
    coin.transfer(
        owner_private_key=bob_private_key,
        recipient_public_key=alice_public_key)

    bank.observe_coin(coin)
    assert bank.fetch_coins(alice_public_key) == [coin]
    assert bank.fetch_coins(bob_public_key) == []
    
