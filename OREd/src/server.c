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

#include "server.h"

#include <sys/types.h> 
#include <sys/socket.h>

#include <netinet/in.h>

#include <fcntl.h>
#include <unistd.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define BACKLOG 5

#define TIMEOUT_SEC 3

static client_node* server_push_client(server* serv, int sockFd)
{
	assert(serv != NULL);

	client_node* node = malloc(sizeof(client_node));

	if (node == NULL)
	{
		return NULL;
	}

	node->sockFd = sockFd;

	node->next = serv->firstClient;

	node->prev = NULL;

	if (serv->firstClient != NULL)
	{
		serv->firstClient->prev = node;
	}

	serv->firstClient = node;

	return node;
}

static int server_pop_client(server* serv, client_node* node)
{
	assert(serv != NULL);

	if (serv->firstClient == node)
	{
		serv->firstClient = node->next;
	}

	if (node->prev != NULL)
	{
		node->prev->next = node->next;
	}

	if (node->next != NULL)
	{
		node->next->prev = node->prev;
	}

	free(node);

	return 1;
}

server* server_init(int port)
{
	server* serv = malloc(sizeof(server));

	if (serv == NULL)
	{
		return NULL;
	}

	#ifndef ORE_USE_IPV6
	serv->sockFd = socket(AF_INET, SOCK_STREAM, 0);
	#else
	serv->sockFd = socket(AF_INET6, SOCK_STREAM, 0);
	#endif

	if (serv->sockFd < 0)
	{
		free(serv);

		return NULL;
	}

	struct sockaddr_in serv_addr;

	bzero((char*) &serv_addr, sizeof(serv_addr));

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(port);

	if (bind(serv->sockFd, (struct sockaddr*) &serv_addr, sizeof(serv_addr)) < 0)
	{
		close(serv->sockFd);

		free(serv);

		return NULL;
	}

	serv->serving = 0;

	return serv;
}

void server_serve(server* serv)
{
	assert(serv != NULL);

	listen(serv->sockFd, BACKLOG);

	struct timeval timeout;

	timeout.tv_sec = TIMEOUT_SEC;
	timeout.tv_usec = 0;

	fd_set fds;

	serv->serving = 1;

	while (serv->serving)
	{
		FD_ZERO(&fds);

		FD_SET(serv->sockFd, &fds);

		client_node* it = serv->firstClient;

		while (it != NULL)
		{
			FD_SET(it->sockFd, &fds);

			it = it->next;
		}

		if (select(sizeof(fds) * 8, &fds, NULL, NULL, &timeout) < 0)
		{
			break;
		}

		if (FD_ISSET(serv->sockFd, &fds))
		{
			struct sockaddr_in cli_addr;

			unsigned int clilen = sizeof(cli_addr);

			int cliSockFd = accept(serv->sockFd, (struct sockaddr*) &cli_addr, &clilen);

			if (cliSockFd < 0)
			{
				break;
			}

			if (serv->connectCb != NULL)
			{
				if ((serv->connectCb)(cliSockFd))
				{
					server_push_client(serv, cliSockFd);

					FD_SET(cliSockFd, &fds);
				}
				else
				{
					close(cliSockFd);
				}
			}
		}

		it = serv->firstClient;

		while (it != NULL)
		{
			if (FD_ISSET(it->sockFd, &fds))
			{
				char buffer[256];

				bzero(buffer, sizeof(buffer));

				if (read(it->sockFd, buffer, sizeof(buffer) - 1) < 0)
				{
					if (serv->disconnectCb != NULL)
					{
						(serv->disconnectCb)(it->sockFd);
					}

					client_node* temp = it;

					it = it->next;

					server_pop_client(serv, temp);

					continue;
				}

				if (serv->msgCb != NULL)
				{
					(serv->msgCb)(it->sockFd, (char*) buffer);
				}
			}

			it = it->next;
		}
	}
}

void server_terminate(server* serv)
{
	assert(serv != NULL);

	serv->serving = 0;

	client_node* it = serv->firstClient;

	while (it != NULL)
	{
		close(it->sockFd);

		client_node* temp = it;

		it = it->next;

		free(temp);
	}

	close(serv->sockFd);

	free(serv);
}
