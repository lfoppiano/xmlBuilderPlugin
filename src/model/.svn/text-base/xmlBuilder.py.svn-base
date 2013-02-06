"XML builder"

class XMLBuilder:
	"XML Builder"
	
	def __init__(self, docu):
		self.doc = docu
	
	def printXML(self):
		print self.getXML()
	
	def getXML(self):
		result = ""
		result = result + str("<?xml version='1.0' encoding='utf-8'?>\n")
	
		result = result + str("<document format=\""+str(self.doc.format)+"\">\n")

		temp_data = self.doc.data
		subdata = ""

		#retrieve coords
		for i in temp_data:
			temp_coord = i.getCoords()
	
			if i.type == 1:
				subdata = "field"
				label = ""
			elif i.type == 2:
				subdata = "choose"
				label = "label=\""+str(i.label)+"\" "
			elif i.type == 3:
				subdata = "choose"
				label = "label=\""+str(i.label)+"\" "
	
			result = result + str("\t<data "+label+"type=\""+str(i.type)+"\">\n");

			for temp in temp_coord:
				result = result +str("\t\t<"+str(subdata)+" label=\""+str(temp.label)+"\" unit=\""+str(temp.unit)+"\">\n")
				result = result + str("\t\t\t<x1>"+str(temp.x1)+"</x1>\n")
				result = result + str("\t\t\t<y1>"+str(temp.y1)+"</y1>\n")
				result = result + str("\t\t\t<x2>"+str(temp.x2)+"</x2>\n")
				result = result + str("\t\t\t<y2>"+str(temp.y2)+"</y2>\n")
				result = result + str("\t\t</"+str(subdata)+">\n")

			result = result + str("\t</data>\n")


		result = result + str("</document>")
		return result


	def writeXML(self, filename):
		#print "DEBUG: writing on file"
		file = open(str(filename)+".xml", "w")
		file.write(self.getXML())


