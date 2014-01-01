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

#ifndef _ORED_RSAKEY_
#define _ORED_RSAKEY_

#include <string>

namespace OREd
{
	/**
	 * \brief Encapsulates a RSA key pair.
	 */
	class RSAKey
	{
	public:
		RSAKey() {}

		/**
		 * \brief Generate a new RSA key pair.
		 */
		void Generate();

		void SetPublicKey(const std::string& key);

		void SetPrivateKey(const std::string& key);

		/**
		 * \return the associated public key.
		 */
		std::string GetPublicKey() const;

		/**
		 * \return the associated private key.
		 */
		std::string GetPrivateKey() const;

		/**
		 * \brief Encrypt the specified message.
		 */
		std::string Encrypt(const std::string& msg) const;

		/**
		 * \brief Decrypt the specified message.
		 */
		std::string Decrypt(const std::string& msg) const;

	protected:
		std::string m_Public;

		std::string m_Private;
	};

	void RSAKey::SetPublicKey(const std::string& key)
	{
		m_Public = key;
	}

	void RSAKey::SetPrivateKey(const std::string& key)
	{
		m_Private = key;
	}

	std::string RSAKey::GetPublicKey() const
	{
		return m_Public;
	}

	std::string RSAKey::GetPrivateKey() const
	{
		return m_Private;
	}
} /* OREd */

#endif
