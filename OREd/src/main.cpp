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
#include "Manager.hpp"
#include "Log.hpp"

#include <stdlib.h>

static char* const args[] = { "java", "-jar", "craftbukkit.jar", NULL };

std::string JavaPath = "/usr/bin/java";

using namespace OREd;

int main()
{
	if (!Daemonize("/servers/ORE/"))
	{
		exit(EXIT_FAILURE);
	}

	Manager manager(4242, "skaro");

	Console build(JavaPath, args);

	manager.Start();

	Log::STREAM << "Exiting..." << std::endl;

	exit(EXIT_SUCCESS);
}
