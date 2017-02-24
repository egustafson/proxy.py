import logging
import zmq

from zmqconnector import ZmqClient, ZmqServer

LOCALHOST = '127.0.0.1'

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')

## ############################################################

zserver = ZmqServer(LOCALHOST, 19888)
zclient = ZmqClient(LOCALHOST, 19778)

logger.info("Client and Server initialized")

while True:
    rlist = [zclient.recvsock, zserver.recvsock]
    (r, w, x) = zmq.select(rlist, [], [], 5)

    if zclient.recvsock in r:
        msg = zclient.recv()
        zserver.send(msg)
        logger.debug("c->s: '{}'".format(msg))

    if zserver.recvsock in r:
        msg = zserver.recv()
        zclient.send(msg)
        logger.debug("s->c: '{}'".format(msg))

    if len(r) <= 0:
        logger.debug("nothing received.")
