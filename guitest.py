import webkit
import gtk

def file2string(_file):
    _file = open(_file)
    out = "".join(_file)
    _file.close()
    return out

class Window(gtk.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.set_default_size(300,300)
        self.set_title("Simple Twisted chat")

        self.vbox = gtk.VBox()

        self.html = webkit.WebView()
        self.scroll = gtk.ScrolledWindow()
        self.scroll.add(self.html)

        self.html.load_html_string(file2string("index.html"), "file:///")

        self.button = gtk.Button()

        self.vbox.pack_start(self.scroll)
        self.vbox.pack_start(self.button)

        self.add(self.vbox)

        self.show_all()
        self.show()

        self.button.connect("clicked", self.on_clicked)

    def on_clicked(self, widget):
        self.html.execute_script('createDiv("hola")')


if __name__ == '__main__':
    Window()
    gtk.main()
