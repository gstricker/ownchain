"""PNG Coin

This script define the simple and stupid form of a Blockchain via PNG images:
PNG Coin. The code is based on Justin Moons videos from BUIDL camp.

PNG Coin itself is meant as the first in a series of naive Blockchain
implementations to showcase some basic properties of a Blockchain. In that
regard the implementation teaches what NOT to do!

For teaching purposes only.

Contains the following class:
   * PNGCoin

Contains the following functions
   * handle_user_input
"""

import pickle

#####################
# Hellper functions #
#####################


def handle_user_input(user_input):
    """Handles user input and returns a bool for valid answers, calls itself
    otherwise

    Parameters
    ----------
    user_input : str
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
    transfers : list
        A list of images of type PIL.PngImagePlugin.PngImageFile generated from
        Image.open()

    Methods
    -------
    serialize
        Turns Python object into bytecode
    deserialize
        Turns bytecode into a Python object
    validate
        Validates the coin by showing PNG images of signatures
    to_disk
        Writes a Python object to filename in bytecode
    from_disk
        Reads a Python object from filename (in bytecode)
    """

    def __init__(self, transfers):
        self.transfers = transfers

    def validate(self):
        """Validates the coin by showing PNG images of signatures

        Parameters
        ----------
        coin : PNGCoin
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
