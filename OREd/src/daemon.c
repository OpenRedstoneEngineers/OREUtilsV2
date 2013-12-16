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

#include "daemon.h"

#include <sys/types.h>
#include <sys/stat.h>

#include <fcntl.h>
#include <unistd.h>
#include <syslog.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int daemonize(void)
{
	pid_t pid = fork();

	if (pid < 0)
	{
		printf("Fork unsuccesful.\n");

		exit(EXIT_FAILURE);
	}

	if (pid > 0)
	{
		printf("Fork succesful. [PID: %i]\n", pid);

		exit(EXIT_SUCCESS);
	}

	umask(0);

	fLog = fopen(LOG_PATH, "w");

	if (fLog == NULL)
	{
		printf("Could not open log file %s\n", LOG_PATH);

		exit(EXIT_FAILURE);
	}

	pid_t sid = setsid();

	if (sid < 0)
	{
		fprintf(fLog, "Could not create a new session.\n");

		fclose(fLog);

		exit(EXIT_FAILURE);
	}

	if (chdir(WORKING_DIRECTORY) < 0)
	{
		fprintf(fLog, "Could not change working directory to %s.\n", WORKING_DIRECTORY);

		fclose(fLog);

		exit(EXIT_FAILURE);
	}

	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);

	return 0;
}
