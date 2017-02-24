import argparse
import logging

from zmqconnector import ZmqClient

ZMQ_BASE_PORT = 19797
LOCALHOST = '127.0.0.1'

logger = logging.getLogger(__name__)

## ############################################################

def main(host, port, count=1):

    zclient = ZmqClient(host, port)
    logger.info("zclient created - {}:{}".format(host, port))

    while count > 0:
        count -= 1
        msg = b'ping'
        zclient.send(msg)
        logger.debug("message sent: '{}'".format(msg))
        msg = zclient.recv()
        logger.debug("received: {}".format(msg))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=LOCALHOST, help="Default: {}".format(LOCALHOST))
    parser.add_argument('--port', default=ZMQ_BASE_PORT, help="Default: {}".format(ZMQ_BASE_PORT))
    parser.add_argument('--count', default=1, help="Default: 1")
    args = parser.parse_args()

    logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')

    host = args.host
    port = int(args.port)
    count = int(args.count)

    main(host, port, count)

    logger.info('done.')
