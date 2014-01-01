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
	ProtoServer::~ProtoServer()
	{
		for (ServerConnMap::iterator it = m_Conns.begin(); it != m_Conns.end(); ++it)
		{
			delete it->second;
		}
	}

	bool ProtoServer::OnConnect(Client* cli)
	{
		return m_Auth.AuthServerIn(cli);
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

		const std::string& type = args[1];

		if (type == "EVENT")
		{
			OnEvent(cli, args);
		}
		else if (type == "QUERY")
		{
			OnQuery(cli, args);
		}
		else
		{
			OnCommand(cli, args);
		}
	}

	void ProtoServer::ConnectToServer(const std::string& name, Client* cli)
	{
		if (cli->IsValid())
		{
			if (m_Auth.AuthServerOut(cli))
			{
				if (cli->GetType() == Client::TYPE_SERVER)
				{
					m_Conns[name] = cli;
				}
			}
		}
	}

	void ProtoServer::BroadcastCommand(const std::string& host, const ArgsList& args)
	{
		std::stringstream stream;

		stream << host << std::endl;

		for (ArgsList::const_iterator it = args.begin(); it != args.end(); ++it)
		{
			stream << " " << *it;
		}

		stream << "\n";

		BroadcastMessage(stream.str());
	}
} /* OREd */
