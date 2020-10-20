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
        spend_message = self.tx_ins[index].spend_message()
        signature = private_key.sign(spend_message)
        self.tx_ins[index].signature = signature

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
    spend_message
        A constructor of the message that will be signed. The structure of
        message is not that important as long as it is easy to replicate and
        encoded in bytecode
    """
    def __init__(self, tx_id, index, signature):
        self.tx_id = tx_id
        self.index = index
        self.signature = signature

    def spend_message(self):
        """A constructor of the message that will be signed. The structure of
            message is not that important as long as it is easy to replicate and
            encoded in bytecode
        
        Parameters
        ----------
        none
        
        Returns
        -------
        bytecode
            The bytecode format is needed as an input for the signing function
        """
        return f"{self.tx_id}:{self.index}".encode()

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
    none
    """
    def __init__(self, tx_id, index, amount, public_key):
        self.tx_id = tx_id
        self.index = index
        self.amount = amount
        self.public_key = public_key

class Bank:
    """ The class of the bank, the central entity that keeps track of
    all transactions

    Attributes
    ----------
    txs: dict
        A database of transactions associated with an ID

    Methods
    -------
    issue
        A method to issue new coins
    is_unspent
        A methond to check if an input is unspent (and thus can be used as an
        input)
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
        self.txs = {}

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
        self.txs[tx.id] = tx
        return tx

    def is_unspent(self, tx_in):
        """A methond to check if an input is unspent (and thus can be used as an
        input)

        Parameters
        ----------
        tx_in: TxIn
            An input transaction

        Returns
        -------
        bool
            True if transaction input has already been spent. False otherwise.
        """

        # Check if the combination of index and id is already present in the
        # transaction database
        for tx in self.txs.values():
            for input_tx in tx.tx_ins:
                if input_tx.tx_id == tx_in.tx_id and \
                   input_tx.index == tx_in.index:
                    return False

        return True

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

        for tx_in in tx.tx_ins:
            # check if unspent
            assert self.is_unspent(tx_in)

            # since inputs don't have amounts, we have to get the amount
            # from the associated outputs of a previous transaction
            tx_out = self.txs[tx_in.tx_id].tx_outs[tx_in.index]
            pub_key = tx_out.public_key
            pub_key.verify(tx_in.signature, tx_in.spend_message())

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
        self.txs[tx.id] = tx

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
