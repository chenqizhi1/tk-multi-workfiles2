import socket, cPickle, threading
from sgtk.platform.qt import QtCore

class Server(QtCore.QObject):
    con = threading.Condition()
    working = True
    def __init__(self, ip_port):
        super(Server, self).__init__()
        self.clients = {}
        self.threads = []
        self.ip_port = ip_port

    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ip_port)
        self.sock.listen(2)

    def close(self):
        self.working = False
        try:
            self.sock.shutdown(2)
            self.sock.close()
        except socket.error as e:
            print e

    def acceptClient(self):
        while self.working:
            self.client, self.address = self.sock.accept()
            self.name = self.client.recv(1024)
            self.clients[(self.name, unicode(self.client))] = self.client
            thread = threading.Thread(target=self.messageHandle, args=(self.client, self.name))
            self.threads.append(thread)
            thread.start()

    def messageHandle(self, client, name):
        while self.working:
            try:
                msg = client.recv(1024)
                if not msg:
                    client.close()
                    del self.clients[(name, unicode(client))]
                    return
                data = cPickle.loads(msg)
                self.mainRun(name, client, data)
            except Exception as e:
                print e
                return

    def mainRun(self, name, client, data):
        func, arg = data.items()[0]
        print func, arg
        run_func = u'self.{0}({1})'.format(func, arg, unicode(client), name)
        eval(run_func)
        client.send(u'Q')