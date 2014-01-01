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

#include "Auth.hpp"

namespace OREd
{
	bool Authenticator::AuthServerIn(Client* remote)
	{
		// TODO: Listen for public key

		remote->m_Type = Client::TYPE_LISTENER;

		return false;
	}

	bool Authenticator::AuthServerOut(Client* remote)
	{
		// TODO: Send public key

		remote->m_Type = Client::TYPE_LISTENER;

		return false;
	}

	std::string Authenticator::EncryptMessage(Client* remote, const std::string& msg)
	{
		return m_Key.Encrypt(msg);
	}

	std::string Authenticator::DecryptMessage(Client* remote, const std::string& msg)
	{
		return m_Key.Decrypt(msg);
	}
} /* OREd */
