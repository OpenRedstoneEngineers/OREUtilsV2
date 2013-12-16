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

#ifndef _ORED_CONSOLE_
#define _ORED_CONSOLE_

#include <sys/types.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \brief Represents a child process.
 */
typedef struct child_proc_
{
	/* Process ID */
	pid_t pid;

	/* File descriptors. */
	int pipeFd[2];
} child_proc;

/**
 * \brief Create a new child process.
 *
 * On failure, a NULL pointer will be returned.
 */
child_proc* console_init(const char* filename, char* const argv[]);

/**
 * \brief Terminate the specified child process.
 *
 * WARNING: The pointer will be invalidated.
 */
void console_terminate(child_proc* proc);

/**
 * \return whether the child process is running.
 */
int console_is_running(child_proc* proc);

#ifdef __cplusplus
}
#endif

#endif
