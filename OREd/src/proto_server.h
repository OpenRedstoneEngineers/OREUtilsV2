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

#ifndef _ORED_PROTO_SERVER_
#define _ORED_PROTO_SERVER_

#include "server.h"

#include "client.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum proto_cmd_
{
	cmd_unknown = -1,

	/* Normal commands */
	cmd_kill,
	cmd_restart,
	cmd_broadcast,

	/* Special */
	cmd_query,
	cmd_event,

	cmd_count
} proto_cmd;

typedef int (*HandleCmd)(proto_cmd cmd, const char* argv[], int argc);

/**
 * \brief Represents a server-to-server connection.
 */
typedef struct proto_server_conn_
{
	struct proto_server_conn_* next;

	/* Server name */
	const char* servName;

	/* File descriptor */
	client sockFd;
} proto_server_conn;

typedef struct proto_server_
{
	/* Server instance */
	server* serv;

	/* Server connections list head */
	proto_server_conn* firstConn;

	/* Server name */
	const char* name;
} proto_server;

/**
 * \brief Create a new protocol server.
 *
 * On failure, NULL will be returned.
 */
proto_server* proto_server_init(int port, const char* name);

/**
 * \brief Connect to another server.
 */
int proto_server_connect_serv(proto_server* serv, const char* name, client cli);

/**
 * \return the server with the specified name.
 */
client proto_server_get_serv(proto_server* serv, const char* name);

/**
 * \brief Terminate a protocol server.
 */
void proto_server_terminate(proto_server* serv);

#ifdef __cplusplus
}
#endif

#endif
