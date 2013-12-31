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

#include "ProtoServer.hpp"

#include <sstream>

namespace OREd
{
	bool ProtoServer::OnConnect(Client* cli)
	{
		// TODO: Authenticate (Server)

		return true;
	}

	void ProtoServer::OnMessage(Client* cli, const std::string& msg)
	{
		std::stringstream stream(msg);

		ArgsList args;

		while (stream.good())
		{
			std::string arg;

			stream >> arg;

			args.push_back(arg);
		}

		if (args.size() < 2)
		{
			return;
		}

		HandlerMap::iterator it = m_Handlers.find(args[1]);

		if (it == m_Handlers.end())
		{
			return; // Unknown command
		}

		if (!(it->second)(cli, args))
		{
			return; // Syntax error
		}
	}

	void ProtoServer::ConnectToServer(const std::string& name, const Client cli)
	{
		if (cli.IsValid())
		{
			// TODO: Authenticate (Client)

			m_Conns[name] = cli;
		}
	}

	void ProtoServer::RegisterHandler(const std::string& cmd, CmdHandler handler)
	{
		m_Handlers[cmd] = handler;
	}
} /* OREd */
