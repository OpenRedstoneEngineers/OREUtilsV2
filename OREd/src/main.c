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

#include "console.h"

#include <stdlib.h>

static char* const args[] = { "java", "-jar craftbukkit.jar", NULL };

int main()
{
	if (daemonize() < 0)
	{
		exit(EXIT_FAILURE);
	}

	child_proc* server = console_init("/usr/bin/java", args);

	if (server == NULL)
	{
		fprintf(fLog, "Could not start craftbukkit.\n");

		fclose(fLog);

		exit(EXIT_FAILURE);
	}

	console_terminate(server);

	fprintf(fLog, "Exiting.\n");

	fclose(fLog);

	exit(EXIT_SUCCESS);
}
