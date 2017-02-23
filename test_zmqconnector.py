import unittest
import multiprocessing
import zmqconnector
from zmqconnector import ZmqServer
from zmqconnector import ZmqClient

ZMQ_BASE_PORT = 19797
LOCALHOST = '127.0.0.1'

class StubLoopbackAgent(multiprocessing.Process):

    def __init__(self, cls, host, port):
        self.proto = cls
        self.host = host
        self.port = port

    def run(self):
        agent = self.proto(host, port)
        msg = agent.recv()
        agent.send(msg)
        ## done - only loop a single message


class TestZmqConnector(unittest.TestCase):

    def test_create_server(self):
        zserver = ZmqServer(LOCALHOST, ZMQ_BASE_PORT)
        self.assertFalse(zserver.closed)
        zserver.close()
        self.assertTrue(zserver.closed)


    def test_create_client(self):
        zclient = ZmqClient(LOCALHOST, ZMQ_BASE_PORT)
        self.assertFalse(zclient.closed)
        zclient.close()
        self.assertTrue(zclient.closed)


    @unittest.skip("BROKEN:  some thread/race condition - investigate (eg-2/2017)")
    def test_client(self):
        remote = StubLoopbackAgent(ZmqServer, LOCALHOST, ZMQ_BASE_PORT)
        zclient = ZmqClient(LOCALHOST, ZMQ_BASE_PORT)
        sendmsg = b'xyzzy'
        zclient.send(sendmsg)
        recvmsg = zclient.recv()
        self.assertEqual(sendmsg, recvmsg)
        zclient.close()


