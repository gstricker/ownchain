""" This module defines the slightly advanced version of the BankCoin Family.
It includes some bug fixes from BankCoin as well as ...

The code is based on Justin Moons  videos from BUIDL
camp.

BankNetCoin itself is meant as the sixth in a series of naive Blockchain
implementations to showcase some basic properties of a Blockchain. In the
original series the BankNetCoin is part of BlockCoin

For teaching purposes only.

Contains the following classes:
    * Bank
    * Tx
    * TxIn
    * TxOut

Contains the following functions:
    *
...
"""
import socketserver
import socket
import sys
import logging
import click

############################# Arg Parsing ######################################

# CONTEXT_SETTINGS = dict(help_option_name=['-h', '--help'])

# def execute_command(command, data):
#     response = send_message(command, data)
#     print(f'Received: {response}')

# @click.group(context_settings=CONTEXT_SETTINGS)
# @click.version_option(version='1.0.0')
@click.group()
def banknetcoin():
    pass


@banknetcoin.command()
def ping():
    """Test connection
    """
    ping()


@banknetcoin.command()
def serve():
    """Starts server
    """
    serve()


############################## Sockets #########################################

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime) - 15s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
HOST = "0.0.0.0"
PORT = 10000
ADDRESS = (HOST, PORT)


def ping():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    sock.sendall(b'ping')
    response = sock.recv(10)
    logger.info(f'Received {str(response)}')


def serve():
    server = socketserver.TCPServer(ADDRESS, TCPHandler)
    server.serve_forever()


class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        message_bytes = self.request.recv(10).strip()
        logger.info(f'Received {str(message_bytes)}')
        if message_bytes == b'ping':
            self.request.sendall(b'pong\n')
            logger.info('Send pong')


# Main
if __name__ == "__main__":
    banknetcoin()
