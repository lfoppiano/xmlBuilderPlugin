#!/usr/bin/env python

# MODULE MINI HOWTO
# This is a small wrapper that makes plugins look like an object class that
# you can derive to create your plugin.  With this wrapper, you are pretty
# much responsible for doing everything (checking run_mode, gui, etc).  If
# you want to write a quick plugin, you probably want the gimpfu module.
#
# A plugin using this module would look something like this:
#
#   import gimp, gimpplugin
#
#   pdb = gimp.pdb
#
#   class myplugin(gimpplugin.plugin):
#       def query(self):
#           gimp.install_procedure("plug_in_mine", ...)
#
#       def plug_in_mine(self, par1, par2, par3,...):
#           do_something()
#
#   if __name__ == '__main__':
#       myplugin().start()

import sys
import os

path = os.path.abspath(os.path.dirname(sys.argv[0]))
if os.path.isdir(path):
    sys.path.append(path)

sys.path.append(path+str('/model'))
import xmlBuilder
import xmlModel

sys.path.append(path+str('/util'))
from util import *
from dialogs import *

import gimp, gimpplugin
import pygtk
pygtk.require("2.0")

import gtk
from gimpenums import *
import gtk.glade

pdb = gimp.pdb

del(path)


class myplugin(gimpplugin.plugin):

    def __init__(self):
        # initialisation routines
        # called when gimp starts.
        print "hello world \o/"
        self.reference_coord = -1
        self.doc = xmlModel.Document()

        self.coords = []
        self.count = 0

        self.entries = []
        self.labels = []
        
        self.name = "mainWindow"
        self.gladefile = os.path.join(os.path.abspath(sys.path[0]),"view/gui.glade")
        self.widgets = WidgetWrapper(gtk.glade.XML(self.gladefile,'mainWindow'))

        dic = {\
            "on_AddGroupButton_clicked": self.add_group_coord,\
            "on_CloseGroupButton_clicked": self.close_group_coord,\
            "on_AddCoordButton_clicked": self.add_coord,\
            "on_RemoveButton_clicked": self.remove_item,\
            "on_ExitButton_clicked": self.destroy,\
            "on_SaveButton_clicked": self.save_xml,\
            "on_gotRelativeCoordButton_clicked": self.got_relative_coords\
            }

        self.widgets.signal_autoconnect(dic)

        self.viewport = self.widgets["viewport"]

        self.treestore = gtk.TreeStore(str)
        self.tree = gtk.TreeView(self.treestore)

        self.tvcolumn = gtk.TreeViewColumn('Coordinates')

        self.tree.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.tree.set_search_column(0)
        self.tvcolumn.set_sort_column_id(0)
        self.tree.set_reorderable(True)

        self.viewport.add(self.tree)
        self.viewport.show_all()


    def reload_list(self):
        self.treestore.clear()

        data = self.doc.data
        
        for x in data:
            current_data = self.treestore.append(None, ['group %s type=%s' %(x.label,x.type)])
            for y in x.coords: 
                self.treestore.append(current_data, ['coord %s: (%i, %i)(%i, %i )' %(y.label, y.x1, y.y1, y.x2, y.y2)])

    def get_selected_item(self):
        s = self.tree.get_selection()
        (model,iterator) = s.get_selected()     
        if iterator != None:
            if model.iter_is_valid(iterator):               
                (selected,) = model.get(iterator,0)
                return selected
            else:
                return None
        else:
            return None


