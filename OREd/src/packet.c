/** OREd/packet.c: Implementation of OREd's basic packet format.
 * Copyright: GPLv3
 * Created:  2014-02-23 | redstonewarrior
 * Contributors:
 *     - redstonewarrior
 * Changelog:
 *     2014-02-23 | Implemented interface. | redstonewarrior
 * Description: This file contains the functions that generate and parse
 *     packets in OREd's simple message format. The format is described
 *     in packet.h.
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

/*****************/
/* Dependencies: */

/* Interface to implement. */
#include "packet.h"

/* String manipulation. */
#include <string.h>

/* snprintf. */
#include <stdio.h>

/* Free/malloc */
#include <stdlib.h>

/*********************/
/* Useful functions: */

char *get_src(const char *pkt) {
	char *tmp = strdup(pkt);
	char *tmp_tok;
	char *ret;
	ret = strdup(strtok_r(tmp, " ", &tmp_tok));
	free(tmp);
	return ret;
}

char *get_dst (const char *pkt) {
	char *tmp = strdup(pkt);
	char *tmp_tok;
	char *ret;
	ret = strtok_r(tmp, " ", &tmp_tok);
	ret = strdup(strtok_r(NULL, " ", &tmp_tok));
	free(tmp);
	return ret;
}

ored_msg get_msg (const char *pkt) {
	char *tmp = strdup(pkt);
	char *tmp_tok;
	char *ret;
	ret = strtok_r(tmp, " ", &tmp_tok);
	ret = strtok_r(NULL, " ", &tmp_tok);
	ret = strdup(strtok_r(NULL, " ", &tmp_tok));
	free(tmp);
	return ret;
}

char *mk_pkt(struct ored_vhost *dst, struct ored_vhost *src, const ored_msg msg) {
	int len =
		strlen(dst->name) + 1 + strlen(dst->domain) + 1 +
		strlen(src->name) + 1 + strlen(src->name) + 1 +
		strlen((const char *)msg) + 1;
	char *ret = (char*) malloc(len);
	snprintf(ret, len, "%s.%s %s.%s %s",
	         dst->name, dst->domain,
	         src->name, src->domain,
	         (const char*) msg);
	return ret;
}

/* Slightly slower than could be, but too lazy to hardcode. */
char *get_name(const char *vhost) {
	char *tmp = strdup(vhost);
	char *tmp_tok;
	char *ret;
	ret = strdup(strtok_r(tmp, ".", &tmp_tok));
	free(tmp);
	return ret;
	
}

char *get_domain(const char *vhost) {
	char *tmp = strdup(vhost);
	char *tmp_tok;
	char *ret;
	ret = strtok_r(tmp, ".", &tmp_tok);
	ret = strdup(strtok_r(NULL, ".", &tmp_tok));
	free(tmp);
	return ret;

}
