# -*- coding: utf-8 -*-
"""
    zmqconnector.py

    ZeroMQ Connector - Create a pair of zmq PUSH-PULL sockets
      in opposite directions to emulate a bidirectional "Pipe".
      One end listens and the other connects.

    :copyright: (c) 2017 by Eric Gustafson
    :license: BSD, see LICENSE for more details.
"""

VERSION = (0, 1)
__version__ = '.'.join(map(str, VERSION[0:2]))
__description__ = 'ZeroMQ Connector in Python'
__author__ = 'Eric Gustafson'
__license__ = 'BSD'

import zmq
import logging
import sys

logger = logging.getLogger(__name__)

# True if we're running Python 3.
PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    binary_type = bytes
    from urllib import parse as urlparse
else:
    text_type = unicode
    binary_type = str
    import urlparse


def text_(s, encoding='utf-8', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s  # pragma: no cover


def bytes_(s, encoding='utf-8', errors='strict'):
    """ If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, text_type):  # pragma: no cover
        return s.encode(encoding, errors)
    return s

## ############################################################

class ZmqConnection(object):
    """ZeroMQ generalized connection"""

    def __init__(self, host, pushport, pullport):
        self.pushaddr = "tcp://{}:{}".format(host, int(pushport))
        self.pulladdr = "tcp://{}:{}".format(host, int(pullport))
        self.zcontext = zmq.Context()
        self.closed = False

    def send(self, data):
        return self.sendsock.send(data)

    def recv(self):
        return self.recvsock.recv()

    def close(self, linger=None):
        self.recvsock.close(linger)
        self.sendsock.close(linger)
        self.closed = True


class ZmqServer(ZmqConnection):

    def __init__(self, host, port):
        super(ZmqServer, self).__init__(host, port, int(port)+1)
        self.recvsock = self.zcontext.socket(zmq.PULL)
        self.recvsock.bind(self.pulladdr)
        self.sendsock = self.zcontext.socket(zmq.PUSH)
        self.sendsock.bind(self.pushaddr)


class ZmqClient(ZmqConnection):

    def __init__(self, host, port):
        super(ZmqClient, self).__init__(host, int(port)+1, port)
        self.recvsock = self.zcontext.socket(zmq.PULL)
        self.recvsock.connect(self.pulladdr)
        self.sendsock = self.zcontext.socket(zmq.PUSH)
        self.sendsock.connect(self.pushaddr)

