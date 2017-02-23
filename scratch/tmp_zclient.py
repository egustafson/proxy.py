from zmqconnector import ZmqClient

ZMQ_BASE_PORT = 19797
LOCALHOST = '127.0.0.1'

zclient = ZmqClient(LOCALHOST, ZMQ_BASE_PORT)
print("zclient created")

msg = b'ping'
zclient.send(msg)
print("message sent")
msg = zclient.recv()
print("received: {}\n".format(msg))
