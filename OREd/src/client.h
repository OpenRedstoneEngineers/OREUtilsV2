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

#ifndef _ORED_CLIENT_
#define _ORED_CLIENT_

#include <sys/types.h> 
#include <sys/socket.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \brief Represents a connection to a remote host.
 */
typedef int client;

/**
 * \brief Create a new client socket.
 *
 * \param host Hostname (NULL-terminated string).
 * \param service NULL-terminated string specifiying a service (e.g. http) or a port.
 *
 * On failure, a negative value will be returned.
 * 
 * On success, a file descriptor will be returned.
 * 
 * NOTE: This function will create a standard IPv4 TCP 
 * socket, unless the macro ORE_USE_IPV6 is defined.
 */
client client_init_host_service(const char* host, const char* service);

/**
 * \brief Create a new client socket.
 *
 * \param addrs IP Address. (NULL-terminated string)
 * \param port Port.
 *
 * On failure, a negative value will be returned.
 * 
 * On success, a file descriptor will be returned.
 * 
 * NOTE: This function will create a standard IPv4 TCP 
 * socket, unless the macro ORE_USE_IPV6 is defined.
 */
client client_init_host_port(const char* addrs, int port);

/**
 * \brief Terminate a client socket connection.
 */
void client_terminate(client cli);

#ifdef __cplusplus
}
#endif

#endif
