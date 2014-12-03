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

package org.openredstone.gen;

import org.bukkit.generator.ChunkGenerator;
import org.bukkit.Material;
import org.bukkit.World;

import java.util.Random;

public class PlotGenerator extends ChunkGenerator {
	public int PlotWidth = 256;
	public int PlotHeight = 16;
	public int PlotLength = 256;

	public short BlockMain = (short) Material.SANDSTONE.getId();
	public short BlockBorder = (short) Material.SMOOTH_BRICK.getId();
	public short BlockCorner0 = (short) (Material.WOOL.getId() + ((short) 1 >> 8));
	public short BlockCorner1 = (short) Material.NETHERRACK.getId();

	public short[][] generateExtBlockSections(World world, Random random, int x, int z, BiomeGrid biomes) {
		short[][] result = new short[world.getMaxHeight() / 16][];

		int chunkOffsetX = 16 * x;
		int chunkOffsetZ = 16 * z;
		int modX, modZ;

		for (int x1 = 0; x1 < 16; ++x1) {
			for (int z1 = 0; z1 < 16; ++z1) {
				for(int y1 = 0; y1 < PlotHeight; ++y1) {
					setBlock(result, x1, y1, z1, BlockMain);

					if (y1 == PlotHeight - 1) {
						modX = (chunkOffsetX + x1) % PlotWidth;
						modZ = (chunkOffsetZ + z1) % PlotLength;

						if (modX == 0 || modX == 255 || modX == -1 || modZ == 0 || modZ == 255 || modZ == -1)
							setBlock(result, x1, y1, z1, BlockBorder);

						if (x1 == 0 && z1 == 0 || x1 == 15 && z1 == 15)
							setBlock(result, x1, y1, z1, BlockCorner0);

						if (x1 == 0 && z1 == 15 || x1 == 15 && z1 == 0)
							setBlock(result, x1, y1, z1, BlockCorner1);
					}
				}
			}
		}

		return result;
	}

	void setBlock(short[][] result, int x, int y, int z, short blkid) {
		if (result[y >> 4] == null) {
			result[y >> 4] = new short[4096];
		}

		result[y >> 4][((y & 0xF) << 8) | (z << 4) | x] = blkid;
	}
}
