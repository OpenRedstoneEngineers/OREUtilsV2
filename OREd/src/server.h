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

#ifndef _ORED_SERVER_
#define _ORED_SERVER_

#include <sys/types.h> 
#include <sys/socket.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \brief Incoming connection callback.
 *
 * \return whether to accept the incoming connection.
 */
typedef int (*ConnectionCB)(int sockFd);

/* Client disconnected. */
typedef void (*DisconnectCB)(int sockFd);

/* Incmoning message callback. */
typedef void (*MessageCB)(int sockFd, const char* msg);

/* Double-linked list */
typedef struct client_node_
{
	struct client_node_* next;
	struct client_node_* prev;

	int sockFd;
} client_node;

/**
 * \brief Represents a server instance.
 */
typedef struct server_
{
	/* File descriptor. */
	int sockFd;

	/* Callback functions. */
	ConnectionCB connectCb;
	DisconnectCB disconnectCb;
	MessageCB msgCb;

	/* Client list head */
	client_node* firstClient;

	/* Boolean flag indicating whether the server is running. */
	int serving;
} server;

/**
 * \brief Create a new server instance.
 *
 * \param port Port number.
 *
 * On failure, a NULL pointer will be returned.
 *
 * NOTE: This function will create a standard IPv4 TCP 
 * socket, unless the macro ORE_USE_IPV6 is defined.
 */
server* server_init(int port);

/**
 * \brief Start serving.
 *
 * NOTE: This function should be called on a separate thread.
 */
void server_serve(server* serv);

/**
 * \brief Terminate a server.
 *
 * WARNING: The pointer will be invalidated.
 */
void server_terminate(server* serv);

#ifdef __cplusplus
}
#endif

#endif
