@event("QuitEvent")
def OnKick(event):
    print("Baiiii")

@event("ServerException")
def OnError(event):
    print("This is an error. That is a bad thing")
