/** OREd/routing.c: Functions to manage and determine appropraite handlers.
 * Copyright: GPLv3
 * Created: 2014-01-24 | redstonewarrior
 * Contributors:
 *     redstonewarrior
 * Changelog:
 *     2014-01-24 | Created file, basic routing. | redstonewarrior
 *     2014-02-23 | Rebuilt file, implemented functions using
 *         quick, basic, naive algorithms. | redstonewarrior
 * Description: This file contains the code that manages hosts, vhosts,
 *     and send message functors and mutexes. Manages calls and routes
 *     messages.
 * Plans:
 *     -Binary search on vhosts lookup, linear for now (lazy)
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

/**********************/
/* OREd dependencies: */

/* Definitions and prototypes */
#include "routing.h"

/* Log file */
#include "daemon.h"

/*******************/
/* Utility headers */

/* I/O operations */
#include <stdio.h>

/* libc types */
#include <stdlib.h>

/* POSIX calls and types. */
#include <unistd.h>

/* open(), close() */
#include <fcntl.h>

/* Error reporting */
#include <errno.h>
#include <string.h>

/***************/
/* Global vars */

/* Vhost list. Sorted by domain, hostname. */
struct ored_vhost **vhosts = NULL;
int vhosts_count = 0;
pthread_rwlock_t vhosts_lock;

/* Current host. */
struct ored_host curr_host;

/*********************/
/* Shared functions: */

/* Call's vhost's send method. */
int send_msg(struct ored_vhost *dst,
                     struct ored_vhost *src,
                     ored_msg msg) {
	if (!dst || !src) {
		dprintf(ore_logfd, "[Error]Daemon: Attempted to send or receive message to/from invalid host. Src: %p, Dst: %p .\n", src, dst);
		return 0;
	}

	if (!dst->callback) {
		dprintf(ore_logfd, "[Error]Daemon: Attempted to call NULL callback in send_msg.\n");
		dprintf(ore_logfd, "[Error]Daemon: Info: dst: %s.%s, src: %s.%s, msg: %s.\n",
		        dst->name, dst->domain, src->name, src->domain, (const char*) msg);
		return 0;
	}
	dst->callback(dst,src,msg);
	return 1;
}

int send_msg_dom(const char *domain, struct ored_vhost *src, ored_msg msg) {
	if (!domain || !src) {
		dprintf(ore_logfd, "[Error]Daemon: Attempted to send/receive message to/from invalid domain/host. Src: %p, to Domain: %s.\n",
		        src, domain);
		return 0;
	}

	/* TODO: Binary search. */

	pthread_rwlock_rdlock(&vhosts_lock);
	int i;
	for (i = 0; i < vhosts_count; i++) {
		pthread_rwlock_rdlock(&vhosts[i]->lock);
		if (!strcmp (vhosts[i]->domain, domain)) {
			pthread_rwlock_unlock(&vhosts[i]->lock);
			break;
		}
		pthread_rwlock_unlock(&vhosts[i]->lock);
	}
	int count = 0;
	pthread_rwlock_rdlock(&src->lock);
	for (; i < vhosts_count; i++) {
		if (vhosts[i] == src) continue; /* Careful, don't deadlock yourself :3 */
		pthread_rwlock_rdlock(&vhosts[i]->lock);
		if (strcmp(vhosts[i]->domain, domain)) {
			pthread_rwlock_unlock(&vhosts[i]->lock);
			break;
		}
		count += send_msg(vhosts[i], src, msg);
		pthread_rwlock_unlock(&vhosts[i]->lock);
	}
	pthread_rwlock_unlock(&src->lock);
	pthread_rwlock_unlock(&vhosts_lock);
	return count;
}


