import Manager
import Map
import Frontend

def OnEnable(**kwargs):
	Frontend.InitManagers()

def OnDisable(**kwargs):
	Frontend.SaveData()

