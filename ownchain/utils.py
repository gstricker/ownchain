""" Utility functions for use across projects

Contains the following functions:
    * serialize
    * deserialize
    * to_disk
    * from_disk
    * prepare_tx
"""

import pickle
import uuid

def serialize(coin):
    """Turns Python object into bytecode

    Parameters
    ----------
    coin: Any python object
        Any coin

    Returns
    -------
    Bytecode
    """
    return pickle.dumps(coin)

def deserialize(serialized):
    """Turns bytecode into a Python object

    Parameters
    ----------
    None

    Returns
    -------
    A python object
    """
    return pickle.loads(serialized)

def to_disk(coin, filename):
    """Writes a Python object to filename in bytecode

    Parameters
    ----------
    coin: Any python object
        Any coin
    filename : str
        A file to write the object data to

    Returns
    -------
    None
    """
    serialized = serialize(coin)
    with open(filename, "wb") as f:
        f.write(serialized)

def from_disk(filename):
    """Reads a Python object from filename (in bytecode)

    Parameters
    ----------
    filename : str
        The file to read from

    Returns
    ----------
    A Python object that was stored in bytecode
    """
    with open(filename, "rb") as f:
        serialized = f.read()
    return deserialize(serialized)

def prepare_tx(utxos, sender_private_key, receiver_public_key, amount):
    """Constructs transaction from given UTXOs of the sender and with new Tx
    outputs according to the given amount. Checks if sender has enough UTXOs
    to be spent.

    Parameters
    ----------
    utxos: list of Tx_outs
        A list of UTXOs that can be spend from
    sender_private_key: ecdsa.keys.SigningKey
        The private_key of the sender
    receiver_public_key: ecdsa.keys.VerifyingKey
        The public_key of the receiver
    amount: numeric
        An amount to be spent from the UTXOs

    Returns
    -------
    A transaction of type Tx
    """
    
    # some import to be corrected later
    from ownchain.banknetcoin import Tx, TxIn, TxOut
    
    sender_public_key = sender_private_key.get_verifying_key()
    amount = int(amount)

    # Construct TxIns
    tx_ins = []
    tx_in_sum = 0
    for tx_outs in utxos:
        tx_ins.append(TxIn(tx_id=tx_outs.tx_id, index=tx_outs.index,
                           signature=None))
        tx_in_sum += tx_outs.amount
        if tx_in_sum > amount:
            break

    # Make sure sender can afford it
    assert tx_in_sum >= amount

    # Construct TxOuts
    tx_id = uuid.uuid4()
    change = tx_in_sum - amount
    tx_outs = [
        TxOut(tx_id=tx_id, index=0, amount=amount, public_key=receiver_public_key),
        TxOut(tx_id=tx_id, index=1, amount=change, public_key=sender_public_key)
    ]

    # Construct Tx and sign input
    tx = Tx(id=tx_id, tx_ins=tx_ins, tx_outs=tx_outs)
    for i in range(len(tx.tx_ins)):
        tx.sign_input(i, sender_private_key)

    return tx

