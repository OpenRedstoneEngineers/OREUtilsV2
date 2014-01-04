/** OREd/main.c: Programme for daemon's execution.
 * Copyright: GPLv3
 * Created: 2013-12-15 | structinf
 * Contributors:
 *     redstonewarrior
 *     structinf
 * Changelog:
 *     2014-01-03 | Formatted file, moved daemonize(), added ore_logfd,
 *         replaced Log, C'd up the place. | redstonewarrior
 * Description: This file contains the main programme of events.
 * Plans:
 *     -Parse arguments
 *     -Start routing server
 *     -Auth, SSL, local socket
 *     -Local configuration / persistence
 *     -Routing, automatic reconnect
 *     -Virtual routing client
 *     -OREd event handler \
 *     -Bukkit console manager
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

/**************************************/
/* OREd dependencies and assumptions: */

/* Networking / sockets:
 *     Remote clients: libssl
 *     Local clients: POSIX
 */
//#include "sockets.h" To be added.

/* Database / persistence backends:
 *     MySQL: libmysqlclient
 *     File : POSIX
 */
//#include "persist.h" To be added.

/************************/
/* Functional sections: */

/* Daemon information and log file */
#include "daemon.h"

/* ORENet routing and control */
//#include "routing.h" To be added.

/* ORENet client handling */
//#include "controller.h" To be added/changed/removed.

/*******************/
/* Utility headers */

/* I/O operations */
#include <stdio.h>

/* libc types */
#include <stdlib.h>

/* fork(), chdir(), setsid(), ... */
#include <unistd.h>

/* umask() */
#include <sys/types.h>
#include <sys/stat.h>

/* open(), close() */
#include <fcntl.h>

/* Error reporting */
#include <errno.h>
#include <string.h>

/*************/
/* Constants */

/* When persistence is implemented, these will 
 * removed in favor of virtual configuration.
 * Hopefully, all configuration / libs
 * will be symlinked/generated/written before
 * starting the server in /srv/<name> directory.
 */
#define ORED_DEFAULT_DIR        "/servers/ORE"        /* "/srv" */
#define ORED_DEFAULT_LOG_PATH   "/var/log/OREd.log"
#define ORED_DEFAULT_JAVA_BIN   "/usr/bin/java"
#define ORED_DEFAULT_BUKKIT_BIN "/usr/bin/bukkit.jar"
#define ORED_DEFAULT_PLUGIN_DIR "."                   /* "/usr/lib/bukkit" */

/* Java details */
#define JAVA_BIN_NAME "java"
#define JAVA_JAR_FLAG "-jar"

/* Bukkit flags. */
#define BUKKIT_NONINTERACTIVE "--nojline"
#define BUKKIT_STRIP_COLORS   "--log-strip-color"

/********************/
/* Global variables */

/* File descriptor for the log file. Displayed in daemon.h. */
int ore_logfd;

/********************/
/* Useful functions */

/* Forks and kills the parent. Does not transfer threads- read the man
 * pages for more information on fork() side effects. Also starts a new
 * session, though this may be moved later.  Returns nonzero on success,
 * zero on failure. (Check errno.)
 *
 * Failure to fork returns an error. This is in hopes of recovery.
 * Failure to create session reports on stderr, and returns success.
 * Failure to change working directory is fatal to the program.
 * These may be adjusted.
 */
int daemonize(const char *path)
{
	pid_t pid, sid;

	pid = fork(); /* Error < 0 = parent < child */

	if (pid < 0) /* An error occurred. Check errno. */
		return 0;

	if (pid > 0) /* This is the parent process. */
		exit(EXIT_SUCCESS);

	if (chdir(path) < 0) {
		char *cwd;
		fprintf(stderr, "[Error]Daemon: Error: Could not change working directory.\n");
		if (!(cwd = getcwd(NULL, 0))) {
			fprintf(stderr, "[Error]Daemon: Error: Could not get working directory.\n");
			exit(EXIT_FAILURE);
		}
		fprintf(stderr, "[Error]Daemon: From: %s to %s.\n", cwd, path);
		fprintf(stderr, "[Error]Daemon: Reason: %s.\n", strerror(errno));
		free(cwd);
		exit(EXIT_FAILURE);
	}

	sid = setsid();

	if (sid < 0) {
		fprintf(stderr, "[Error]Daemon: Error: Could not create new session group.\n");
		return 0;
	}

	/* Almost certainly succeeds. May add check. */
	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);
	return 1;
}

/******************/
/* Main programme */

/* Will be replaced */
#include "Manager.hpp"

/* Will be burned with the fire of a thousand C-programmed suns */
using namespace OREd;

int main(int argc, const char **argv)
{
	/* Todo: getopt for basic configuration options. */

	/* By setting up the log before daemonizing, write permission
	 * failure on the log file isn't mysterious.
	 */

	ore_logfd = open(ORED_DEFAULT_LOG_PATH, O_WRONLY | O_APPEND | O_CREAT);	
	if (ore_logfd == -1) {
		fprintf(stderr, "[Error]Daemon: Failed to open log path: %s.\n",
		        ORED_DEFAULT_LOG_PATH);
		fprintf(stderr, "[Error]Daemon: Reason: %s.\n", strerror(errno));
		exit(EXIT_FAILURE);
	}

	if (!daemonize(ORED_DEFAULT_DIR))
	{
		fprintf(stderr, "[Error]Daemon: Unable to fork: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}

	umask(0); /* Never fails. */

	Manager manager(4242, "skaro");

	char * args[] = {
		/* Program name as first argument */
		(char*) JAVA_BIN_NAME,
		/* Tell java to use the bukkit executable. */
		(char*) JAVA_JAR_FLAG, (char*) ORED_DEFAULT_BUKKIT_BIN,
		/* Makes console noninteractive and rips color from logs. */
		(char*) BUKKIT_NONINTERACTIVE, (char*) BUKKIT_STRIP_COLORS,
		/* Terminating NULL string. */
		(char*) NULL
	};

	Console build(ORED_DEFAULT_JAVA_BIN, args);

	manager.Start();

	dprintf(ore_logfd, "Exiting...\n");

	exit(EXIT_SUCCESS);
}
