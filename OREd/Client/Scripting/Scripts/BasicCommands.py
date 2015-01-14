@command('raw')
def OnCommandRaw(*args):
    API.Console.Send(' '.join(args))


@command('cmd')
def OnCommand(*args):
    API.Console.Command(' '.join(args))


@event('Join')
def OnCommand(event):
    print('JOIN EVENT: ' + repr(event))
