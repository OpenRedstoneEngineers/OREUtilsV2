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

import java.util.Map;
import java.util.UUID;
import java.util.HashMap;

public class PlotManager {
    private final int DEFAULT_MAX_PLOTS = 1;

    protected int radius;
    protected int sizeX;
    protected int sizeZ;

    private HashMap<Plot.Pos, Plot> plots;
    private HashMap<UUID, PlotUser> users;

    public static int intDiv(int x, int y) {
        return (int)Math.floor(x / (double)y);
    }

    public PlotManager(int radius, int sizeX, int sizeZ) {
        this.radius = radius;

        this.sizeX = sizeX;
        this.sizeZ = sizeZ;

        this.plots = new HashMap<Plot.Pos, Plot>();
        this.users = new HashMap<UUID, PlotUser>();
    }

    public int getNumPlots() {
        return 4 * radius * radius;
    }
    public int getRadius() {
        return radius;
    }

    public int getSizeX() {
        return sizeX;
    }

    public int getSizeZ() {
        return sizeZ;
    }

    public boolean isInRange(int x, int y) {
        return (x < radius) && (y < radius) && (x >= -radius) && (y >= -radius);
    }

    public HashMap<UUID, PlotUser> getUsers() {
        return users;
    }

    public HashMap<Plot.Pos, Plot> getPlots() {
        return plots;
    }

    public void setRadius(int radius) {
        this.radius = radius;
    }

    public void claim(int x, int y, String ownerName, UUID ownerUUID, String reason) throws PlotException {
        PlotUser user = getOrCreateUser(ownerUUID);
        user.setLastName(ownerName);

        int remPlots = user.getRemPlots();
        if (remPlots == 0) {
            throw new PlotException("Cannot claim more plots");
        }

        Plot plot = getOrCreatePlot(x, y);
        plot.claim(ownerName, ownerUUID, reason);

        user.setRemPlots(remPlots - 1);
    }

    public void unclaim(int x, int y, String ownerName, UUID ownerUUID) throws PlotException {
        Plot plot = getPlot(x, y);
        if (plot == null) {
            throw new PlotException("Plot is not claimed");
        }

        if (plot.isClaimed()) {
            if (plot.getOwnerUUID() == ownerUUID) {
                plots.remove(new Plot.Pos(x, y));

                PlotUser user = getOrCreateUser(ownerUUID);
                user.setRemPlots(user.getRemPlots() + 1);
            } else {
                throw new PlotException("Plot is claimed by " + plot.getOwnerName());
            }
        } else {
            throw new PlotException("Plot is not claimed");
        }
    }

    public void forceUnclaim(int x, int y) throws PlotException {
        Plot plot = getPlot(x, y);
        if (plot == null) {
            throw new PlotException("Plot is not claimed");
        }

        if (plot.isClaimed()) {
            PlotUser user = getOrCreateUser(plot.getOwnerUUID());
            user.setRemPlots(user.getRemPlots() + 1);

            plots.remove(new Plot.Pos(x, y));
        } else {
            throw new PlotException("Plot is not claimed");
        }
    }

    public void reserve(int x, int y, String ownerName, UUID ownerUUID, String reason) throws PlotException {
        PlotUser user = getOrCreateUser(ownerUUID);
        user.setLastName(ownerName);

        Plot plot = getOrCreatePlot(x, y);
        plot.reserve(ownerName, ownerUUID, reason);
    }

    public Plot getPlot(int x, int y) {
        return plots.get(new Plot.Pos(x, y));
    }

    public Plot getOrCreatePlot(int x, int y) {
        Plot.Pos key = new Plot.Pos(x, y);

        Plot plot = plots.get(key);
        if (plot == null) {
            plot = new Plot();
            plots.put(key, plot);
        }

        return plot;
    }

    public Plot.Pos worldToPlotCoords(int x, int z) {
        return new Plot.Pos(
                intDiv(x, sizeX),
                intDiv(z, sizeZ));
    }

    public PlotUser getOrCreateUser(UUID uuid) {
        PlotUser user = users.get(uuid);
        if (user == null) {
            user = new PlotUser(DEFAULT_MAX_PLOTS);
            users.put(uuid, user);
        }

        return user;
    }

    public Plot.Pos getPlotCentre(int x, int z) {
        int halfSizeX = sizeX / 2;
        int halfSizeZ = sizeZ / 2;

        return new Plot.Pos(x * sizeX + halfSizeX, z * sizeZ + halfSizeZ);
    }

    public PlotUser getUser(UUID uuid) {
        return users.get(uuid);
    }

    public UUID getUserUUID(String name) {
        for (Map.Entry<UUID, PlotUser> it : users.entrySet()) {
            PlotUser user = it.getValue();
            if (user.getLastName().equals(name)) {
                return it.getKey();
            }
        }

        return null;
    }

    public PlotUser findUserMatch(String partialName) {
        String match = partialName.toLowerCase();

        for (PlotUser user : users.values()) {
            if (user.getLastName().toLowerCase().equals(match)) {
                return user;
            }
        }

        for (PlotUser user : users.values()) {
            if (user.getLastName().toLowerCase().contains(match)) {
                return user;
            }
        }

        return null;
    }

    public String getInfo(int x, int y) {
        Plot plot = getOrCreatePlot(x, y);

        StringBuilder builder = new StringBuilder("Plot (");
        builder.append(x);
        builder.append(", ");
        builder.append(y);
        builder.append(")\n");
        builder.append(plot.toString());

        return builder.toString();
    }
}
