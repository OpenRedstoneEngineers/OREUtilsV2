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

#ifndef _ORED_CLIENT_
#define _ORED_CLIENT_

#include <string>

namespace OREd
{
	/**
	 * \brief Represents a remote TCP connection.
	 */
	class Client
	{
	public:
		Client(const std::string& host, const std::string& service);

		Client(const std::string& address, const int port);

		Client(int handle) : m_Handle(handle) {}

		Client() : m_Handle(-1) {}

		~Client();

		/**
		 * \return whether the socket is valid.
		 */
		bool IsValid() const;

		/**
		 * \return the last message from the packet queue. (Blocking)
		 */
		bool Recv(std::string& msg);

		/**
		 * \brief Send the specified message.
		 */
		bool Send(const std::string& msg);

	protected:
		/** Socket handle */
		int m_Handle;

		friend class Server;
	};
} /* OREd */

#endif
