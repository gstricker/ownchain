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
        return f"{self.tx_id}:{self.index}"

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
