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
	ConsolePtr::ConsolePtr(const std::string& path, char* const* argv) : m_Path(path), m_Argv(argv)
	{
		m_Ptr = new Console(m_Path, m_Argv);
	}

	void ConsolePtr::Stop()
	{
		if (m_Ptr)
		{
			delete m_Ptr;

			m_Ptr = NULL;
		}
	}

	void ConsolePtr::Start()
	{
		if (m_Ptr == NULL)
		{
			m_Ptr = new Console(m_Path, m_Argv);
		}
	}

	bool Manager::OnCommand(Client* cli, const ArgsList& args)
	{
		ConsolePtr* console = GetConsoleByTarget(args[0]);

		if (console == NULL)
		{
			return false;
		}

		HandlerMap::iterator it = m_CmdHandlers.find(args[1]);

		if (it == m_CmdHandlers.end())
		{
			return false; // Unknown command
		}

		return (it->second)(cli, *console, args);
	}

	bool Manager::OnEvent(Client* cli, const ArgsList& args)
	{
		// TODO: Parse event		

		return true;
	}

	bool Manager::OnQuery(Client* cli, const ArgsList& args)
	{
		ConsolePtr* console = GetConsoleByTarget(args[0]);

		if (console == NULL)
		{
			return false;
		}

		HandlerMap::iterator it = m_QueryHandlers.find(args[1]);

		if (it == m_QueryHandlers.end())
		{
			return false; // Unknown query
		}

		return (it->second)(cli, *console, args);
	}

	void Manager::InitConsole(const std::string& name, ConsolePtr* console)
	{
		if (!(*console)->IsValid())
		{
			return;
		}

		m_Consoles[name] = console;
	}

	ConsolePtr* Manager::GetConsole(const std::string& name)
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

	ConsolePtr* Manager::GetConsoleByTarget(const std::string& target)
	{
		size_t pos = target.find(".");

		if (pos != std::string::npos)
		{
			std::string host = target.substr(0, pos);

			if (host != m_Host)
			{
				return NULL;
			}

			std::string name = target.substr(pos + 1, std::string::npos);

			return GetConsole(name);
		}

		return NULL;
	}
} /* OREd */
