/** OREd/route.h: Daemon's routing interface management interface.
 * Copyright: GPLv3
 * Created: 2014-01-23 | redstonewarrior
 * Contributors:
 *     redstonewarrior
 * Changelog:
 *     2014-01-23 | Created basic routing logic. | redstonewarrior
 *     2014-02-22 | Cleaned up, added registration system, created
 *         simpler local / remote callback interface. | redstonewarrior
 *     2014-02-23 | Implemented interface. | redstonewarrior
 * Description: This file contains an interface for managing hosts
 *     and vhosts. This includes registering callbacks and a few helpful
 *     functions for dealing with locks. (Please don't deadlock me.)
 *     Different modules of code register callbacks, whether they be
 *     to a unix pipe or an SSL one.
 * Plans:
 *     - Implement unix module.
 *     - Implement perhost, perdomain, and * vhost listing.
 *     - Implement ssl module.
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

#ifndef __ORED_ROUTE_H
#define __ORED_ROUTE_H

/*****************/
/* Dependencies: */

/* Threading (rwlocks): */
#include <pthread.h>

/*******************************/
/* Routing related structures: */

/* This structure is managed by the
 * routing and server modules. There is
 * one global ored_host, available
 * below. (The current host.)
 */
struct ored_host {

	/* For removing in a multithreaded
	 * environment. */
	pthread_rwlock_t lock;

	/* rsw.openredstone.org */
	char *url;

	/* Since we register callbacks in ored_vhost,
	 * they're not necessary here. If you can think
	 * of any other good fields, please commit :3
	 */
};


/* We hide the internals of a packet in the various routing
 * modules. The public interface only uses a message, sender,
 * and receiver setup.
 */
typedef char *ored_msg;

/* Callback for handling incomming messages.
 * Is used on same thread as send_msg function,
 * it's recommended that you use proper threading
 * (Maybe not even a write() in it.)
 * Note: You're inside an R/W Lock while running this.
 * If you choose to free your mutex, problems will occur.
 * Just... send it down a queue, okay? Let another thread
 * do the dirty work.
 */
struct ored_vhost;
typedef void (*ored_callback)(struct ored_vhost *dst,
                              struct ored_vhost *src,
                              const ored_msg msg);



/* Reference to a virtual host on the ORE network. */
struct ored_vhost {

	/* Function to call to send message to a host.
	 * May go through the network. Please thread
	 * properly, and don't do many write()s.
	 */
	ored_callback callback;

	/* To ensure that noone cleans up a vhost
	 * while someone else is attempting to route to it.
	 */
	pthread_rwlock_t lock;
	/* NULL if current host. */
	struct ored_host *curr_host;
	char *name; /* rsw, ban, ... */
	char *domain; /* host, bukkit, cli, .... */
};

/*********************/
/* Global variables: */

/* Generated on route_init(), and free'd on route_kill(). */
extern struct ored_host curr_host;

/*********************/
/* Shared functions: */

/* Sends a specified message to a specified vhost
 * from a specified vhost over an unspecified protocol.
 * Internals are defined in routing.c.
 * ORE_MSGs are usually C strings, and may not contain
 * NULL characters in the payload (on pains of
 * truncation.)
 * OREd->OREd threads will call this as a wrapper over
 * the callback system, to pass the message onto local hosts.
 * Do lock your vhosts before entering.
 * Returns 1 on success, 0 on failure.
 */
int send_msg(struct ored_vhost *dst,
             struct ored_vhost *src,
             const ored_msg msg);

/* Send message to a domain rather than a specific host.
 * If src is in specified domain, do not send message to src.
 * Automatically locks all vhosts involved.
 * Returns number of messages sent.
 */
int send_msg_dom(const char *domain,
                 struct ored_vhost *src,
                 const ored_msg msg);

/* Register a new virtual host and handler function
 * for messages. Initializes rwlock.
 */
int init_vhost(struct ored_vhost *host);

/* For those of you who don't know pthreads: */
int rlock_vhost(struct ored_vhost *host);
int wlock_vhost(struct ored_vhost *host);
int ulock_vhost(struct ored_vhost *host);

/* Destroys a vhost. Don't look too closely. */
int kill_vhost(struct ored_vhost *host);

/* Finds a specified vhost structure. */
struct ored_vhost *get_vhost(const char *name);

/* Hosts are usually managed by the providing module.
 * Some helpful functions, for those who don't know pthreads.
 */
/* (First/last == init/kill) */
int ilock_host(struct ored_host *host);
int rlock_host(struct ored_host *host);
int wlock_host(struct ored_host *host);
int ulock_host(struct ored_host *host);
int klock_host(struct ored_host *host);

/* Init/kill routing module. */
void init_routing();
void kill_routing();

#endif /* __ORED_ROUTE_H */
