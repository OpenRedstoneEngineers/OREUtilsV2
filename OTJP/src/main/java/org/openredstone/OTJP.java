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

package org.openredstone;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.CommandSender;
import org.bukkit.generator.ChunkGenerator;
import org.bukkit.plugin.java.JavaPlugin;

import org.openredstone.plot.PlotServer;
import org.openredstone.gen.PlotGenerator;

import java.util.logging.Level;

/**
 * Main java plugin class.
 *
 */
public class OTJP extends JavaPlugin {
	private PlotServer plotServer;

	@Override
	public ChunkGenerator getDefaultWorldGenerator(String worldName, String id) {
		return new PlotGenerator();
	}

	@Override
	public void onEnable() {
		plotServer = new PlotServer(this);
		plotServer.initManagers(getServer());
	}

	@Override
	public void onDisable() {
		plotServer.save();
	}

	public static void info(String msg) {
		Bukkit.getServer().getLogger().log(Level.INFO, msg);
	}

	public static void severe(String msg) {
		Bukkit.getServer().getLogger().log(Level.SEVERE, msg);
	}

	public static void sendInfo(CommandSender sender, String msg) {
		sender.sendMessage(ChatColor.YELLOW + "[INFO] " + msg);
	}

	public static void sendWarning(CommandSender sender, String msg) {
		sender.sendMessage(ChatColor.GOLD + "[WARNING] " + msg);
	}

	public static void sendError(CommandSender sender, String msg) {
		sender.sendMessage(ChatColor.RED + "[ERROR] " + msg);
	}

	public static void sudo(String cmd) {
		Bukkit.dispatchCommand(Bukkit.getConsoleSender(), cmd);
	}
}