## Callbacks

    def add_group_coord(self, widget):
        print "add group coordinate"
        self.data = xmlModel.Data()
        self.widgets["AddGroupButton"].set_sensitive(False)
        
        a = GroupCoordDialog()
        (res, return_data) = a.run()
        
        if res == gtk.RESPONSE_OK:
            self.data.label = return_data[1]
            self.data.type = int(return_data[2])
            self.reload_list()
            self.widgets["CloseGroupButton"].set_sensitive(True)
            self.widgets["AddCoordButton"].set_sensitive(True)
            self.widgets["gotRelativeCoordButton"].set_sensitive(False)

        elif res == gtk.RESPONSE_CANCEL:
            self.widgets["AddGroupButton"].set_sensitive(True)
            self.widgets["CloseGroupButton"].set_sensitive(False)
            self.widgets["AddCoordButton"].set_sensitive(False)


    def close_group_coord(self, widget):
        print "closing group coordinate"
        self.doc.addData(self.data)
        del self.data
        self.widgets["CloseGroupButton"].set_sensitive(False)
        self.widgets["AddGroupButton"].set_sensitive(True)
        self.widgets["AddCoordButton"].set_sensitive(False)
        self.reload_list()
                    

    def add_coord(self, widget):
        print "add coordinate", self.drawable.mask_bounds
        
        self.widgets["AddCoordButton"].set_sensitive(False)
        self.coord = xmlModel.Coord()
        b = CoordDialog()
        b.set_coord(self.drawable.mask_bounds)

        (res, return_data) = b.run()
        if res == gtk.RESPONSE_OK:
            if self.drawable:
                self.coord.label=return_data[1]
                self.coord.unit=return_data[2]
                if self.reference_coord == -1:
                    self.coord.setCoord(self.drawable.mask_bounds[0], 
                        self.drawable.mask_bounds[1], 
                        self.drawable.mask_bounds[2], 
                        self.drawable.mask_bounds[3])
                else:
                    self.coord.setCoord(int(self.drawable.mask_bounds[0])-int(self.reference_coord[0]), 
                        int(self.drawable.mask_bounds[1])-int(self.reference_coord[1]),
                        int(self.drawable.mask_bounds[2])-int(self.reference_coord[0]),
                        int(self.drawable.mask_bounds[3])-int(self.reference_coord[1]))

                self.data.addCoords(self.coord)
                if self.data.type == 1:
                    self.close_group_coord(None)
                del self.coord
                self.widgets["AddCoordButton"].set_sensitive(True)
                
            self.reload_list()

        elif res == gtk.RESPONSE_CANCEL:
            self.widgets["AddCoordButton"].set_sensitive(True)
                    

    
    def remove_item(self, widget):
        print "removing coordinate"
        self.doc.data.pop()
        self.reload_list()

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()


    def delete_event(self, widget, data=None):
        print "delete event occurred"

        return False

    def save_xml(self, widget):
        chooser = gtk.FileChooserDialog(title="Save XML",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        chooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("XML")
        filter.add_mime_type("text/xml")
        filter.add_pattern("*.xml")
        chooser.add_filter(filter)

        response = chooser.run()
 
        if response == gtk.RESPONSE_OK:
            self.doc.format = self.widgets["formatEntry"].get_text()
            builder = xmlBuilder.XMLBuilder(self.doc)
            builder.writeXML(chooser.get_filename())
        
        chooser.destroy()

    def got_relative_coords(self, widget):
        self.reference_coord = self.drawable.mask_bounds
        self.widgets["relativeCoordsLabel"].set_label("("+str(self.drawable.mask_bounds[0])+", "+str(self.drawable.mask_bounds[1])+")")


## Plugin infos and methods
    
    
    def quit(self):
        # clean up routines
        # called when gimp exits (normally).
        print "bye world <o>"



    def xmlBuilderMain(self, id, image, drawable):
        # do what ever this plugin should do
        print "I'm running"
        self.image = image
        self.drawable = drawable
        gtk.main()



    def query(self):
        # called to find what functionality the plugin provides.
        gimp.install_procedure("xmlBuilderMain", 
                                "help", 
                                "", 
                                "Luca 'whitenoise' Foppiano <luca@foppiano.org>", 
                                "Copyright (c) 2007 Luca 'whitenoise' Foppiano <luca@foppiano.org", 					   "18/01/2008", 
                                "<Image>/OCR/xmlBuilder...",
                                "", 
                                PLUGIN, 
                                [(PDB_INT32, "run_mode", "Run mode"),
                                (PDB_IMAGE, "image", "Image"),
                                (PDB_DRAWABLE, "drawable", "Drawable")], 
                                [])	

if __name__ == '__main__':
    myplugin().start()

