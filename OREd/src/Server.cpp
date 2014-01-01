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

#include "Server.hpp"

#include <sys/types.h> 
#include <sys/socket.h>

#include <netinet/in.h>

#include <fcntl.h>
#include <unistd.h>

#include <string.h>

#define BACKLOG 5

#define TIMEOUT_SEC 3

namespace OREd
{
	Server::Server(const int port) : m_Running(false), m_Handle(-1)
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

		struct sockaddr_in serv_addr;

		bzero((char*) &serv_addr, sizeof(serv_addr));

		serv_addr.sin_family = AF_INET;
		serv_addr.sin_addr.s_addr = INADDR_ANY;
		serv_addr.sin_port = htons(port);

		if (bind(m_Handle, (struct sockaddr*) &serv_addr, sizeof(serv_addr)) < 0)
		{
			close(m_Handle);

			m_Handle = -1;

			return;
		}
	}

	Server::~Server()
	{
		for (ClientList::iterator it = m_Clients.begin(); it != m_Clients.end(); ++it)
		{
			delete *it;
		}

		if (IsValid())
		{
			close(m_Handle);
		}
	}

	bool Server::IsValid() const
	{
		return m_Handle >= 0;
	}

	void Server::Start()
	{
		if (m_Running || !IsValid())
		{
			return;
		}

		if (listen(m_Handle, BACKLOG) < 0)
		{
			return;
		}

		m_Running = true;

		struct timeval timeout;

		timeout.tv_sec = TIMEOUT_SEC;
		timeout.tv_usec = 0;

		fd_set fds;

		while (m_Running)
		{
			FD_ZERO(&fds);

			FD_SET(m_Handle, &fds);

			for (ClientList::iterator it = m_Clients.begin(); it != m_Clients.end(); ++it)
			{
				FD_SET((*it)->m_Handle, &fds);
			}

			if (select(sizeof(fds) * 8, &fds, NULL, NULL, &timeout) < 0)
			{
				break;
			}

			if (FD_ISSET(m_Handle, &fds))
			{
				struct sockaddr_in cli_addr;

				unsigned int clilen = sizeof(cli_addr);

				int cliSockFd = accept(m_Handle, (struct sockaddr*) &cli_addr, &clilen);

				if (cliSockFd < 0)
				{
					m_Running = false;

					break;
				}

				Client* cli = new Client(cliSockFd);

				if (OnConnect(cli))
				{
					m_Clients.push_back(cli);
				}
				else
				{
					delete cli;
				}
			}

			for (ClientList::iterator it = m_Clients.begin(); it != m_Clients.end();)
			{
				if (FD_ISSET((*it)->m_Handle, &fds))
				{
					std::string msg;

					if (!(*it)->Recv(msg))
					{
						delete *it;

						ClientList::iterator temp = it;

						++it;

						m_Clients.erase(temp);

						continue;
					}

					OnMessage(*it, msg);
				}

				++it;
			}
		}
	}

	void Server::Stop()
	{
		m_Running = false;
	}

	void Server::BroadcastMessage(const std::string& msg)
	{
		for (ClientList::iterator it = m_Clients.begin(); it != m_Clients.end(); ++it)
		{
			(*it)->Send(msg);
		}
	}
} /* OREd */
