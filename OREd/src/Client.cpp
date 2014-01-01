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

#include "Client.hpp"

#include <sys/types.h> 
#include <sys/socket.h>

#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

#include <fcntl.h>
#include <unistd.h>

#include <string.h>

namespace OREd
{
	Client::Client(const std::string& host, const std::string& service)
	{
		#ifndef ORE_USE_IPV6
		m_Handle = socket(AF_INET, SOCK_STREAM, 0);
		#else
		m_Handle = socket(AF_INET6, SOCK_STREAM, 0);
		#endif

		if (m_Handle < 0)
		{
			return;
		}

		struct addrinfo hints;

		bzero(&hints, sizeof(struct addrinfo));

		hints.ai_family = AF_UNSPEC;
		hints.ai_socktype = SOCK_STREAM;
		hints.ai_flags = 0;
		hints.ai_protocol = 0;

		struct addrinfo* result;

		if (getaddrinfo(host.c_str(), service.c_str(), &hints, &result) != 0)
		{
			close(m_Handle);

			m_Handle = 0;

			return;
		}

		struct addrinfo* it;

		for (it = result; it != NULL; it = it->ai_next)
		{
			if (connect(m_Handle, it->ai_addr, it->ai_addrlen) != -1)
			{
				break;
			}
		}

		freeaddrinfo(result);

		if (it == NULL)
		{
			close(m_Handle);

			m_Handle = 0;
		}
	}

	Client::Client(const std::string& address, const int port)
	{
		#ifndef ORE_USE_IPV6
		m_Handle = socket(AF_INET, SOCK_STREAM, 0);
		#else
		m_Handle = socket(AF_INET6, SOCK_STREAM, 0);
		#endif

		if (m_Handle < 0)
		{
			return;
		}

		#ifndef ORE_USE_IPV6
		struct sockaddr_in addr;

		addr.sin_family = AF_INET;
		addr.sin_port = htons(port);

		inet_pton(AF_INET, address.c_str(), &addr.sin_addr);
		#else
		struct sockaddr_in6 addr;

		addr.sin6_family = AF_INET6;
		addr.sin6_port = htons(port);

		inet_pton(AF_INET6, address.c_str(), &addr.sin6_addr);
		#endif

		if (connect(m_Handle, (struct sockaddr*) &addr, sizeof(addr)) < 0)
		{
			close(m_Handle);

			m_Handle = 0;
		}
	}

	Client::~Client()
	{
		if (IsValid())
		{
			close(m_Handle);
		}
	}

	bool Client::IsValid() const
	{
		return m_Handle >= 0;
	}

	bool Client::Recv(std::string& msg)
	{
		if (!IsValid())
		{
			return false;
		}

		char buffer[256];

		bzero(buffer, sizeof(buffer));

		if (read(m_Handle, buffer, sizeof(buffer) - 1) < 0)
		{
			return false;
		}

		msg = std::string(buffer);

		return true;
	}

	bool Client::Send(const std::string& msg)
	{
		if (!IsValid())
		{
			return false;
		}

		if (write(m_Handle, msg.c_str(), msg.size()) < 0)
		{
			return false;
		}

		return true;
	}
} /* OREd */
