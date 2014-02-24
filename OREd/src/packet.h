/** OREd/packet.h: Interface for OREd's basic protocol packet generation/management.
 * Copyright: GPLv3
 * Created:  2014-02-23 | redstonewarrior
 * Contributors:
 *     - redstonewarrior
 * Changelog:
 *     2014-02-23 | Created utility interface, buffer based. | redstonewarrior
 * Description: This file contains the functions that generate and parse
 *     packets in OREd's simple message format. The format is described below.
 *     It is used on both OREd->OREd SSL sockets and on local unix sockets.
 * Plans:
 *
 * Further copyright information:
 *     Copyright (C) 2013 OpenRedstone
 *
 *     This program is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     This program is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __ORED_PACKET_H
#define __ORED_PACKET_H

/*****************/
/* Dependencies: */

/* This interface deals mostly with buffers. We only need ored_msg. */
#include "routing.h"

/*********************/
/* Useful functions: */

/* These functions deal with packets in OREd's simple packet format.
 * The format is text based, and is as follows:
 * DST SRC MSG\0...
 * There may not be NULL characters in the message.
 * DST: Destination VHost name and domain. Examples:
 * build.servers
 * rsw.cli
 * rsw.kicker.utils
 * And so on.
 * SRC: Source VHost name and domain.
 * MSG: A message. Usually in the form of CMD ARG....
 * This is a simple packet used for routing messages on the OREd
 * network. Barely worth mentioning. Clients will have their own
 * interfaces, but that is not specified here.
 */

/* Allocates string. */
char *get_src(const char *pkt);
char *get_dst(const char *pkt);
ored_msg get_msg(const char *pkt);

/* Please lock your vhosts. (ReadOnly) */
char *mk_pkt(struct ored_vhost *dst, struct ored_vhost *src, const ored_msg msg);

/* Subdomain / name splitting. */
char *get_name(const char *vhost);
char *get_domain(const char *vhost);

#endif // __ORED_PACKET_H