/* Vhost managing functions. */
int init_vhost(struct ored_vhost *host) {

	/* Validation. */
	int j = host->name && host->domain;
	if (j)
		j = j && host->name[0] && host->domain[0];
	j = j && host->callback;
	if (!j) {
		const char *url = NULL;
		if (host->curr_host) {
			pthread_rwlock_rdlock(&host->curr_host->lock);
			url = host->curr_host->url;
			pthread_rwlock_unlock(&host->curr_host->lock);
		}
		dprintf(ore_logfd, "[Error]Daemon: Attempted to register vhost without a name.\n");

		dprintf(ore_logfd, "[Error]Daemon: Information: name.domain: %s.%s. Host URL: %s.\n", host->name, host->domain, url);
		return -1;
	}

	pthread_rwlock_wrlock(&vhosts_lock);

	/* Could make searching O(log(n)). Meh. */
	int i;
	for (i = 0; i < vhosts_count; i++)
		if (strcmp(vhosts[i]->domain,host->domain) > 0)
			break;
	for (; i < vhosts_count; i++)
		if (strcmp(vhosts[i]->name, host->name) > 0)
			break;
	vhosts_count++;
	vhosts = (struct ored_vhost **) realloc(&vhosts, vhosts_count * sizeof(struct ored_vhost*));
	int i2;
	/* Basic bubble */
	for (i2 = vhosts_count-1; i2 > i; i2--)
		vhosts[i2] = vhosts[i2-1];
	vhosts[i] = host;

	pthread_rwlock_unlock(&vhosts_lock);
	return pthread_rwlock_init(&host->lock, NULL);
}

int kill_vhost(struct ored_vhost *host) {
	pthread_rwlock_rdlock(&vhosts_lock);

	int ret = pthread_rwlock_destroy(&host->lock);

	/* Remove list entry. */
	int i = 0;
	for (i = 0; i < vhosts_count; i++) {
		if (vhosts[i] == host)
			break;
	}

	if (i == vhosts_count) {
		dprintf(ore_logfd, "[Error]Daemon: Attempted to kill unregistered vhost. Ignoring.\n");
		pthread_rwlock_unlock(&vhosts_lock);
		return -1;
	}

	/* Basic bubbling. O(n). */
	for (; i < vhosts_count - 1; i++)
		vhosts[i] = vhosts[i+1];

	vhosts_count--;
	/* Let libc do memory management for us. */
	vhosts = (struct ored_vhost **) realloc(&vhosts, vhosts_count * sizeof (struct ored_vhost*));

	pthread_rwlock_unlock(&vhosts_lock);

	return ret;
}

struct ored_vhost *get_vhost(const char *name) {
	/* TODO: Basic binary serach. */
	int i;
	/* Get name and domain (Manually, just as easy as strtok.) */ 
	int t;
	for (t = 0; name[t] && (name[t] != '.'); t++);
	/* DO NOT register vhosts without domain names. I will eat your soul. */
	if (!name[t]) {/* No names found. */
		dprintf(ore_logfd, "[Error]Daemon: Could not get domain name when finding vhost.\n[Error]Info: name: %s.\n", name);
		return NULL;
	}
	/* Host = name[:i-1], domain=name[i+1:]. */
	pthread_rwlock_rdlock(&vhosts_lock);
	for (i = 0; i < vhosts_count; i++)
		if (!strcmp(vhosts[i]->domain, name + i + 1))
			break;
	for (; i < vhosts_count; i++)
		if (!strncmp(vhosts[i]->name, name, i))
			break;
	/* We let the calling function choose to show an error message. */
	if (i == vhosts_count)
		return NULL;
	else
		return (struct ored_vhost*) (vhosts + i);
		
}

int rlock_vhost(struct ored_vhost *host) {
	return pthread_rwlock_rdlock(&host->lock);
}
int wlock_vhost(struct ored_vhost *host) {
	return pthread_rwlock_wrlock(&host->lock);
}
int ulock_vhost(struct ored_vhost *host) {
	return pthread_rwlock_unlock(&host->lock);
}


int ilock_host(struct ored_host *host) {
	return pthread_rwlock_init(&host->lock,NULL);
}
int rlock_host(struct ored_host *host) {
	return pthread_rwlock_rdlock(&host->lock);
}
int wlock_host(struct ored_host *host) {
	return pthread_rwlock_wrlock(&host->lock);
}
int ulock_host(struct ored_host *host) {
	return pthread_rwlock_unlock(&host->lock);
}
int klock_host(struct ored_host *host) {
	return pthread_rwlock_destroy(&host->lock);
}
