import Manager
import Map
import Frontend
Map.Config      = None
Manager.Config  = None
Frontend.Config = None


def OnEnable(**kwargs):
	Map.Config      = kwargs["conf"]
	Manager.Config  = kwargs["conf"]
	Frontend.Config = kwargs["conf"]
	Frontend.InitManagers()

def OnDisable(**kwargs):
	Frontend.SaveData()

