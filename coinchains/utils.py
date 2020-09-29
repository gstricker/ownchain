""" Utility functions for use across projects

Contains the following functions:
...
"""

import pickle

def serialize(coin):
    """Turns Python object into bytecode

    Parameters
    ----------
    coin: Any python object
        Any coin

    Returns
    -------
    Bytecode
    """
    return pickle.dumps(coin)

def deserialize(serialized):
    """Turns bytecode into a Python object

    Parameters
    ----------
    None

    Returns
    -------
    A python object
    """
    return pickle.loads(serialized)

def to_disk(coin, filename):
    """Writes a Python object to filename in bytecode

    Parameters
    ----------
    coin: Any python object
        Any coin
    filename : str
        A file to write the object data to

    Returns
    -------
    None
    """
    serialized = serialize(coin)
    with open(filename, "wb") as f:
        f.write(serialized)

def from_disk(filename):
    """Reads a Python object from filename (in bytecode)

    Parameters
    ----------
    filename : str
        The file to read from

    Returns
    ----------
    A Python object that was stored in bytecode
    """
    with open(filename, "rb") as f:
        serialized = f.read()
    return deserialize(serialized)
