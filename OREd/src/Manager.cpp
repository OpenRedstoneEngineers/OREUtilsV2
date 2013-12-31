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

#include "Manager.hpp"

namespace OREd
{
	bool Manager::HandleQuery(Client* cli, const ArgsList& args)
	{
		if (args.size() < 3)
		{
			return false;
		}

		const std::string& type = args[2];

		return true;
	}

	bool Manager::HandleEvent(Client* cli, const ArgsList& args)
	{
		if (args.size() < 3)
		{
			return false;
		}

		const std::string& type = args[2];

		return true;
	}

	Manager::Manager(const int port) : ProtoServer(port)
	{
		RegisterHandler("EVENT", HandleEvent);

		RegisterHandler("QUERY", HandleQuery);
	}

	void Manager::InitConsole(const std::string& name, Console* console)
	{
		if (!console->IsValid())
		{
			return;
		}

		m_Consoles[name] = console;
	}

	Console* Manager::GetConsole(const std::string& name)
	{
		ConsoleMap::iterator it = m_Consoles.find(name);

		if (it == m_Consoles.end())
		{
			return NULL;
		}
		else
		{
			return it->second;
		}
	}
} /* OREd */
