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

#include "console.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>

#include <fcntl.h>
#include <unistd.h>
#include <syslog.h>

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <assert.h>

child_proc* console_init(const char* filename, char* const argv[])
{
	assert(filename != NULL);

	child_proc* proc = malloc(sizeof(child_proc));

	if (proc == NULL)
	{
		return NULL;
	}

	if (pipe(proc->pipeFd) < 0)
	{
		free(proc);

		return NULL;
	}

	proc->pid = fork();

	if (proc->pid < 0)
	{
		free(proc);

		return NULL;
	}

	if (proc->pid == 0)
	{
		dup2(proc->pipeFd[0], STDIN_FILENO);
		dup2(proc->pipeFd[1], STDOUT_FILENO);
		dup2(proc->pipeFd[1], STDERR_FILENO);

		if (execv(filename, argv) < 0)
		{
			exit(EXIT_FAILURE);
		}

		exit(EXIT_SUCCESS);
	}

	return proc;
}

void console_terminate(child_proc* proc)
{
	assert(proc != NULL);

	kill(proc->pid, SIGTERM);

	free(proc);
}

int console_is_running(child_proc* proc)
{
	assert(proc != NULL);

	int status;

	if (waitpid(proc->pid, &status, WNOHANG) < 0)
	{
		return -1;
	}

	return !(WIFEXITED(status) || WIFSIGNALED(status));
}
