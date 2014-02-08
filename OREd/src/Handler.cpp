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

#include "Handler.hpp"

namespace OREd
{
	bool HandleCmdKick(Client* cli, ConsolePtr& target, const Manager::ArgsList& args)
	{
		if (args.size() < 3 || !cli->IsAdmin())
		{
			return false;
		}

		std::string cmd = "kick " + args[2] + "\n";

		target->Write(cmd);

		return true;
	}

	bool HandleCmdStop(Client* cli, ConsolePtr& target, const Manager::ArgsList& args)
	{
		if (!cli->IsAdmin())
		{
			return false;
		}

		std::string cmd = "stop\n";

		target->Write(cmd);

		target.Stop();

		return true;
	}

	bool HandleCmdStart(Client* cli, ConsolePtr& target, const Manager::ArgsList& args)
	{
		if (!cli->IsAdmin())
		{
			return false;
		}

		target.Start();

		return true;
	}

	bool HandleCmdKill(Client* cli, ConsolePtr& target, const Manager::ArgsList& args)
	{
		if (!cli->IsAdmin())
		{
			return false;
		}

		target.Stop();

		return true;
	}
} /* OREd */