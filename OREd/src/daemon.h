/** OREd/daemon.h: Daemon-wide status variables.
 * Copyright: GPLv3
 * Created: 2014-01-03 | redstonewarrior
 * Contributors:
 *     redstonewarrior
 * Changelog:
 *     2014-01-03 | Created file, added log | redstonewarrior
 * Description: This file contains process information and the log file fd.
 * Plans:
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

/************************/
/* Configuration Values */

/* These are all static after daemonization.
 * Do strdup(), if not NULL main free()s at
 * kill.
 */
/* Various paths */
extern char *ore_config;        /* '@' if stdin config.                 */
extern char *ore_log;           /* NULL if not daemonized (debug mode.) */
extern char *ore_java;          /* JVM executable.                      */
extern char *ore_jar_flag;      /* Java jar flag.                       */
extern char *ore_bukkit;        /* Bukkit jar path.                     */
extern char *ore_plugins;       /* Bukkit plugin directory.             */

/* OREd has multiple debugging modes, representing different levels
 * of scrutiny. 0 is release mode, it will not output anything but
 * errors and high level messages to the log file. (If you want nothing,
 * redirect to /dev/null.) Level 1 shows detailed notes on everything but
 * per-packet routing. (Save routing errors.) Also prints config on startup.
 * Level 2 shows all available information on the system, including
 * packet info spam.
 */
extern int   ore_debug;          /* 0 if normal, debug level if nonzero. */
#endif /* __ORED_DAEMON_H */



