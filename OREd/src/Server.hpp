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

#ifndef _ORED_SERVER_
#define _ORED_SERVER_

#include "Client.hpp"

#include <string>
#include <list>

namespace OREd
{
	/**
	 * \brief TCP Server implementation.
	 */
	class Server
	{
	public:
		typedef std::list<Client> ClientList;

	protected:
		/**
		 * \brief Called when a remote client attempts to connect.
		 *
		 * \return whether to accept the connection.
		 */
		virtual bool OnConnect(Client* cli) { return true; }

		/**
		 * \brief Called when a remote client disconnects.
		 *
		 * NOTE: The client instance is dead.
		 */
		virtual void OnDisconnect(Client* cli) {}

		/**
		 * \brief Called when a message is received.
		 */
		virtual void OnMessage(Client* cli, const std::string& msg) {}

	public:
		Server(const int port);

		Server() : m_Handle(-1) {}

		~Server();

		/**
		 * \return whether the socket is valid.
		 */
		bool IsValid() const;

		/**
		 * \brief Start serving.
		 */
		void Start();

		/**
		 * \brief Stop serving.
		 */
		void Stop();

		/**
		 * \return the number of connected clients.
		 */
		unsigned int GetNumClients() const;

		/**
		 * \return whether the server is running.
		 */
		bool IsRunning() const;

	protected:
		/** Connected clients */
		ClientList m_Clients;

		/** Flag indicating whether the server is running. */
		bool m_Running;

		/** Socket handle */
		int m_Handle;
	};

	inline unsigned int Server::GetNumClients() const
	{
		return m_Clients.size();
	}

	inline bool Server::IsRunning() const
	{
		return m_Running;
	}
} /* OREd */

#endif
