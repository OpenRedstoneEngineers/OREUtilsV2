import Manager
import Map
import Frontend
Frontend.Config = None

def OnEnable(**kwargs):
	Frontend.Config = kwargs["conf"]
	Frontend.InitManagers()

def OnDisable(**kwargs):
	Frontend.SaveData()

