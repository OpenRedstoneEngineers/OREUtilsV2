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

#include "proto_server.h"

#include "daemon.h"

#include <stdlib.h>
#include <assert.h>
#include <string.h>

static int proto_server_handle_connect(int sockFd)
{
	// TODO: Authenticate

	return 1;
}

static void proto_server_handle_disconnect(int sockFd)
{

}

static void proto_server_handle_message(int sockFd, const char* msg)
{
	// TODO: Tokenize	
}

proto_server* proto_server_init(int port, const char* name)
{
	assert(name != NULL);

	proto_server* proto = malloc(sizeof(proto_server));

	if (proto == NULL)
	{
		return NULL;
	}

	proto->serv = server_init(port);

	if (proto->serv == NULL)
	{
		free(proto);

		return NULL;
	}

	proto->serv->connectCb = proto_server_handle_connect;
	proto->serv->disconnectCb = proto_server_handle_disconnect;
	proto->serv->msgCb = proto_server_handle_message;

	proto->firstConn = NULL;

	return proto;
}

int proto_server_connect_serv(proto_server* serv, const char* name, client cli)
{
	assert(serv != NULL);

	proto_server_conn* conn = malloc(sizeof(proto_server_conn));

	if (conn == NULL)
	{
		return 0;
	}

	conn->sockFd = cli;

	assert(name != NULL);

	conn->servName = name;

	conn->next = serv->firstConn;

	serv->firstConn = conn;

	return 1;
}

client proto_server_get_serv(proto_server* serv, const char* name)
{
	assert(serv != NULL);

	// OPTIMIZE: Binary search

	proto_server_conn* it = serv->firstConn;

	while (it != NULL)
	{
		if (strcmp(it->servName, name) == 0)
		{
			return it->sockFd;
		}
	}

	return -1;
}

void proto_server_terminate(proto_server* serv)
{
	assert(serv != NULL);

	server_terminate(serv->serv);

	free(serv);
}
