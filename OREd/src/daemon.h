/**
 *  ORE Server management daemon
 *  Copyright (C) 2013 OpenRedstone
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

#ifndef _ORED_DAEMON_
#define _ORED_DAEMON_

#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Working directory */
#define WORKING_DIRECTORY "/servers/ORE/"

/* Path to log file */
#define LOG_PATH "OREd.log"

/* Log file handle */
FILE* fLog;

/**
 * \brief Try to daemonize the process.
 *
 * On success, the parent process will exit and control will be given to the child process.
 *
 * On failure, both processes will exit with an error code.
 */
int daemonize(void);

#ifdef __cplusplus
}
#endif

#endif
