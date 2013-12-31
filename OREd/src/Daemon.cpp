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

#include "Daemon.hpp"

#include "Log.hpp"

#include <iostream>

#include <sys/types.h>
#include <sys/stat.h>

#include <fcntl.h>
#include <unistd.h>
#include <syslog.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

namespace OREd
{
	bool Daemonize(const std::string& wdir)
	{
		pid_t pid = fork();

		if (pid < 0)
		{
			std::cout << "Fork unsuccesful." << std::endl;

			return false;
		}

		if (pid > 0)
		{
			std::cout << "Fork succesful. [PID: " << pid << "]" << std::endl;

			exit(EXIT_SUCCESS);
		}

		umask(0);

		if (!Log::Init("OREd.log"))
		{
			std::cout << "Could not open log file." << std::endl;

			exit(EXIT_FAILURE);
		}

		pid_t sid = setsid();

		if (sid < 0)
		{
			Log::STREAM << "Could not create a new session" << std::endl;

			exit(EXIT_FAILURE);
		}

		if (chdir(wdir.c_str()) < 0)
		{
			Log::STREAM << "Could not change working directory to " << wdir << std::endl;

			exit(EXIT_FAILURE);
		}

		close(STDIN_FILENO);
		close(STDOUT_FILENO);
		close(STDERR_FILENO);

		return true;
	}
} /* OREd */
