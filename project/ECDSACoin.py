""" Descripition to be done

Contains the following classes:
...
Contains the following functions:
...
"""

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
