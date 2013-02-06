from util import *

import gtk
import gtk.glade
import os, sys

    
class GroupCoordDialog:
    "Run a dialog to add groups of coordinates"

    def __init__(self):
        self.name = "groupDialog"
        self.gladefile = os.path.join(os.path.abspath(sys.path[0]),"view/gui.glade")
        self.widgets = WidgetWrapper(gtk.glade.XML(self.gladefile,self.name))
        
        self.dlg = self.widgets[self.name]
        self.dlg.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK)
        
        vbox2=self.widgets["vbox2"]
        self.button = gtk.RadioButton(None, "field")
        self.button.connect("toggled", self.callback, "1")
        self.button.set_active(True)
        vbox2.pack_start(self.button, True, True, 0)
        self.button.show()
        self.type_selected = 1

        self.button = gtk.RadioButton(self.button, "single multichoose")
        self.button.connect("toggled", self.callback, "2")
        vbox2.pack_start(self.button, True, True, 0)
        self.button.show()

        self.button = gtk.RadioButton(self.button, "multi multichoose")
        self.button.connect("toggled", self.callback, "3")
        vbox2.pack_start(self.button, True, True, 0)
        self.button.show()
        self.result = None


    def run(self):
        self.result = self.dlg.run()
        res = (self.result,\
            self.widgets["label"].get_text(),\
            self.type_selected)
        self.dlg.destroy()
        self.data = str(res[1])+" - "+str(res[2])

        return (self.result,res)


    def callback(self, widget, data="none"):
        self.type_selected = int(data)
        if self.type_selected == 1:
            self.widgets["label"].set_sensitive(False)
        else:
            self.widgets["label"].set_sensitive(True)


class CoordDialog:
    "Run a dialog to add coordinates"

    def __init__(self):
        self.name = "coordDialog"
        self.gladefile = os.path.join(os.path.abspath(sys.path[0]),"view/gui.glade")
        self.widgets = WidgetWrapper(gtk.glade.XML(self.gladefile,self.name))
        
        self.dlg = self.widgets[self.name]
        self.dlg.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK)
        
        self.result = None


    def run(self):
        self.result = self.dlg.run()
        res = (self.result,\
            self.widgets["coordLabel"].get_text(),\
            self.widgets["coordUnit"].get_text())
        self.dlg.destroy()

        return (self.result,res)


    def set_coord(self, coords):
        string = "("+str(coords[0])+","+str(coords[1])+")("+str(coords[2])+","+str(coords[3])+")"
        self.widgets["coordSelected"].set_label(string)



