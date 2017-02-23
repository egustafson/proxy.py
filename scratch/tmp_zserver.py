from zmqconnector import ZmqServer

ZMQ_BASE_PORT = 19797
LOCALHOST = '127.0.0.1'

zserver = ZmqServer(LOCALHOST, ZMQ_BASE_PORT)
print("zserver created")

while True:
    msg = zserver.recv()
    print("received:  {}\n".format(msg))
    zserver.send(msg)
