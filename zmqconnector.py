# -*- coding: utf-8 -*-
"""
    zmqconnector.py

    ZeroMQ Connector - Abstraction around a simple socket using
                       ZMQ's PAIR socket type.  (i.e. a Pipe)

    :copyright: (c) 2017 by Eric Gustafson
    :license: BSD, see LICENSE for more details.
"""

VERSION = (0, 2)
__version__ = '.'.join(map(str, VERSION[0:2]))
__description__ = 'ZeroMQ Connector in Python'
__author__ = 'Eric Gustafson'
__license__ = 'BSD'

import zmq
import logging
import sys

logger = logging.getLogger(__name__)

## ############################################################

class ZmqConnection(object):
    """ZeroMQ generalized connection"""

    def __init__(self, host, port):
        self.addr = "tcp://{}:{}".format(host, int(port))
        self.zcontext = zmq.Context()
        self.closed = False

    def send(self, data):
        return self.sock.send(data)

    def recv(self):
        return self.sock.recv()

    def close(self, linger=None):
        self.sock.close(linger)
        self.closed = True


class ZmqServer(ZmqConnection):

    def __init__(self, host, port):
        super(ZmqServer, self).__init__(host, port)
        self.sock = self.zcontext.socket(zmq.PAIR)
        self.sock.bind(self.addr)
        logger.debug("zmq listening on {}".format(self.addr))


class ZmqClient(ZmqConnection):

    def __init__(self, host, port):
        super(ZmqClient, self).__init__(host, port)
        self.sock = self.zcontext.socket(zmq.PAIR)
        self.sock.connect(self.addr)
        logger.debug("zmq connecting to ()".format(self.addr))


if __name__=='__main__':
    logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')
    logger.info("Using  pyzmq v{}".format(zmq.__version__))
    logger.info("Using libzmq v{}".format(zmq.zmq_version()))
