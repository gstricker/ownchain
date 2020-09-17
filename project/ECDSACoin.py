""" Descripition to be done

Contains the following classes:
...
Contains the following functions:
...
"""

import pickle

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
        self.publick_key = public_key

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
        message = pickle.dumps(public_key)
        signature = self.private_key.sign(message)
        
        transfer = Transfer(
            signature = signature,
            public_key = public_key)

        coin = ECDSACoin([transfer])
        return coin
