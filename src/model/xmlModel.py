"XML data modelling"

class Document:
	"Classe che modellizza il documento"
	
	def __init__(self):
		self.data = []
		self.format = ""

	def addData(self, data):
		self.data.append(data)


class Data:
	"Classe di gestione dei sub data"
	def __init__(self):
		self.coords = []
		self.label = ""
		self.type = 1
		
	def addCoords(self, c):
		self.coords.append(c)

	def getCoords(self):
		return self.coords


class Coord:
	"Classe di gestione delle coordinate"
	
	def __init__(self):
		self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
		self.label, self.unit = "", ""

	def setCoord(self,x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		#print "Coords added (", self.x1,",",self.y1,")", self.x2,",", self.y2,")"


