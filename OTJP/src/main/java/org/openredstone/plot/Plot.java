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

import java.util.UUID;

public class Plot {
    public enum Status {
        FREE,
        CLAIMED,
        RESERVED
    }

    public static class Pos {
        int x;
        int z;

        public Pos() {
            this.x = 0;
            this.z = 0;
        }

        public Pos(int x, int z) {
            this.x = x;
            this.z = z;
        }

        @Override
        public int hashCode() {
            return (x << 16) + z;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (!(obj instanceof Pos)) {
                return false;
            }
            Pos key = (Pos) obj;
            return x == key.x && z == key.z;
        }
    }

    private Status status;
    private String ownerName;
    private UUID ownerUUID;
    private String reason;
    private long date;

    public Plot() {
        status = Status.FREE;

        ownerName = null;
        ownerUUID = null;
        reason = null;
        date = 0;
    }

    public Status getStatus() {
        return status;
    }

    public boolean isClaimed() {
        return status != Status.FREE;
    }

    public boolean isClaimable() {
        return status == Status.FREE;
    }

    public UUID getOwnerUUID() {
        return ownerUUID;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public String getReason() {
        return reason;
    }

    public void claim(String ownerName, UUID ownerUUID, String reason) throws PlotException {
        if (status == Status.CLAIMED) {
            throw new PlotException("This plot is owned by " + this.ownerName);
        } else if (status == Status.RESERVED && !this.ownerUUID.equals(ownerUUID)) {
            throw new PlotException("This plot is owned by " + this.ownerName);
        }

        this.status = Status.CLAIMED;
        this.ownerName = ownerName;
        this.ownerUUID = ownerUUID;
        this.reason = reason;
        this.date = getTimestamp();
    }

    public void reserve(String ownerName, UUID ownerUUID, String reason) throws PlotException {
        if (!isClaimable()) {
            throw new PlotException("This plot is owned by " + this.ownerName);
        }

        this.status = Status.RESERVED;
        this.ownerName = ownerName;
        this.ownerUUID = ownerUUID;
        this.reason = reason;
        this.date = getTimestamp();
    }

    private long getTimestamp() {
        return System.currentTimeMillis() / 1000L;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder("Status: ");

        switch (status) {
            case FREE: {
                builder.append("Free");
                break;
            }

            case CLAIMED: {
                builder.append("Claimed");
                builder.append("\nOwner: " + ownerName);
                builder.append("\nClaimed at " + date);
                if (reason != null) {
                    builder.append("\nDescription: " + reason);
                }
                break;
            }

            case RESERVED: {
                builder.append("Reserved");
                builder.append("\nReservee: " + ownerName);
                builder.append("\nReserved at " + date);
                if (reason != null) {
                    builder.append("\nReason: " + reason);
                }
                break;
            }

            default: {
                builder.append("Invalid");
                break;
            }
        }

        return builder.toString();
    }
}
