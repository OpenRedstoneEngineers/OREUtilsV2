from __future__ import print_function

import sys
import uuid
import urllib
import json
import time

import PersistentData


def name_to_uuid(name, page="https://api.mojang.com/users/profiles/minecraft/"):
	while True:
		path = page + name
		url = urllib.urlopen(path)
		NS = uuid.UUID('80c336a2-2226-11e4-89e8-0401211ac001')
		text = url.read()
		try:
			jdata = json.loads(text)
		except ValueError:
			ret = uuid.uuid5(NS, name)
			return ret
		try:
			ret = str(uuid.UUID(jdata["id"]))
			return ret
		except KeyError:
			if "TooManyRequestsException" in text:
				print("TooManyRequestsException, waiting 5 seconds", file=sys.stderr)
				error = 1
				time.sleep(5)
			else:
				ret = uuid.uuid5(NS, name)
				return ret

if __name__ == "__main__":

	if len(sys.argv) > 1:
		path = sys.argv[1]
	else:
		path = "PlotData.json"


	old = PersistentData.NodeFile(path)
	new = PersistentData.NodeFile('output.json')
	
	new.node.Ensure("ORE")
	new.node.ORE.Ensure("Size")
	new.node.ORE.Size = old.node.ORE.Size
	new.node.ORE.Ensure("Plots")
	new.node.ORE.Ensure("Players")

	for player in old.node.ORE.Players:
		u = name_to_uuid(str(player))
		new.node.ORE.Players.Ensure(str(u)).Ensure("Name", str(player))
		new.node.ORE.Players.Ensure(str(u)).Ensure("remPlots", int(old.node.ORE.Players[player].remPlots))

	for plot in old.node.ORE.Plots:
		new.node.ORE.Plots.Ensure(plot).Ensure("status", int(old.node.ORE.Plots[plot].status))
		if new.node.ORE.Plots.Ensure(plot).status == 0:
			continue
		new.node.ORE.Plots.Ensure(plot).Ensure("ownerid", name_to_uuid(str(old.node.ORE.Plots[plot].owner)))
		new.node.ORE.Plots.Ensure(plot).Ensure("date", str(old.node.ORE.Plots[plot].date))

	new.Dump()
