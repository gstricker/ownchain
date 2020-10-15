""" This module defines the slightly advanced version of the BankCoin
extended with a transaction system that lets the coins be transacted instead of
just transfered. Transactions require amounts and thus enable divisibility 
instead of giving an entire coin form A to B. The code is based on Justin Moons
 videos from BUIDL camp.

txBankCoin itself is meant as the fourth in a series of naive Blockchain
implementations to showcase some basic properties of a Blockchain. In the 
original series the txBankCoin is part of BankCoin.

For teaching purposes only.

Contains the following classes:
    * Bank

Contains the following functions:
    * 
...
"""
from uuid import uuid4

class Tx:

    def __init__(self, id, tx_ins, tx_outs):
        self.id = id
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs

    def sign_input(self, index, private_key):
        spend_message = self.tx_ins[index].spend_message()
        signature = private_key.sign(spend_message)
        self.tx_ins[index].signature = signature

class TxIn:
    
    def __init__(self, tx_id, index, signature):
        self.tx_id = tx_id
        self.index = index
        self.signature = signature

    def spend_message(self):
        """Needed to encode to bystring for hashing in the signing function
        """
        return f"{self.tx_id}:{self.index}".encode()

class TxOut:
    
    def __init__(self, tx_id, index, amount, public_key):
        self.tx_id = tx_id
        self.index = index
        self.amount = amount
        self.public_key = public_key

class Bank:

    def __init__(self):
        self.txs = {}

    def issue(self, amount, public_key):
        id = uuid4()
        tx_ins = []
        tx_outs = [
            TxOut(tx_id=id, index=0, amount=amount, public_key=public_key)
        ]
        tx = Tx(id=id, tx_ins=tx_ins, tx_outs=tx_outs)
        self.txs[tx.id] = tx
        return tx

    def is_unspent(self, tx_in):
        for tx in self.txs.values():
            for input_tx in tx.tx_ins:
                if input_tx.tx_id == tx_in.tx_id and \
                   input_tx.index == tx_in.index:
                    return False

        return True

    def validate(self, tx):
        in_sum = 0
        out_sum = 0

        for tx_in in tx.tx_ins:
            assert self.is_unspent(tx_in)

            tx_out = self.txs[tx_in.tx_id].tx_outs[tx_in.index]
            pub_key = tx_out.public_key
            pub_key.verify(tx_in.signature, tx_in.spend_message())

            in_sum += tx_out.amount

        for tx_out in tx.tx_outs:
            out_sum += tx_out.amount

        assert in_sum == out_sum

    def handle_tx(self, tx):
        self.validate(tx)
        self.txs[tx.id] = tx

    def fetch_utxo(self, public_key):
        # Find which (tx_id, index) pairs have been spent
        spent_pairs = [(tx_in.tx_id, tx_in.index)
                       for tx in self.txs.values()
                       for tx_in in tx.tx_ins]
        # Return tx_outs associated with the public_key and not in the spent list
        return [tx_out for tx in self.txs.values()
                for i, tx_out in enumerate(tx.tx_outs)
                    if public_key == tx_out.public_key
                    and (tx.id, i) not in spent_pairs]

    def fetch_balance(self, public_key):
        utxo = self.fetch_utxo(public_key)
        return sum([tx_out.amount for tx_out in utxo])
