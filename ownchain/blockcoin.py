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
import os
import threading
import re

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
HOST = '0.0.0.0'
PORT = 10000
ADDRESS = (HOST, PORT)

current = 0
ID = int(os.environ['ID'])
PEER_HOSTNAMES = os.environ['PEERS'].split(',')


class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class TCPHandler(socketserver.BaseRequestHandler):

    def peer(self):
        address = self.client_address[0]
        host_info = socket.gethostbyaddr(address)
        return re.search(r'_(.+?)_', host_info[0]).group(1)

    def handle(self):
        message_bytes = self.request.recv(10).strip()
        logger.info(f'Received {message_bytes.decode()} from "{self.peer()}"')
        self.request.sendall(b'pong\n')
        logger.info(f'Send "pong" to "{self.peer()}"')
        
        schedule_ping()


def ping(hostname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (hostname, PORT)
    sock.connect(addr)
    sock.sendall(b'ping')
    logger.info(f'Sent "ping" to "{hostname}"')
    response = sock.recv(10)
    logger.info(f'Received {response.decode()} form "{hostname}"')


def ping_peers():
    for hostname in PEER_HOSTNAMES:
        ping(hostname)


def schedule_ping():
    global current
    current = (current + 1) % 3
    if ID == current:
        threading.Timer(3, ping_peers).start()


def serve():
    schedule_ping()
    server = MyTCPServer(ADDRESS, TCPHandler)
    server.serve_forever()


# Main
if __name__ == "__main__":
    banknetcoin()
