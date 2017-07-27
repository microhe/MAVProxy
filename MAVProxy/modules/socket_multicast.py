import socket
import struct
import threading


class SocketMulticast(threading.Thread):
    def __init__(self, multicast_ip, multicast_port):
        threading.Thread.__init__(self)
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port

    def init_receive(self, on_data):
        self.on_data = on_data
        self.rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                      socket.IPPROTO_UDP)
        self.rec_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rec_sock.bind(('', self.multicast_port))
        mreq = struct.pack("4sl",
                           socket.inet_aton(self.multicast_ip),
                           socket.INADDR_ANY)

        self.rec_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                 mreq)

    def init_sender(self):
        self.sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                         socket.IPPROTO_UDP)
        self.sender_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,
                                    2)

    def run(self):
        while True:
            rec_data = self.rec_sock.recv(10240)
            self.on_data(rec_data)

    def send(self, data):
        self.sender_sock.sendto(data, (self.multicast_ip, self.multicast_port))


def on_data(data):
    print("receive: " + data)


if __name__ == '__main__':
    socketMulticast = SocketMulticast('224.1.1.1', 5000)
    socketMulticast.init_sender()
    socketMulticast.init_receive(on_data)
    socketMulticast.start()
    while True:
        data = raw_input("input: ")
        socketMulticast.send(data)
