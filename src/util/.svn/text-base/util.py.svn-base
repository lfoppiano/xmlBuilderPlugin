class WidgetWrapper:
	"""
	Wrapper to get widgets as of w["widget_name"].actions()
	Thanks to Giacomo 'j-doe' Bagnoli http://jdoe.netsons.org/tdm/
    	"""
    	def __init__(self,wTree) :
        	self.widgets = wTree
        
    	def __getitem__(self, key):
        	return self.widgets.get_widget(key)
    
    	def signal_autoconnect(self,dic):
        	self.widgets.signal_autoconnect(dic)


