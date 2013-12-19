import Manager
import Map
import Frontend

def OnEnable(**kwargs):
	Frontend.InitManagers(**kwargs)

def OnDisable(**kwargs):
	Frontend.SaveData()
