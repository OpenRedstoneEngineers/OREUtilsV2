/** OREd/daemon.h: Daemon-wide status variables.
 * Copyright: GPLv3
 * Created: 2014-01-03 | redstonewarrior
 * Contributors:
 *     redstonewarrior
 * Changelog:
 *     2014-01-03 | Created file, added log | redstonewarrior
 * Description: This file contains process information and the log file fd.
 * Plans:
 *     -Possibly move to log.h and add helper methods?
 *
 * Further copyright information:
 *     Copyright (C) 2013 OpenRedstone
 *
 *     This program is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     This program is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __ORED_DAEMON_H
#define __ORED_DAEMON_H

/********************/
/* Global variables */

/* Log file's fd. Implemented in main.c as of 2014-01-03. */
extern int ore_logfd;

#endif // __ORED_DAEMON_H
