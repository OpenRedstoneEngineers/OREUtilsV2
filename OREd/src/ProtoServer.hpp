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

#ifndef _ORED_PROTO_SERVER_
#define _ORED_PROTO_SERVER_

#include "Auth.hpp"

#include "Server.hpp"

#include <string>
#include <vector>
#include <map>

namespace OREd
{
	/**
	 * \brief ORE Protocol implementation.
	 */
	class ProtoServer : public Server
	{
	public:
		typedef std::vector<std::string> ArgsList;

		typedef std::map<const std::string, Client*> ServerConnMap;

	public:
		ProtoServer(const int port) : Server(port) {}

		~ProtoServer();

		/**
		 * \brief Connect to a remote server.
		 */
		void ConnectToServer(const std::string& name, Client* cli);

		/**
		 * \brief Broadcast a command.
		 */
		void BroadcastCommand(const std::string& host, const ArgsList& args);

	protected:
		virtual bool OnConnect(Client* cli);

		virtual void OnMessage(Client* cli, const std::string& msg);

	protected:
		/**
		 * \brief Called when a command is broadcasted.
		 */
		virtual bool OnCommand(Client* cli, const ArgsList& args) = 0;

		/**
		 * \brief Called when an event is broadcasted.
		 */
		virtual bool OnEvent(Client* cli, const ArgsList& args) = 0;

		/**
		 * \brief Called when a query is broadcasted.
		 */
		virtual bool OnQuery(Client* cli, const ArgsList& args) = 0;

	protected:
		/** Outgoing server connections */
		ServerConnMap m_Conns;

		/** Associated authenticator */
		Authenticator m_Auth;
	};
} /* OREd */

#endif
