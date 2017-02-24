import argparse
import logging

from zmqconnector import ZmqServer

ZMQ_BASE_PORT = 19797
LOCALHOST = '127.0.0.1'

logger = logging.getLogger(__name__)

## ############################################################

def main(host, port):

    zserver = ZmqServer(host, port)
    logger.info("zserver created - {}:{}".format(host, port))

    while True:
        msg = zserver.recv()
        zserver.send(msg)
        logger.debug("received/replied: '{}'".format(msg))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=LOCALHOST, help="Default: {}".format(LOCALHOST))
    parser.add_argument('--port', default=ZMQ_BASE_PORT, help="Default: {}".format(ZMQ_BASE_PORT))
    args = parser.parse_args()

    logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')

    host = args.host
    port = int(args.port)

    main(host, port)
    logger.info('done.')

