import gtk
import webkit
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install()

def file2string(_file):
        _file = open(_file)
        out = "".join(_file)
        _file.close()
        return out

class Window(gtk.Window):
    def __init__ (self):
        super(Window, self).__init__()
        self.set_default_size(400, 400)
        self.set_title("Simple Twisted chat")

        self.vbox = gtk.VBox()

        self.label = gtk.Label("Waiting...")
        self.button = gtk.Button()
        self.entry = gtk.Entry()

        self.web = webkit.WebView()
        self.web.load_html_string(file2string("index.html"), "file:///")

        self.scroll = gtk.ScrolledWindow()
        self.scroll.add(self.web)

        self.vbox.pack_start(self.label)
        self.vbox.pack_start(self.scroll)
        self.vbox.pack_start(self.entry)
        self.vbox.pack_start(self.button)

        self.add(self.vbox)

        self.button.connect("clicked", self.on_clicked)
        self.entry.connect("activate", self.on_clicked)
        self.connect("destroy", lambda x: reactor.stop())

        self.show_all()
        self.show()

    def on_clicked(self, widget):
        factory.instance.sendLine(self.entry.get_text()) 
        self.web.execute_script('createDiv("%s")' % (self.entry.get_text()), )
        self.entry.set_text("")

    def set_connected(self, string):
        self.label.set_text(string)

    def set_chat(self, string):
        #self.label1.set_text(string)
        print self.scroll.get_vscrollbar().get_value()
        self.web.execute_script('createDiv("%s")' % (string,))

class MyProtocol(LineReceiver):
    def lineReceived(seld, line):
        gui.set_chat(line)

    def connectionMade(self):
        print "Connection made"
        gui.set_connected("Connected")

    def connectionLost(self, reason):
        print "Connection Lost"
        gui.set_connected("Connection Lost")

class MyFactory(ClientFactory):
    protocol = MyProtocol

    def buildProtocol(self, addr):
        self.instance = self.protocol()
        return self.instance

if __name__ == '__main__':
    gui = Window()
    from twisted.internet import reactor
    factory = MyFactory()
    reactor.connectTCP('localhost', 1234, factory)
    reactor.run()
