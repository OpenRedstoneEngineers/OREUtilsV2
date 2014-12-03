/**
 *  ORE's Tiny Java Plugin
 *  Copyright (C) 2013-2014 OpenRedstone
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package org.openredstone.plot;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import org.bukkit.Location;
import org.bukkit.Server;
import org.bukkit.World;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.java.JavaPlugin;

import org.openredstone.OTJP;

public class PlotServer {
    private HashMap<String, PlotMap> managers;

    private final int DEFAULT_RADIUS = 5;
    private final int DEFAULT_SIZEX = 256;
    private final int DEFAULT_SIZEY = 256;

    public PlotServer(JavaPlugin plugin) {
        this.managers = new HashMap<String, PlotMap>();

        plugin.getCommand("pusers").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    sender.sendMessage("Not a player!");
                    return true;
                }

                Player player = (Player) sender;
                PlotManager manager = getOrCreateManager(player.getWorld());
                HashMap<UUID, PlotUser> users = manager.getUsers();

                if (users.isEmpty()) {
                    player.sendMessage("No users!");
                    return true;
                }

                StringBuilder builder = new StringBuilder("Users:");
                for (PlotUser user : users.values()) {
                    builder.append(" " + user.getLastName());
                }

                player.sendMessage(builder.toString());
                return true;
            }
        });

        plugin.getCommand("pgive").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    sender.sendMessage("Not a player!");
                    return true;
                }

                if (!sender.hasPermission("ore.plot.give")) {
                    sender.sendMessage("No permission!");
                    return true;
                }

                if (args.length == 0) {
                    return false;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                PlotUser user = manager.findUserMatch(args[0]);
                if (user == null) {
                    sender.sendMessage("Could not find player!");
                    return true;
                }

                if (args.length > 1) {
                    try {
                        user.setRemPlots(user.getRemPlots() + Integer.parseInt(args[1]));
                    } catch (NumberFormatException e) {
                        return false;
                    }
                } else {
                    user.setRemPlots(user.getRemPlots() + 1);
                }

                sender.sendMessage("User " + args[0] + " can now claim " + user.getRemPlots() + " more plots.");
                return true;
            }
        });

        plugin.getCommand("ptake").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    sender.sendMessage("Not a player!");
                    return true;
                }

                if (!sender.hasPermission("ore.plot.give")) {
                    sender.sendMessage("No permission!");
                    return true;
                }

                if (args.length == 0) {
                    return false;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                PlotUser user = manager.findUserMatch(args[0]);
                if (user == null) {
                    sender.sendMessage("Could not find player!");
                    return true;
                }

                if (args.length > 1) {
                    user.setRemPlots(user.getRemPlots() - Integer.parseInt(args[1]));
                } else {
                    user.setRemPlots(user.getRemPlots() - 1);
                }

                if (user.getRemPlots() < 0) {
                    sender.sendMessage("User already at zero plots!");
                    user.setRemPlots(0);
                } else {
                    sender.sendMessage("User " + args[0] + " can now claim " + user.getRemPlots() + " more plots.");
                }
                return true;
            }
        });

        plugin.getCommand("psearch").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    sender.sendMessage("Not a player!");
                    return true;
                }

                if (args.length != 1) {
                    return false;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                String match = args[0].toLowerCase();
                sender.sendMessage("Matches for owner:");
                for (Map.Entry<Plot.Pos, Plot> it : manager.getPlots().entrySet()) {
                    Plot plot = it.getValue();
                    if (plot.isClaimed()) {
                        if (plot.getOwnerName().toLowerCase().contains(match)) {
                            Plot.Pos pos = it.getKey();
                            sender.sendMessage(manager.getInfo(pos.x, pos.z));
                        }
                    }
                }

                sender.sendMessage("Matches for reason:");
                for (Map.Entry<Plot.Pos, Plot> it : manager.getPlots().entrySet()) {
                    Plot plot = it.getValue();
                    if (plot.isClaimed()) {
                        String reason = plot.getReason();
                        if (reason != null && reason.toLowerCase().contains(match)) {
                            Plot.Pos pos = it.getKey();
                            sender.sendMessage(manager.getInfo(pos.x, pos.z));
                        }
                    }
                }

                return true;
            }
        });

        plugin.getCommand("pinfo").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    sender.sendMessage("Not a player!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPosMatch(manager, player, args, pos);
                if (nextArg < 0) {
                    sender.sendMessage("Unknown plot!");
                }

                OTJP.sendInfo(sender, manager.getInfo(pos.x, pos.z));
                return true;
            }
        });

        plugin.getCommand("pmapmove").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                if (!sender.hasPermission("ore.plot.mapmove")) {
                    OTJP.sendError(sender, "No permission!");
                    return true;
                }

                if (args.length != 3) {
                    return false;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                int newX, newY, newZ;
                try {
                    newX = Integer.parseInt(args[0]);
                    newY = Integer.parseInt(args[1]);
                    newZ = Integer.parseInt(args[2]);
                } catch (NumberFormatException e) {
                    return false;
                }

                manager.setMapPos(newX, newY, newZ);
                manager.generate();

                OTJP.sendInfo(sender, "Plot map moved to " + args[0] + ", " + args[1] + ", " + args[2]);
                return true;
            }
        });

        plugin.getCommand("pgenerate").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                if (!sender.hasPermission("ore.plot.generate")) {
                    OTJP.sendError(sender, "No permission!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                if (args.length > 0) {
                    try {
                        int radius = Integer.parseInt(args[0]);

                        manager.setRadius(radius); // TODO: Remove invalid plots
                    } catch (NumberFormatException e) {}
                }

                manager.generate();

                OTJP.sendInfo(sender, "Generated " + manager.getNumPlots() + " plots");
                return true;
            }
        });

        plugin.getCommand("preserve").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                if (!sender.hasPermission("ore.plot.reserve")) {
                    OTJP.sendError(sender, "No permission!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPos(manager, player, args, pos);
                if (nextArg < 0) {
                    OTJP.sendError(sender, "Unknown plot!");
                    return true;
                }

                String reason = null;
                if (nextArg < args.length) {
                    reason = args[nextArg];
                }

                try {
                    manager.reserve(pos.x, pos.z, player.getName(), player.getUniqueId(), reason);
                } catch (PlotException e) {
                    OTJP.sendError(sender, e.getMessage());
                    return true;
                }

                manager.markReserved(pos.x, pos.z);

                OTJP.sendInfo(sender, "Reserved plot " + pos.x + ", " + pos.z);
                return true;
            }
        });

        plugin.getCommand("pclaim").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPos(manager, player, args, pos);
                if (nextArg < 0) {
                    OTJP.sendError(sender, "Unknown plot!");
                    return true;
                }

                String reason = null;
                if (nextArg < args.length) {
                    reason = args[nextArg];
                }

                try {
                    manager.claim(pos.x, pos.z, player.getName(), player.getUniqueId(), reason);
                } catch (PlotException e) {
                    OTJP.sendError(sender, e.getMessage());
                    return true;
                }

                manager.markClaimed(pos.x, pos.z);

                OTJP.sendInfo(sender, "Claimed plot " + pos.x + ", " + pos.z);
                return true;
            }
        });

        plugin.getCommand("pclaimas").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                if (!sender.hasPermission("ore.plot.claimas")) {
                    OTJP.sendError(sender, "No permission!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPos(manager, player, args, pos);
                if (nextArg < 0) {
                    OTJP.sendError(sender, "Unknown plot!");
                    return true;
                }

                String owner = args[nextArg + 1];
                if (nextArg >= args.length) {
                    return false;
                }

                String reason = null;
                if (nextArg + 1 < args.length) {
                    reason = args[nextArg];
                }

                UUID ownerUUID = manager.getUserUUID(owner);
                if (ownerUUID == null) {
                    OTJP.sendError(sender, "Could not find player!");
                    return true;
                }

                try {
                    manager.claim(pos.x, pos.z, owner, ownerUUID, reason);
                } catch (PlotException e) {
                    OTJP.sendError(sender, e.getMessage());
                    return true;
                }

                manager.markClaimed(pos.x, pos.z);

                OTJP.sendInfo(sender, "Claimed plot " + pos.x + ", " + pos.z + " as " + owner);
                return true;
            }
        });

        plugin.getCommand("punclaim").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPosMatch(manager, player, args, pos);
                if (nextArg < 0) {
                    OTJP.sendError(sender, "Unknown plot!");
                    return true;
                }

                try {
                    if (player.hasPermission("ore.plot.unclaimadmin")) {
                        manager.forceUnclaim(pos.x, pos.z);
                    } else {
                        manager.unclaim(pos.x, pos.z, player.getName(), player.getUniqueId());
                    }
                } catch (PlotException e) {
                    OTJP.sendError(sender, e.getMessage());
                    return true;
                }

                manager.markUnclaimed(pos.x, pos.z);

                OTJP.sendInfo(sender, "Unclaimed plot " + pos.x + ", " + pos.z);
                return true;
            }
        });

        plugin.getCommand("pmap").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPosMatch(manager, player, args, pos);
                if (nextArg < 0) {
                    OTJP.sendError(sender, "Unknown plot!");
                    return true;
                }

                Plot.Pos mapPos = manager.plotToMapCoords(pos.x, pos.z);

                Location location = player.getLocation();
                location.setX(mapPos.x);
                location.setY(manager.getPosY());
                location.setZ(mapPos.z);
                player.teleport(location);

                return true;
            }
        });

        plugin.getCommand("pwarp").setExecutor(new CommandExecutor() {
            @Override
            public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
                if (!(sender instanceof Player)) {
                    OTJP.sendError(sender, "Not a player!");
                    return true;
                }

                Player player = (Player) sender;
                PlotMap manager = getOrCreateManager(player.getWorld());

                Plot.Pos pos = new Plot.Pos();
                int nextArg = tryParsePlotPosMatch(manager, player, args, pos);
                if (nextArg < 0) {
                    OTJP.sendError(sender, "Unknown plot!");
                    return true;
                }

                Plot.Pos center = manager.getPlotCentre(pos.x, pos.z);

                Location location = player.getLocation();
                location.setX(center.x);
                location.setY(manager.getPosY());
                location.setZ(center.z);
                player.teleport(location);

                return true;
            }
        });
    }

    public int initManagers(Server server) {
        managers.clear();

        for (World world : server.getWorlds()) {
            PlotMap manager = new PlotMap(world, DEFAULT_RADIUS, DEFAULT_SIZEX, DEFAULT_SIZEY); // TODO: load
            managers.put(world.getName(), manager);
        }

        return managers.size();
    }

    public void save() {
        // TODO: save
    }

    public PlotMap getManager(World world) {
        return managers.get(world.getName());
    }

    public PlotMap getOrCreateManager(World world) {
        PlotMap manager = managers.get(world.getName());
        if (manager == null) {
            manager = new PlotMap(world, DEFAULT_RADIUS, DEFAULT_SIZEX, DEFAULT_SIZEY); // TODO: load
            managers.put(world.getName(), manager);
        }

        return manager;
    }

    private int tryParsePlotPosMatch(PlotMap manager, Player player, String[] args, Plot.Pos pos) {
        /*
         * <cmd> <x> <y>
         * <cmd> <partialUserName> [optionalIndex]
         * <cmd> <partialReason> [optionalIndex]
         */

        if (args.length >= 2) {
            try {
                pos.x = Integer.parseInt(args[0]);
                pos.z = Integer.parseInt(args[1]);

                return 2;
            } catch (NumberFormatException e) {}
        }

        if (args.length >= 1) {
            int index = 0;
            int nextArg = 1;
            if (args.length >= 2) {
                try {
                    index = Integer.parseInt(args[1]);
                    nextArg = 2;
                } catch (NumberFormatException e) {}
            }

            int currIndex = 0;

            PlotUser user = manager.findUserMatch(args[0]);
            if (user != null) {
                for (Map.Entry<Plot.Pos, Plot> it : manager.getPlots().entrySet()) {
                    Plot plot = it.getValue();
                    if (plot.isClaimed()) {
                        if (plot.getOwnerName().equals(user.getLastName())) {
                            if (currIndex == index) {
                                pos.x = it.getKey().x;
                                pos.z = it.getKey().z;
                                return nextArg;
                            }
                            ++currIndex;
                        }
                    }
                }
            }

            currIndex = 0;

            String match = args[0].toLowerCase();
            for (Map.Entry<Plot.Pos, Plot> it : manager.getPlots().entrySet()) {
                Plot plot = it.getValue();
                if (plot.isClaimed()) {
                    String reason = plot.getReason();
                    if (reason != null && reason.toLowerCase().contains(match)) {
                        pos.x = it.getKey().x;
                        pos.z = it.getKey().z;
                        return nextArg;
                    }
                }
            }
        }

        Plot.Pos playerPos = getPlayerPlotPos(manager, player);
        if (manager.isInRange(pos.x, pos.z)) {
            pos.x = playerPos.x;
            pos.z = playerPos.z;
            return 0;
        }

        return -1;
    }

    private int tryParsePlotPos(PlotMap manager, Player player, String[] args, Plot.Pos pos) {
        if (args.length >= 2) {
            try {
                pos.x = Integer.parseInt(args[0]);
                pos.z = Integer.parseInt(args[1]);

                return 2;
            } catch (NumberFormatException e) {}
        }

        Plot.Pos playerPos = getPlayerPlotPos(manager, player);
        if (manager.isInRange(pos.x, pos.z)) {
            pos.x = playerPos.x;
            pos.z = playerPos.z;
            return 0;
        }

        return -1;
    }

    private Plot.Pos getPlayerPlotPos(PlotMap manager, Player player) {
        int posX = (int) player.getLocation().getX();
        int posZ = (int) player.getLocation().getZ();

        if (manager.isOnMap(posX, posZ)) {
            return manager.mapToPlotCoords(posX, posZ);
        } else {
            return manager.worldToPlotCoords(posX, posZ);
        }
    }
}
