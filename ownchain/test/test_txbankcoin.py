import uuid
from ecdsa import SigningKey, SECP256k1
from ownchain.txbankcoin import TxIn, TxOut, Tx, Bank

# Create accounts
alice_private_key = SigningKey.generate(curve=SECP256k1)
alice_public_key = alice_private_key.get_verifying_key()
bob_private_key = SigningKey.generate(curve=SECP256k1)
bob_public_key = bob_private_key.get_verifying_key()

def test_bank_balances():
    """Issue a coin and transfer it twice
    """

    # Bank issues coin to Alice
    bank = Bank()
    coinbase = bank.issue(1000, alice_public_key)

    # Alice sends 10 coins to Bob
    tx_ins = [
        TxIn(tx_id=coinbase.id, index=0, signature=None)
    ]
    tx_id = uuid.uuid4()
    tx_outs = [
        TxOut(tx_id=tx_id, index=0, amount=10, public_key=bob_public_key),
        TxOut(tx_id=tx_id, index=0, amount=990, public_key=alice_public_key)
    ]

    alice_to_bob = Tx(id=tx_id, tx_ins=tx_ins, tx_outs=tx_outs)
    alice_to_bob.sign_input(0, alice_private_key)
    bank.handle_tx(alice_to_bob)

    assert 990 == bank.fetch_balance(alice_public_key)
    assert 10 == bank.fetch_balance(bob_public_key)
