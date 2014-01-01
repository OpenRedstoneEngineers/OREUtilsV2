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

#ifndef _ORED_AUTH_
#define _ORED_AUTH_

#include "Client.hpp"

#include "RSAKey.hpp"

#include <string>
#include <vector>

namespace OREd
{
	/**
	 * \brief Interface for authenticators.
	 */
	class Authenticator
	{
	public:
		typedef std::vector<std::string> KeyList;

	public:
		Authenticator() {}

		virtual ~Authenticator() {}

		/**
		 * \brief Authenticate as a server.
		 */
		virtual bool AuthServerIn(Client* remote);

		/**
		 * \brief Authenticate as a client.
		 */
		virtual bool AuthServerOut(Client* remote);

		/**
		 * \brief Encrypt a network message.
		 */
		virtual std::string EncryptMessage(Client* remote, const std::string& msg);		

		/**
		 * \brief Decrypt a network message.
		 */
		virtual std::string DecryptMessage(Client* remote, const std::string& msg);

	protected:
		RSAKey m_Key;

		KeyList m_KnownKeys;
	};
} /* OREd */

#endif
