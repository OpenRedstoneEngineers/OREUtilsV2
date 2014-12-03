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

import org.bukkit.Material;
import org.bukkit.World;

public class PlotMap extends PlotManager {
    private int posX;
    private int posY;
    private int posZ;

    private World world;

    private final Material BLOCK_RESERVED = Material.REDSTONE_LAMP_ON;
    private final Material BLOCK_CLAIMED = Material.REDSTONE_LAMP_ON;
    private final Material BLOCK_UNCLAIMED = Material.REDSTONE_LAMP_OFF;
    
    private final Material BLOCK_BELOW_RESERVED = Material.REDSTONE_BLOCK;
    private final Material BLOCK_BELOW_CLAIMED = Material.REDSTONE_BLOCK;
    private final Material BLOCK_BELOW_UNCLAIMED = Material.AIR;

    private final Material BLOCK_FRAME_X = Material.STONE;
    private final Material BLOCK_FRAME_Y = Material.WOOD;
    private final Material BLOCK_FRAME_CROSS = Material.STONE;

    public PlotMap(World world, int radius, int sizeX, int sizeY) {
        super(radius, sizeX, sizeY);

        this.posX = 0;
        this.posY = 90;
        this.posZ = 0;

        this.world = world;
    }

    public boolean isOnMap(int x, int z) {
        return Math.abs(x - posX) < (radius * 3) && Math.abs(z - posZ) < (radius * 3);
    }

    public void setMapPos(int x, int y, int z) {
        posX = x;
        posY = y;
        posZ = z;
    }

    public int getPosY() {
        return posY;
    }

    public Plot.Pos plotToMapCoords(int x, int z) {
        int newX = x * 3;
        int newZ = z * 3;

        if (newX < 0) {
            newX -= 1;
        } else {
            newX += 1;
        }

        if (newZ < 0) {
            newZ -= 1;
        } else {
            newZ += 1;
        }

        return new Plot.Pos(newX + posX + 2, newZ + posZ + 2);
    }

    public Plot.Pos mapToPlotCoords(int x, int z) {
        int newX = x - posX;
        int newZ = z - posZ;

        if (newX > 0) {
            newX -= 2;
        }

        if (newZ > 0) {
            newZ -= 2;
        }

        return new Plot.Pos(
                intDiv(newX, 3),
                intDiv(newZ, 3));
    }

    public void markClaimed(int x, int z) {
        Plot.Pos pos = plotToMapCoords(x, z);

        world.getBlockAt(pos.x,     posY, pos.z    ).setType(BLOCK_CLAIMED);
        world.getBlockAt(pos.x - 1, posY, pos.z    ).setType(BLOCK_CLAIMED);
        world.getBlockAt(pos.x,     posY, pos.z - 1).setType(BLOCK_CLAIMED);
        world.getBlockAt(pos.x - 1, posY, pos.z - 1).setType(BLOCK_CLAIMED);

        world.getBlockAt(pos.x,     posY - 1, pos.z    ).setType(BLOCK_BELOW_CLAIMED);
        world.getBlockAt(pos.x - 1, posY - 1, pos.z    ).setType(BLOCK_BELOW_CLAIMED);
        world.getBlockAt(pos.x,     posY - 1, pos.z - 1).setType(BLOCK_BELOW_CLAIMED);
        world.getBlockAt(pos.x - 1, posY - 1, pos.z - 1).setType(BLOCK_BELOW_CLAIMED);
    }

    public void markReserved(int x, int z) {
        Plot.Pos pos = plotToMapCoords(x, z);

        world.getBlockAt(pos.x,     posY, pos.z    ).setType(BLOCK_RESERVED);
        world.getBlockAt(pos.x - 1, posY, pos.z    ).setType(BLOCK_RESERVED);
        world.getBlockAt(pos.x,     posY, pos.z - 1).setType(BLOCK_RESERVED);
        world.getBlockAt(pos.x - 1, posY, pos.z - 1).setType(BLOCK_RESERVED);

        world.getBlockAt(pos.x,     posY - 1, pos.z    ).setType(BLOCK_BELOW_RESERVED);
        world.getBlockAt(pos.x - 1, posY - 1, pos.z    ).setType(BLOCK_BELOW_RESERVED);
        world.getBlockAt(pos.x,     posY - 1, pos.z - 1).setType(BLOCK_BELOW_RESERVED);
        world.getBlockAt(pos.x - 1, posY - 1, pos.z - 1).setType(BLOCK_BELOW_RESERVED);
    }

    public void markUnclaimed(int x, int z) {
        Plot.Pos pos = plotToMapCoords(x, z);

        world.getBlockAt(pos.x,     posY, pos.z    ).setType(BLOCK_UNCLAIMED);
        world.getBlockAt(pos.x - 1, posY, pos.z    ).setType(BLOCK_UNCLAIMED);
        world.getBlockAt(pos.x,     posY, pos.z - 1).setType(BLOCK_UNCLAIMED);
        world.getBlockAt(pos.x - 1, posY, pos.z - 1).setType(BLOCK_UNCLAIMED);

        world.getBlockAt(pos.x,     posY - 1, pos.z    ).setType(BLOCK_BELOW_UNCLAIMED);
        world.getBlockAt(pos.x - 1, posY - 1, pos.z    ).setType(BLOCK_BELOW_UNCLAIMED);
        world.getBlockAt(pos.x,     posY - 1, pos.z - 1).setType(BLOCK_BELOW_UNCLAIMED);
        world.getBlockAt(pos.x - 1, posY - 1, pos.z - 1).setType(BLOCK_BELOW_UNCLAIMED);
    }

    private void markFrame(int x, int z) {
        Plot.Pos pos = plotToMapCoords(x, z);

        world.getBlockAt(pos.x - 2, posY, pos.z    ).setType(BLOCK_FRAME_Y);
        world.getBlockAt(pos.x - 2, posY, pos.z - 1).setType(BLOCK_FRAME_Y);
        world.getBlockAt(pos.x,     posY, pos.z - 2).setType(BLOCK_FRAME_X);
        world.getBlockAt(pos.x - 1, posY, pos.z - 2).setType(BLOCK_FRAME_X);

        if (x == radius - 1) {
            world.getBlockAt(pos.x + 1, posY, pos.z    ).setType(BLOCK_FRAME_Y);
            world.getBlockAt(pos.x + 1, posY, pos.z - 1).setType(BLOCK_FRAME_Y);
        }

        if (z == radius - 1) {
            world.getBlockAt(pos.x,     posY, pos.z + 1).setType(BLOCK_FRAME_X);
            world.getBlockAt(pos.x - 1, posY, pos.z + 1).setType(BLOCK_FRAME_X);
        }

        world.getBlockAt(pos.x - 2, posY, pos.z - 2).setType(BLOCK_FRAME_CROSS);
    }

    public void generate() {
        for (int x = -radius; x < radius; ++x) {
            for (int z = -radius; z < radius; ++z) {
                markFrame(x, z);

                Plot plot = getPlot(x, z);
                if (plot == null) {
                    markUnclaimed(x, z);
                } else {
                    Plot.Status status = plot.getStatus();
                    switch (status) {
                        case FREE: {
                            markUnclaimed(x, z);
                            break;
                        }

                        case RESERVED: {
                            markReserved(x, z);
                            break;
                        }

                        case CLAIMED: {
                            markClaimed(x, z);
                            break;
                        }
                    }
                }
            }
        }

        System.out.println("Generated map");
    }
}
