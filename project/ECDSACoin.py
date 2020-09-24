""" Descripition to be done

Contains the following classes:
...
Contains the following functions:
...
"""
from project import utils
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
        
    return utils.serialize(message)

#############
# ECDSACoin #
#############

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

class ECDSACoin:
    """The class of the ECDSACoin
    
    Attributes
    ----------
    transfers: list
        A list of coin transfers where each element is of type Transfer

    Methods
    -------
    None
    """
    def __init__(self, transfers):
        self.transfers = transfers

    def is_owner(self, public_key):
        """Checks the ownership of the coin if given a public key to compare

        Parameters
        ----------
        public_key: ecdsa.keys.VerifyingKey
            the public key of the owner
        
        Returns
        -------
        bool
        """
        if self.transfers[-1].public_key == public_key:
            return True
        return False

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

class User:
    """The class of a user in the ECDSA Banking System
    
    Attributes
    ----------
    private_key: ecdsa.keys.SigningKey
        The private_key of a user
    public_key: ecdsa.keys.VerifyingKey
        The public key of a user

    Methods
    -------
    None
    """
    def __init__(self):
        self.private_key = SigningKey.generate(curve = SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

class Bank(User):
    """The class that the defines a bank in the ECDSA Banking system.
    Inherits the init method from the User class
    
    Attributes
    ----------
    see User
    
    Methods
    -------
    issue
        issues a new ECDSACoin to given public_key
    """
                                                   
    def issue(self, public_key):
        """Issues a new ECDSACoin to given public_key
        
        Parameters
        ----------
        public_key: ecdsa.keys.VerifyingKey
            The public key of the recipient
        
        Returns
        -------
        ECDSACoin
        """
        message = create_transfer_message(b'',public_key)
        signature = self.private_key.sign(message)
        
        transfer = Transfer(
            signature = signature,
            public_key = public_key)

        coin = ECDSACoin([transfer])
        return coin
        
