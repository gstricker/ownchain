"""PNG Coin

This functions define the simple and stupid form of a Blockchain via PNG images:
PNG Coin. The code is based on Justin Moons videos from BUIDL camp.

PNG Coin itself is meant as the first in a series of naive Blockchain 
implementations to showcase some basic properties of a Blockchain. In that 
regard the implementation teaches what NOT to do!

For teaching purposes only.

Contains the following functions:
   * validate
   * validate_PNG
"""

from PIL import Image
import pickle

#####################
# Hellper functions #
#####################

def handle_user_input(user_input):
    """Handles user input and returns a bool for valid answers, calls itself
    otherwise

    Parameters
    ----------
    user_input: str
        A string of user input

    Returns
    -------
    bool
        True or False depending on the input of the user. y = yes, n = no
    """

    if user_input.lower() == "y":
        return True
    elif user_input.lower() == "n":
        return False
    else:
        user_input = input("Please answer only y or n")
        return handle_user_input(user_input)

###########
# PNGCoin #
###########

class PNGCoin:
    """The class of the simple PNGCoin

    Attributes
    ----------
    transfers: list 
    A list of images of type PIL.PngImagePlugin.PngImageFile generated from 
    Image.open()

    Methods
    -------
    None
    """
    
    def __init__(self, transfers):
        self.transfers = transfers

    def validate(self):
    """Asks the user for input in a yes/no question

    Parameters
    ----------
    coin: PNGCoin
        A coin of type PNGCoin

    Returns
    -------
    bool 
        True or False based on the validity of the transfers
    """
    
    for transfer in self.transfers:
        transfer.show()
    user_input = input("Is this a valid signature? (y/n)")
        valid = handle_user_input(user_input)
        if not valid:
            return False
    return True

def to_disk(coin, filename):
    """Writes a Python object to filename in bytecode
    
    Parameters
    ----------
    coin: PNGCoin
        A PNGCoin
    filename: str
        A file to write the object data to

    Returns
    -------
    None
    """
    serialized = pickle.dumps(coin)
    with open(filename, "wb") as f:
        f.write(serialized)

def from_disk(filename):
    """Reads a Python object from filename (in bytecode)

    Parameters
    ----------
    filename: str
        The file to read from

    Returns
    ----------
    A Python object that was stored in bytecode
    """
    with open(filename, "rb") as f:
        serialized = f.read()
        return pickle.loads(serialized)
    
    
