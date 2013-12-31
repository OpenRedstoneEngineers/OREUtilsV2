@event("PythonException")
def onPythonError(event):
	API.Logger.Severe(str(event))
