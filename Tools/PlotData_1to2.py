'''
Tool used to update pickle'd OREUtils v1 plot data to JSON'd OREUtils v2 data.
'''

import sys
import pickle

class PlotStatus2:
	FREE     = 0
	CLAIMED  = 1
	RESERVED = 2

def Plot2_CoordStr(X, Y):
	return "Plot_%s_%s" % (X, Y)

def LoadData1(Path):
	try:
		File = open(Path, "rb")

		return pickle.load(File)

	except:
		return None

def ConvertData(Plots, Players):
	OutData = {}

	OutData["Plots"] = {}

	for Coords, Plot in Plots.iteritems():
		X = Coords[0]
		Y = Coords[1]

		PlotTag = Plot2_CoordStr(X, Y)		

		OutData["Plots"][PlotTag] = {}

		if Plot[0] == False:
			Status = PlotStatus2.FREE
	
			OutData["Plots"][PlotTag]["status"] = Status

		else:
			Status = PlotStatus2.CLAIMED

			Owner = Plot[0]
			Index = Plot[1]
			Date  = Plot[2]

			OutData["Plots"][PlotTag]["status"] = Status
			OutData["Plots"][PlotTag]["owner"]  = Owner
			OutData["Plots"][PlotTag]["date"]   = Date

	OutData["Players"] = {}

	for Name, Info in Players.iteritems():
		NumPlots = len(Info[0])
		MaxPlots = Info[1]
		
		RemPlots = MaxPlots - NumPlots

		OutData["Players"][Name] = {}

		OutData["Players"][Name]["remPlots"] = RemPlots

	OutData["Size"] = {}

	OutData["Size"]["radius"] = 20
	OutData["Size"]["x"]      = 256
	OutData["Size"]["y"]      = 256

	OutData["Size"]["pos"] = {}

	OutData["Size"]["pos"]["x"] = 0
	OutData["Size"]["pos"]["y"] = 16
	OutData["Size"]["pos"]["z"] = 0

	return OutData

def SaveNode2(File, Node, Embed=0):
	File.write("{\n")

	for Item, Value in Node.iteritems():
		File.write(("\t" * Embed) + "'" + str(Item) + "' : ")

		if isinstance(Value, dict):
			SaveNode2(File, Value, Embed + 1)
		else:
			File.write(repr(Value))

		File.write(",\n")

	File.write(("\t" * Embed) + "}")

def SaveData2(Path, Data):
	try:
		File = open(Path, "wb")

		SaveNode2(File, Data)

		return True

	except:
		return False

if len(sys.argv) > 1:
	InPlotPath = sys.argv[1]
else:
	InPlotPath = "Plots.xeodata"

if len(sys.argv) > 2:
	InPlayerPath = sys.argv[2]
else:
	InPlayerPath = "Players.xeodata"

if len(sys.argv) > 3:
	OutPath = sys.argv[3]
else:
	OutPath = "PlotData.json"

PlotData = LoadData1(InPlotPath)

if PlotData == None:
	print "Could not read file %s" % InPlotPath
	exit(-1)

PlayerData = LoadData1(InPlayerPath)

if PlayerData == None:
	print "Could not read file %s" % InPlayerPath
	exit(-1)

OutData = {}

try:
	OutData["ORE"] = ConvertData(PlotData, PlayerData)
except:
	print "Corrupted data"
	exit(-1)

if SaveData2(OutPath, OutData):
	print "Done!"
else:
	print "Could not save data to %s" % OutPath
