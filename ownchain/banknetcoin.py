""" This module defines the slightly advanced version of the BankCoin Family. 
It includes some bug fixes from BankCoin as well as ...

The code is based on Justin Moons  videos from BUIDL
camp.

BankNetCoin itself is meant as the sixth in a series of naive Blockchain
implementations to showcase some basic properties of a Blockchain. In the 
original series the BankNetCoin is part of BlockCoin

For teaching purposes only.

Contains the following classes:
    * Bank
    * Tx
    * TxIn
    * TxOut

Contains the following functions:
    * 
...
"""
from uuid import uuid4
from copy import deepcopy
from ecdsa import SigningKey, SECP256k1
from ownchain.utils import serialize

def spend_message(tx, index):
    # potentially move to Tx as a class method
    tx_in = tx.tx_ins[index]
    outpoint = tx_in.outpoint
    return serialize(outpoint) + serialize(tx.tx_outs)

class Tx:
    """ A class that defines a transaction with inputs and outputs
    
    Attributes
    ----------
    id: uuid.UUID
        The ID of the transaction
    tx_ins: list
        A list of all transaction inputs
    tx_outs: list
        A list of all transaction outputs
    
    Methods
    -------
    sign_input
        method to sign the input in a transaction (usually by the sender)
    """

    def __init__(self, id, tx_ins, tx_outs):
        self.id = id
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs

    def sign_input(self, index, private_key):
        """ Method to sign the input in a transaction (usually by the sender)

        Parameters
        ----------
        index: int
            The index number of the input. Each input has to be signed
            separately
        private_key: ecdsa.keys.SigningKey
            The private key of the owner of the input
        
        Returns
        -------
        none
        """
        message = spend_message(self, index)
        signature = private_key.sign(message)
        self.tx_ins[index].signature = signature

    def verify_input(self, index, public_key):
        tx_in = self.tx_ins[index]
        message = spend_message(self, index)
        return public_key.verify(tx_in.signature, message)

class TxIn:
    """ The class of a transaction input
    
    Attributes
    ----------
    tx_id: uuid.UUID
        The ID of the transaction input
    index:
        The index number of the input. That is its place in the list of inputs
    signature: bytecode
        cryptographic signature of the input owner

    Methods
    -------
    outpoint
        A unique identifier to a transaction input
    """
    def __init__(self, tx_id, index, signature):
        self.tx_id = tx_id
        self.index = index
        self.signature = signature

    @property
    def outpoint(self):
        """ A unique identifier to a transaction input in the form of a tuple
        of ID and index
        
        Parameters
        ----------
        none
        
        Returns
        -------
        tuple
            A tuple of transaction ID and transaction index
        """
        return (self.tx_id, self.index)

class TxOut:
    """ A class for the transaction output

    Attributes
    ----------
    tx_id: uuid.UUID
        The ID of the transaction output
    index:
        The index number of the output. That is its place in the list of outputs
    amount: numeric (int or float)
        The amount to be sent
    public_key:ecdsa.keys.VerifyingKey
        the public key of the recipient

    Methods
    -------
    outpoint
        A unique identifier to a transaction input
    """
    def __init__(self, tx_id, index, amount, public_key):
        self.tx_id = tx_id
        self.index = index
        self.amount = amount
        self.public_key = public_key

    @property
    def outpoint(self):
        """ A unique identifier to a transaction output in the form of a tuple
        of ID and index
        
        Parameters
        ----------
        none
        
        Returns
        -------
        tuple
            A tuple of transaction ID and transaction index
        """
        return (self.tx_id, self.index)

class Bank:
    """ The class of the bank, the central entity that keeps track of
    all transactions

    Attributes
    ----------
    utxo: dict
        A database of unspent transactions associated with an ID and index

    Methods
    -------
    update_utxo
        Updates the UTXO database
    issue
        A method to issue new coins
    validate
        Method to validate a transactions
    handle_tx
        Method to deal with incoming transactions
    fetch_utxo
        Get all unspent transactions (UTXOs) that are associated with a 
        specific public_key
    fetch_balance
        Get the balance for a specific public_key
    """
    def __init__(self):
        # mapping (tx_id, index) --> tx_out 
        self.utxo = {}

    def update_utxo(self, tx):
        """ Updates the UTXO database with new transaction outputs while
        deleting spent inputs
        
        Parameters
        ----------
        tx: Tx
            A transaction
        
        Returns
        -------
        none
        """
        for tx_in in tx.tx_ins:
            del self.utxo[tx_in.outpoint]

        for tx_out in tx.tx_outs:
            self.utxo[tx_out.outpoint] = tx_out

    def issue(self, amount, public_key):
        """A method to issue new coins

        Parameters
        ----------
        amount: numeric (int or float)
            The amount of new coins to be issued
        public_key: ecdsa.keys.VerifyingKey
            The public_key of the recipient of new coins

        Returns
        -------
        Tx
            A transaction of type Tx
        """
        id = uuid4()
        tx_ins = []
        tx_outs = [
            TxOut(tx_id=id, index=0, amount=amount, public_key=public_key)
        ]
        tx = Tx(id=id, tx_ins=tx_ins, tx_outs=tx_outs)
        self.update_utxo(tx)
        return tx

    def validate(self, tx):
        """Method to validate a transactions. That is, validate that the
        input transactions have not been spent and that the sum of the inputs
        is equal to the sum of the outputs

        Parameters
        ----------
        tx: Tx
            A transaction

        Returns
        -------
        bool
            True if valid. Raisese AssertionError otherwise
        """
        in_sum = 0
        out_sum = 0

        for index, tx_in in enumerate(tx.tx_ins):
            # check if unspent
            assert tx_in.outpoint in self.utxo

            # since inputs don't have amounts, we have to get the amount
            # from the associated outputs of a previous transaction
            tx_out = self.utxo[tx_in.outpoint]
            pub_key = tx_out.public_key
            tx.verify_input(index, pub_key)

            # sum up inputs
            in_sum += tx_out.amount

        # sum up outputs
        for tx_out in tx.tx_outs:
            out_sum += tx_out.amount

        assert in_sum == out_sum

    def handle_tx(self, tx):
        """Method to deal with incoming transactions. That is validate and if
        valid store in database
        
        Parameters
        ----------
        tx: Tx
            A transaction to be handled

        Returns
        -------
        none
        """
        self.validate(tx)
        self.update_utxo(tx)

    def fetch_utxo(self, public_key):
        """Get all unspent transactions (UTXOs) that are associated with a 
        specific public_key
        
        Parameters
        ----------
        public_key: ecdsa.keys.VerifyingKey
            the public key of the client

        Returns
        -------
        list
            All output transactions associated with the public_key, 
            but not in the spent list
        """
        return [utxo for utxo in self.utxo.values()
                if utxo.public_key == public_key]

    def fetch_balance(self, public_key):
        """Get the balance for a specific public_key

        Parameters
        ----------
        public_key: ecdsa.keys.VerifyingKey
            The public key of the client

        Returns
        -------
        numeric (int or float)
            The balance of the account
        """
        utxo = self.fetch_utxo(public_key)
        return sum([tx_out.amount for tx_out in utxo])
