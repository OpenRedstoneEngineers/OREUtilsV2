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

#include "client.h"

#include <sys/types.h> 
#include <sys/socket.h>

#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

#include <fcntl.h>
#include <unistd.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

client client_init_host_service(const char* host, const char* service)
{
	#ifndef ORE_USE_IPV6
	client cli = socket(AF_INET, SOCK_STREAM, 0);
	#else
	client cli = socket(AF_INET6, SOCK_STREAM, 0);
	#endif

	if (cli < 0)
	{
		return -1;
	}

	struct addrinfo hints;

	bzero(&hints, sizeof(struct addrinfo));

	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = 0;
	hints.ai_protocol = 0;

	struct addrinfo* result;

	if (getaddrinfo(host, service, &hints, &result) != 0)
	{
		close(cli);

		return -1;
	}

	struct addrinfo* it;

	for (it = result; it != NULL; it = it->ai_next)
	{
		if (connect(cli, it->ai_addr, it->ai_addrlen) != -1)
		{
			break;
		}
	}

	freeaddrinfo(result);

	if (it == NULL)
	{
		close(cli);

		return -1;
	}

	return cli;
}

client client_init_addr_port(const char* addrs, int port)
{
	#ifndef ORE_USE_IPV6
	client cli = socket(AF_INET, SOCK_STREAM, 0);
	#else
	client cli = socket(AF_INET6, SOCK_STREAM, 0);
	#endif

	if (cli < 0)
	{
		return -1;
	}

	#ifndef ORE_USE_IPV6
	struct sockaddr_in addr;

	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);

	inet_pton(AF_INET, addrs, &addr.sin_addr);
	#else
	struct sockaddr_in6 addr;

	addr.sin6_family = AF_INET6;
	addr.sin6_port = htons(port);

	inet_pton(AF_INET6, addrs, &addr.sin6_addr);
	#endif

	if (connect(cli, (struct sockaddr*) &addr, sizeof(addr)) < 0)
	{
		close(cli);

		return -1;
	}

	return cli;
}

void client_terminate(client cli)
{
	assert(cli >= 0);

	close(cli);
}
