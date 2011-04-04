from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor

class MyProtocol(LineReceiver):

    def lineReceived(self, line):
        print line
        for online in self.factory.online:
            if not online is self:
                online.sendLine(line)

    def connectionMade(self):
        self.factory.online.append(self)
        print self.transport.getHost()

    def connectionLost(self, reason):
        self.factory.online.remove(self)
        

class MyFactory(ServerFactory):
    protocol = MyProtocol

    def __init__(self):
        self.online = []

if __name__ == '__main__':
    port = 1234
    print 'Server Started at port %d' % (port,)
    reactor.listenTCP(port, MyFactory())
    reactor.run()
