import uuid
import pytest
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.keys import BadSignatureError
from ownchain.banknetcoin import TxIn, TxOut, Tx, Bank

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
        TxOut(tx_id=tx_id, index=1, amount=990, public_key=alice_public_key)
    ]

    alice_to_bob = Tx(id=tx_id, tx_ins=tx_ins, tx_outs=tx_outs)
    alice_to_bob.sign_input(0, alice_private_key)

    # Bob modifies Tx outputs after Alice signs them
    alice_to_bob.tx_outs[0].amount = 990
    alice_to_bob.tx_outs[1].amount = 10

    # Bank should realize the modification and throw an error
    with pytest.raises(BadSignatureError):
        bank.handle_tx(alice_to_bob)


def test_public_key_comparisons():
    derived_bob_public_key = VerifyingKey.from_string(
        bob_public_key.to_string(),
        curve=SECP256k1
    )

    assert bob_public_key.to_string() == derived_bob_public_key.to_string()
    assert bob_public_key == derived_bob_public_key
