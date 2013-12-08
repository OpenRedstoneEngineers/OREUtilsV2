from __future__ import division 

from Helper import Sudo 

import org.bukkit.Bukkit.dispatchCommand as dispatchCommand 
import org.bukkit.Bukkit.getPlayerExact  as getPlayerExact

# Permission nodes: 
# ore.nameformat.others

#Xeo's nameformat

# Color Whitelist
colours = '123456789abcdef'

# Format Whitelist
formats = 'lmo'

# Presets
preset = {
    'rainbow'   : '4c6e23915d',
    'ice'       : 'f7b3b7f',
    'greyscale' : '87f',
    'england'   : 'f4f4f4f4f4f4f4f4f4f',
    'pink'      : 'dl',
    'reset'     : 'f',
    'fire'      : 'e646e'
}

# Distribute colours
def dist(nam, col):
    nlen = len(nam)
    clen = len(col)
 
    if clen > nlen:
        col  = col[:nlen]
        clen = nlen
    
    cof = str(col)    

    for i in formats: 
        cof = cof.replace(i, '')
    
    a   = round(nlen / len(cof), 4)
    nam = list(nam)
    col = list(''.join(col))

    while 1:
        if nlen < 1:
            return ''.join(nam)
        
        nlen -= a

        while 1:
            if len(col) > 0 and col[-1] in formats:
                nam.insert(int(nlen), '&' + col.pop())
            else:
                break    

        if len(col) > 0:
            if col[-1] in colours:
                nam.insert(int(nlen), '&' + col[-1])

            col.pop()

# Nameformat
@hook.command('nameformat', usage='/nameformat <colors & formats>')
def onCommandNameformat(sender, args):
    # Search for presets
    for i, v in enumerate(args):
        temp = preset.get(v)

        if temp != None:
            args[i] = temp

    if len(args) == 0: 
        return False

    # Find the receiver
    if getPlayerExact(args[0]) != None and sender.hasPermission('ore.nameformat.others'):
        receiver = getPlayerExact(args.pop(0)).getName()
    else:
        receiver = sender.getName()

    colorSeq = ''.join(args)

    if len(colorSeq) == 0: 
        return False

    # Check if the specified colors/formats are allowed
    for i in colorSeq:
        if i not in colours + formats:
            sender.sendMessage('Issue found: ' + i)

            return False

    # Change player's display name
    sudo(' '.join(['nick', receiver, dist(receiver, colorSeq)]))

    sender.sendMessage('Nickname changed!')

#rankdown
@hook.command("rankup", description="Promote a user.")
def onCommandRankup(sender, args):
    if len(args) == 1:
        dispatchCommand(sender, "pex promote "+args[0])
        return True

    return False

#rankdown
@hook.command("rankdown", description="Demote a user.")
def onCommandRankdown(sender,args):
    if len(args) == 1:
        dispatchCommand(sender, "pex demote "+args[0])
        return True

    return False

#fixname
@hook.command('fixname', description='Fix your name formatting.')
def onCommandFixname(sender,args):
    sudo('nick '+sender.getName()+' off')
    return True
