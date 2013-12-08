# Channel-based chat
#
# -Dot

from collections import defaultdict

from Helper import color

MAX_CHANNELS = 10

class ChannelMode:
    PUBLIC   = 0
    PASSWORD = 1

class Channel:
    def __init__(self, mode):
        self.mode    = mode
        self.players = []

channels       = defaultdict(list)
active_channel = defaultdict(str)

def join(player, channelName):
    if player in channels[channelName]:
        return False

    channels[channelName].append(player)

    channel_join_msg(channelName, player.getName())

    active_channel[player.getName()] = channelName

    return True

def leave(player, channelName):
    if player not in channels[channelName]:
        return False

    channels[channelName].remove(player)

    channel_left_msg(channelName, player.getName())

    if active_channel[player.getName()] == channelName:
        del active_channel[player.getName()]

    if len(channels[channelName]) == 0:
        del channels[channelName]

    return True

def leave_all(player):
    for chanName, playerList in channels.iteritems():
        if player in playerList:
            playerList.remove(player)

            channel_left_msg(chanName, player.getName()) 

def channel_broadcast_raw(channelName, message):
    if channelName not in channels:
        return False

    for player in channels[channelName]:
        player.sendMessage(message)

    return True

def channel_player_msg(channelName, senderName, message):
    msg_str = "["+channelName+"] "+senderName+": "+message

    return channel_broadcast_raw(channelName, msg_str)

def channel_join_msg(channelName, playerName):
    msg_str = "["+channelName+"] "+playerName+" has joined the channel"

    return channel_broadcast_raw(channelName, msg_str)

def channel_left_msg(channelName, playerName):
    msg_str = "["+channelName+"] "+playerName+" has left the channel"

    return channel_broadcast_raw(channelName, msg_str)

@hook.command("cchat", usage = "/<command> <join|leave|info|switch> <channel>")
def onCommandCChat(sender, args):
    if len(args) != 2:
        return False

    cmd  = args[0]
    chan = args[1]

    if cmd == "join":
        if join(sender, chan):
            sender.sendMessage("Welcome to channel " + color("9") + chan)

        else:
            sender.sendMessage(color("c") + "You are already in that channel")

        return True

    elif cmd == "leave":
        if leave(sender, chan):
            sender.sendMessage("You have left the channel")

        else:
            sender.sendMessage("You are not in that channel")

        return True

    elif cmd == "info":
        if chan not in channels:
            sender.sendMessage("No such channel")
            return True

        player_list_msg = ', '.join([x.getName() for x in channels[chan]])

        sender.sendMessage("Players in channel "+chan+": "+player_list_msg) 

        return True

    elif cmd == "switch":
        if chan not in channels:
            sender.sendMessage("No such channel")
            return True

        if sender not in channels[chan]:
            sender.sendMessage("You are not in that channel")
            return True

        active_channel[sender.getName()] = chan

        return True
    
    return False

@hook.command("ccadmin", usage = "/<command> <list|playerinfo|kick>")
def onCOmmandCCAdmin(sender, args):
    if not sender.hasPermission("ore.cchat.admin"):
        sender.sendMessage("No permission")
        return True

    if len(args) == 0:
        return False

    cmd = args[0]

    if cmd == "list":
        sender.sendMessage("Active channels:")

        for chan in channels:
            sender.sendMessage(chan)

        return True

    elif cmd == "playerinfo":
        if len(args) != 2:
            sender.sendMessage("Usage: /ccadmin playerinfo <player>")
            return True

        for channelName, playerList in channels.iteritems():
            for player in playerList:
                if player.getName() == args[1]:
                    sender.sendMessage(channelName)

        return True

    elif cmd == "kick":
        if len(args) != 3:
            sender.sendMessage("Usage: /ccadmin kick <player> <channel>")
            return True

        chan = channels.get(args[2])

        if chan == None:
            sender.sendMessage("No such channel")
            return True

        for player in chan:
            if player.getName() == args[1]:
                player.sendMessage("You have been kicked from channel " + args[2])
                sender.sendMessage("Kicked player")

                chan.remove(player)

        return True

    return False

@hook.command("cc", usage="/<command> <message>")
def onCommandCC(sender, args):
    msg = ' '.join(args)

    channelName = active_channel.get(sender.getName())

    if channelName == None or channelName == "":
        sender.sendMessage("You are not in a channel")
        return True

    channel_player_msg(channelName, sender.getName(), msg)

    return True

@hook.event("player.PlayerQuitEvent", "monitor")
def onEventQuit(event):
    leave_all(event.getPlayer())

    if event.getPlayer().getName() in active_channel:
        del active_channel[event.getPlayer().getName()]
