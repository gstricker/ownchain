""" This module defines the slightly advanced version of the ECDSACoin
extended with a centralized authority that controls coin flow. The code is 
based on Justin Moons videos from BUIDL camp.

BankCoin itself is meant as the second in a series of naive Blockchain
implementations to showcase some basic properties of a Blockchain. 

For teaching purposes only.

Contains the following classes:
    * Transfer
    * BankCoin
    * Bank

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
    id: uuid.UUID
        The ID of the coin

    Methods
    -------
    transfer
        creates a signed transfer to a recipient
    validate
        validates all transfers of the coin and throws a BadSignatureError in
        case it's invalid
    """
    def __init__(self, transfers):
        self.id = uuid4()
        self.transfers = transfers

    def __eq__(self, other):
        return self.id == other.id and self.transfers == other.transfers

    def transfer(self, owner_private_key, recipient_public_key):
        """Creates a signed transfer to a recepient
        
        Parameters
        ----------
        owner_private_key: ecdsa.keys.SigningKey
            The private key of the current owner
        recipient_public_key: ecdsa.keys.VerifyingKey
            The public key of the recepient

        Returns
        -------
        """
        previous_signature = self.transfers[-1].signature
        message = create_transfer_message(previous_signature, recipient_public_key)

        transfer = Transfer(
            signature=owner_private_key.sign(message),
            public_key=recipient_public_key)

        self.transfers.append(transfer)

    def validate(self):
        """A function to validate the coin transfers. It is split in
        verifying that the first transaction came indeed from a bank and the 
        next transaction are all valid.

        Parameters
        ----------

        Returns
        -------
        Throws BadSignatureError on error
        """        
        previous_transfer = self.transfers[0]
        for t in self.transfers[1:]:
            message = create_transfer_message(
                previous_signature=previous_transfer.signature,
                public_key=t.public_key)
            assert previous_transfer.public_key.verify(t.signature, message)
            previous_transfer = t
                


class Bank:
    """The entity that controls the issuance of coins and maintains
    a coin database
    
    Attributes
    ----------
    coins: dict
        The database of coins as a key-value storage (ID to coin)

    Methods
    -------
    issue
        issues a new BankCoin to given public_key and record in database
    observe_coin
        write coin transfers to database if a valid transfer
    fetch_coins
        read which coins belong to certain owner
    """
                                                   
    def __init__(self):
        # coin.id --> coin
        self.coins = {}        

    def issue(self, public_key):
        """Issues a new BankCoin to given public_key and record in database
        
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

    def observe_coin(self, coin):
        """Write coin transfers to database if a valid transfer
        
        Parameters
        ----------
        coin: BankCoin
            A BankCoin to be transfered
        
        Returns
        -------
        """
        current_coin_status = self.coins[coin.id]
        
        # In coin.transfers[] use all bank recorded transfers (num_transfers)
        # instead of the length of all transfers of the coin - 1 because there
        # might have been more transfers added but not recorded that would need
        # to be validated first
        num_transfers = len(current_coin_status.transfers)
        assert current_coin_status.transfers == coin.transfers[:num_transfers]

        coin.validate()

        self.coins[coin.id] = deepcopy(coin)

    def fetch_coins(self, public_key):
        """Read which coins belong to certain owner

        Parameters
        ----------
        public_key: ecdsa.keys.VerifyingKey
            The given public key to be checked for balance
        
        Returns
        -------
        list
            A list of BankCoins of which the public_key holder is the owner
        """
        coins = []
        for coin in self.coins.values():
            if coin.transfers[-1].public_key.to_string() == \
               public_key.to_string():
                coins.append(coin)
        return coins
