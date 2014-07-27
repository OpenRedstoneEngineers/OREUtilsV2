OREUtilsV2
==========

This is a plugin, written by the Open Redstone Engineers, to take care of various things on the ORE servers. It's mostly written in Python, though performance critical code such as world generation is taken care of by the OTJP, ORE's Tiny Java Plugin.

This readme file is still a work in progress.

## Dependencies
* PythonLoader
* PermissionEx
* WorldEdit
* DBPassword

## Components

### OREPyUtils (Python)
* **Plots"*: This is our plot system. It includes an automatically generated plot map, as well as useful plot related functionality.
* **CommandGen**: This takes care of simple commands which are basically just aliases for simple commands. It generates commands from Data/Commands.txt.
* **IRCBot**: This includes an IRC bot, and is designed to deliver both cross server chat if you have multiple servers, and allowing users to chat with those on the server from IRC clients.
* **UsefulCommands**: A bundle of useful commands.
* **NameSystem**: A system for letting users decide for themselves how their name should be coloured, without giving them access to the power of /nick.
* **Derps**: A utility for telling everyone that you fucked up ("derped").
* **FunCommands**: Various commands, mostly for fun.

### OTJP** (Java)
* **Plot World**: World generator to generate a world of 256x256 plots.

## Config

### OREUtils
OREUtils reads the config file Data/config.json. It's not there by default; however, the example config file Data/config.example.json is. Therefore, before you start, copy Data/config.example.json to Data/config.json.

There are two ways to edit OREUtils' configuration. The recommended way is using the command '/property' in game like this: `/property [name] [value]`, for example `/property IRC.Name 'OREBot'`. The other way is to edit the config file directly. Make sure that the server is offline before you directly edit the config file. If you don't, your changes will be lost.

Now that that's out of the way, here's the various config options and their meaning:

* **Include**: Contains which modules should be included. If a module is included, its config value is 1, if not, it's 0.
* **IRC**: Contains configs related to the IRC module.
	* **IRC.Server**: Which IRC server to connect to.
	* **IRC.Chan**: Which IRC channel to connect to.
	* **IRC.Name**: The name of the IRC bot.
	* **IRC.NamePass**: IRC password, for NickServ.
	* **IRC.Port**: IRC port.
* **PlotMap**: Contains configs related to the plot system.
	* **PlotMap.BottomBlocks**: Contains which blocks should be below the top layer of the plot map. Blocks are defined like this: [ID,Data,Physics]. You probably won't need to care about that last value; it's for very advanced uses.
			* **PlotMap.BottomBlocks.Reserved**: Which block should be below the top layer under a reserved plot. 
			* **PlotMap.BottomBlocks.On**: Which block should be below the top layer under a claimed plot.
			* **PlotMap.BottomBlocks.Off**: Which block should be below the top layer under an unclaimed plot.
	* **PlotMap.TopBlocks**: Contains which blocks should be in the top layer of the plot map.
			* **PlotMap.TopBlocks.Reserved**: Which block should represent a reserved plot.
			* **PlotMap.TopBlocks.On**: Which block should represent a claimed plot.
			* **PlotMap.TopBlocks.Off**: Which block should represent an unclaimed plot.
			* **PlotMap.TopBlocks.Base**: Which block the base should consist of.
			* **PlotMap.TopBlocks.Frame**: Contains which blocks the frame should consist of.
				* **PlotMap.TopBlocks.Frame.X**: Which block should be on the frame's X.
				* **PlotMap.TopBlocks.Frame.Y**: Which block should be on the frame's Y.
				* **PlotMap.TopBlocks.Frame.Cross**: Which block should be on the frame's cross.

### Permission Nodes
* **ore.config**: Access to the `/property` command to edit the config file.

~TODO

## Usage

### Plots
All commands related to the plot system start with a `p`. Many commands do something with the plot you're currently on. Those commands can be used either on the plot map, or on an actual plot in the world.

* **User Commands**
	* **pclaim**: Claim the plot you're standing on.
	* **punclaim**: Unclaim the plot you're standing on.
	* **pinfo**: Get info about the plot you're standing on.
	* **ploc**: Alias for pinfo.
	* **pwarp**: Warp from the plot you're standing on from the plot map to the actual plot in the world.
	* **pwarp [name]**: Warp to someone's plot.
	* **pmap**: Warp from a real world plot to the plot's representation on the plot map.
	* **pmap [name]**: Warp to someone's plot's representation on the plot map.
	* **psearch [name]**: Search for a member's plot.
	* **pallow [name]**: Allow someone to build on your plot.
	* **pallow ***: Allow everyone to build on your plot.
	* **punallow [name]**: Take away someone's right to build on your plot.
	* **punallow ***: Take away everyone's right to build on your plot.
* **Administrative Commands**
	* **preserve**: Reserve the plot you're standing on, so that it can't be claimed.
	* **pclaimas [name]**: Claim the plot you're standing on as someone else.
	* **pgenerate [radius]**: Regenerate teh plot map with the radius [radius]. Useful for shrinking or growing the map as needed.
	* **pgive [name] [amount]**: By default, players can claim one plot. This command gives the player more plots to claim.
	* **ptake [name] [amount]**: Remove from the number of plots a player is allowed to claim.

~TODO
