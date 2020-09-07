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

def validate():
    """Asks the user for input in a yes/no question

    Parameters
    ----------
    None

    Returns
    -------
    bool
       True or False depending on the input of the user. y = yes, n = no
    """
    
    user_input = input("Is this a valid signature? (y/n)")
    if user_input.lower() == "y":
        return True
    elif user_input.lower() == "n":
        return False
    else:
        validate()

def validate_PNG(filename):
    """Shows a PNG image and asks the user to validate it

    Parameters
    ----------
    filename: str
       A valid filename incl. the path of a PNG image

    Returns
    -------
    void
    """
    
    img = Image.open(filename)
    img.show()
    validate()


