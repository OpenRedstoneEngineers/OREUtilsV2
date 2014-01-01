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

#include "Console.hpp"

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>

#include <fcntl.h>
#include <unistd.h>

#include <stdlib.h>
#include <string.h>

namespace OREd
{
	Console::Console(const std::string& path, char* const argv[]) : m_Handle(-1)
	{
		if (pipe(m_PipeFd) < 0)
		{
			return;
		}

		pid_t id = fork();

		if (id < 0)
		{
			return;
		}

		if (id == 0)
		{
			dup2(m_PipeFd[0], STDIN_FILENO);
			dup2(m_PipeFd[1], STDOUT_FILENO);
			dup2(m_PipeFd[1], STDERR_FILENO);

			if (execv(path.c_str(), argv) < 0)
			{
				exit(EXIT_FAILURE);
			}

			exit(EXIT_FAILURE);
		}

		m_Handle = id;
	}

	Console::~Console()
	{
		Kill();
	}

	bool Console::IsValid() const
	{
		return m_Handle >= 0;
	}

	bool Console::IsRunning() const
	{
		if (!IsValid())
		{
			return false;
		}

		int status;

		if (waitpid(m_Handle, &status, WNOHANG) < 0)
		{
			return -1;
		}

		return !(WIFEXITED(status) || WIFSIGNALED(status));
	}

	bool Console::Read(std::string& msg)
	{
		if (!IsValid())
		{
			return false;
		}

		char buffer[256];

		bzero(buffer, sizeof(buffer));

		if (read(m_PipeFd[1], buffer, sizeof(buffer) - 1) < 0)
		{
			return false;
		}

		msg = std::string(buffer);

		return true;
	}

	bool Console::Write(const std::string& msg)
	{
		if (!IsValid())
		{
			return false;
		}

		if (write(m_PipeFd[0], msg.c_str(), msg.size()) < 0)
		{
			return false;
		}

		return true;
	}

	void Console::Kill()
	{
		if (IsValid())
		{
			kill(m_Handle, SIGTERM);
		}
	}
} /* OREd */
