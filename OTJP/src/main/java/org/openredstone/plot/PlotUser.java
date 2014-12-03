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

public class PlotUser {
    private int remPlots;
    private String lastName;

    public PlotUser(int remPlots) {
        this.remPlots = remPlots;
        this.lastName = "";
    }

    public int getRemPlots() {
        return remPlots;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String name) {
        this.lastName = name;
    }

    public void setRemPlots(int plots) {
        this.remPlots = plots;
    }
}
