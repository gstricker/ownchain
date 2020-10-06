""" This module defines the slightly advanced version of the PNGCoin
extended with cryptography instead of PNG images. The code is based on Justin 
Moons videos from BUIDL camp.

PNG Coin itself is meant as the second in a series of naive Blockchain
implementations to showcase some basic properties of a Blockchain. 

For teaching purposes only.

Contains the following classes:
    * Transfer
    * BankCoin
    * User
    * Bank (inhereted from User)

Contains the following functions:
    * create_transfer_message
...
"""
from uuid import uuid4
from copy import deepcopy
from ownchain.utils import serialize
from ecdsa import BadSignatureError, SigningKey, SECP256k1

#####################
# Hellper functions #
#####################

def create_transfer_message(previous_signature, public_key):
    """A function to create a transfer message for the next transfer

    Parameters
    ----------
    previous_signature : bytecode
        The signature of the previous transfer
    public_key: ecdsa.keys.VerifyingKey
        the public key of the recipient

    Returns
    -------
    bytecode
        A signed message
    """
    message = {
        "previous_signature": previous_signature,
        "next_public_key": public_key
    }
        
    return serialize(message)

############
# BankCoin #
############

class Transfer:
    """A class to handle coin transfer between public keys

    Attributes
    ----------
    signature : bytecode
        cryptographic signature of the sender
    public_key: ecdsa.keys.VerifyingKey
        the public key of the recipient

    Methods
    -------
    ...
    """
    def __init__(self, signature, public_key):
        self.signature = signature
        self.public_key = public_key

    def __eq__(self, other):
        return self.signature == other.signature and \
            self.public_key.to_string() == other.public_key.to_string()

class BankCoin:
    """The class of the BankCoin
    
    Attributes
    ----------
    transfers: list
        A list of coin transfers where each element is of type Transfer

    Methods
    -------
    None
    """
    def __init__(self, transfers):
        self.id = uuid4()
        self.transfers = transfers

    def __eq__(self, other):
        return self.id == other.id and self.transfers == other.transfers

    def transfer(self, owner_private_key, recipient_public_key):
        previous_signature = self.transfers[-1].signature
        message = create_transfer_message(previous_signature, recipient_public_key)

        transfer = Transfer(
            signature=owner_private_key.sign(message),
            public_key=recipient_public_key)

        self.transfers.append(transfer)

    def validate(self, bank):
        """A function to validate the coin transfers. It is split in
        verifying that the first transaction came indeed from a bank and the 
        next transaction are all valid.

        Parameters
        ----------
        bank: Bank
            The bank that has issued the first coin. Needed in order to be
            able to check the coinage transaction is valid

        Returns
        -------
        bool
        """
        
        try:
            first_transfer = self.transfers[0]
            message = create_transfer_message(b'',first_transfer.public_key)
            bank.public_key.verify(first_transfer.signature, message)
            
        except BadSignatureError:
            print("Bad Signature in coinage transaction")
            return False

        try:
            for i in range(len(self.transfers))[1:]:
                message = create_transfer_message(self.transfers[i-1].signature,
                           self.transfers[i].public_key)
                self.transfers[i-1].public_key.verify(self.transfers[i].signature,
                                                      message)
                
        except BadSignatureError:
            print("Bad Signature in transaction number", i+1)
            return False

        return True

class Bank:
    """TBD
    
    Attributes
    ----------
    
    Methods
    -------
    """
                                                   
    def __init__(self):
        # coin.id --> coin
        self.coins = {}        

    def issue(self, public_key):
        """Issues a new ECDSACoin to given public_key
        
        Parameters
        ----------
        public_key: ecdsa.keys.VerifyingKey
            The public key of the recipient
        
        Returns
        -------
        BankCoin
        """    
        transfer = Transfer(
            signature = None,
            public_key = public_key)

        # Create initial coin
        coin = BankCoin(transfers=[transfer])

        # Put coin into database
        self.coins[coin.id]=deepcopy(coin)
        
        return coin

    def fetch_coins(self, public_key):
        coins = []
        for coin in self.coins.values():
            if coin.transfers[-1].public_key.to_string() == \
               public_key.to_string():
                coins.append(coin)
        return coins
