/** OREd/main.c: Programme for daemon's execution.
 * Copyright: GPLv3
 * Created: 2013-12-15 | structinf
 * Contributors:
 *     redstonewarrior
 *     structinf
 * Changelog:
 *     2014-01-03 | Formatted file, moved daemonize(), added ore_logfd,
 *         replaced Log, C'd up the place. | redstonewarrior
 *     2013-01-23 | Added arg parsing, configuration file parsing, configuration
 *         options, stdin parsing, debug mode. | redstonewarrior
 * Description: This file contains the main programme of events.
 * Plans:
 *     -SSL (AUTH), local socket
 *     -OREd virtual client + bukkit handler
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

/************************/
/* Functional sections: */

/* Daemon information and log file */
#include "daemon.h"

/* ORENet routing and control */
#include "routing.h"

/* ORENet client handling */
//#include "controller.h" To be added/changed/removed.

/*******************/
/* Utility headers */

/* I/O operations */
#include <stdio.h>

/* libc types */
#include <stdlib.h>

/* POSIX calls and types. */
#include <unistd.h>

/* umask() */
#include <sys/types.h>
#include <sys/stat.h>

/* open(), close() */
#include <fcntl.h>

/* Character defs */
#include <ctype.h>

/* Error reporting */
#include <errno.h>
#include <string.h>

/*************/
/* Constants */

/* When persistence is implemented, these may be
 * removed in favor of virtual configuration.
 * Hopefully, all configuration / libs
 * will be symlinked/generated/written before
 * starting the server in /srv/<name> directory.
 */
#define ORED_USAGE_FORMAT       \
"%s [-c /path/to/config] [-l /path/to/logfile | -l -] [-d debug_level] [-p persistence_string]"
#define ORED_DEFAULT_DIR         "."
#define ORED_DEFAULT_LOG_PATH    "/var/log/OREd.log"
#define ORED_DEFAULT_CONFIG_PATH "/etc/OREd.conf"
#define ORED_DEFAULT_JAVA_BIN    "/usr/bin/java"
#define ORED_DEFAULT_BUKKIT_BIN  "/usr/bin/bukkit.jar"
#define ORED_DEFAULT_PLUGIN_DIR  "."                   /* To be: "/usr/lib/bukkit" */
#define ORED_DEFAULT_DEBUG_LEVEL 0

/* True/false strings. */
#define ORED_TRUE  "true"
#define ORED_FALSE "false"
/* Silly, but I need these constants elsewhere. */

/* Java details */
#define JAVA_JAR_FLAG "-jar"

/* Bukkit flags. */
#define BUKKIT_NONINTERACTIVE "--nojline"
#define BUKKIT_STRIP_COLORS   "--log-strip-color"

/********************/
/* Global variables */

/* daemon.h config and global daemon variables. */
/* Log file handle. */
int ore_logfd;

/* Config options. Const after init. */
char *ore_config       = NULL; /* Config path.         */
char *ore_log          = NULL; /* Log file path.       */
char *ore_java         = NULL; /* JVM executable.      */
char *ore_jar_flag     = NULL; /* Java -jar flag.      */
char *ore_bukkit       = NULL; /* Bukkit jar path.     */
char *ore_plugins      = NULL; /* Bukkit plugin dir.   */
int   ore_debug        = 0;    /* Debug level          */
char *ore_debug_c      = NULL  /* Ignore.              */

/* One time use. Not global to daemon. */
/* Examples:
 *     mysql://user@host/DB:password
 *     file://path/to/file
 * No other formats are supported currently.
 */
char *ore_persist = NULL;
char *ore_tofork = NULL;

/********************/
/* Useful functions */

/* Reads the configuration file.
 * Sets variables in options[][].
 * If unknown option, skips.
 * If invalid line, exits.
 */
void read_config() {
	FILE* config_file;
	/* If a config file is specified, read that file. If is specified
	 * and name is '@', then read from stdin. If neither, do not read
	 * config.
	 */
	if (!strcmp(ore_config, "-")) { /* Read from stdin until EOF */
		config_file = stdin;
	} else {
		config_file = fopen(ore_config, "r");
		if (!config_file) {
			fprintf(stderr,"[Error]Daemon: Failed to open config file: %s.\n", ore_config);
			fprintf(stderr,"[Error]Daemon: Reason: %s.\n", strerror(errno));
			exit(EXIT_FAILURE);
		}
	}
	/* Read the configuration.
	 * Format:
	 * #comment\n
	 * derp=herp<whitespace>#optionalcomment\n
	 * All config names are lower case, is case
	 * sensitive.
	 * That's all folks.
	 */

	char *debug;
	/* String / config option pairing. */
	static void **options[9][2] = {
		{(void**) "log_path",      (void**) &ore_log         },
		{(void**) "java_path",     (void**) &ore_java        },
		{(void**) "java_jar_flag", (void**) &ore_jar_flag    },
		{(void**) "bukkit_path",   (void**) &ore_bukkit      },
		{(void**) "plugin_dir",    (void**) &ore_plugins     },
		{(void**) "persist_info",  (void**) &ore_persist     },
		{(void**) "daemonize",     (void**) &ore_tofork      },
		{(void**) "log_level",     (void**) &ore_debug_c     },
		{(void**) NULL,            (void**) NULL             }
	};

	char *line;
	char *key, *value;
	int ln, i;
	size_t in;
	int option_i;
	for (ln = 0; getline(&line, &in, config_file) >= 0; ln++) { 
		for (i = 0; isspace(line[i]) && line[i]; i++);
		if (line[i] == (char) '\n' || !line[i]) continue; /* empty line */
		if (line[i] == '#')  continue; /* It's a comment */
		if (!isalpha(line[i])) { /* Invalid character */
			fprintf(stderr, "[Daemon]Error: Invalid config. Line: %d:%d@%s\n",
			        ln, i, (ore_config[0] == '@')? "STDIN": ore_config);
			fprintf(stderr, "[Daemon]Error: Aborting...\n");
			exit(EXIT_FAILURE);
		}
		if (sscanf(line + i, "%a[^=]=%as", &key, &value) != 2) { /* If not key/value pair */
			fprintf(stderr, "[Daemon]Error: Invalid config. Line: %d:%d@%s\n",
			        ln, i, (ore_config[0] == '@')? "STDIN" : ore_config);
			fprintf(stderr, "[Daemon]Error: Aborting...\n");
			exit(EXIT_FAILURE);
		} /* I'll abbreviate that code eventually. */
		/* We now have a key / value pair, both malloc'd.
		 * Search for it in the options, and free what is not used.
		 */
		for (option_i = 0; strcmp((char*)options[option_i][0],key); option_i++);

		if (options[option_i][0])
			/* Match. */
			*options[option_i][1] = (void*) value;
		else {
			/* No match. */
			fprintf(stderr, "[Daemon]Error: Unknown configuration option: %d:%d@%s\n",
			        ln, i, (ore_config[0] == '@')? "STDIN" : ore_config);
			fprintf(stderr, "[Daemon]Error: Continuing.\n");
			free(value); /* If error, free value. Else, free'd by main later. */
		}
		free(key);
	}
	/* Debug level. Don't have generic number config loop, but meh. */
	if (ore_debug_c) {
		ore_debug = atoi(debug);
		free(debug);
	}
	return;
}

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

int main(int argc, char *argv[])
{
	/* List of configuration options: 
	 * Log path           "-l /path/to/logfile" | "-l -"
	 * Debug level        "-d [0-2]".
	 *     See daemon.h for details.
	 * Config file        "-c /path/to/config"
	 * Persistence string "-p ..."
	 *     See persist.h for details.
	 * Do not daemonize   "-i"
	 *
	 * The rest of the parameters should be easily
	 * configured via the persistence system.
	 * Note: The config is more for basic daemon configuration,
	 * whereas the persistence system is used for server, routing,
	 * etc. config. (This allows it to be more dynamic.)
	 */

	/* Read configuration options, read config (args override config)
	 * file or stream, continue.
	 */

	int opt; /* Option, or -1 if not available. */

	while ((opt = getopt(argc, argv, "il:d:c:p:")) != -1) {
		switch(opt) {
		case 'l':
			ore_log = strdup(optarg);
			break;
		case 'd':
			ore_debug = atoi(optarg); /* If error, 0. */
			break;
		case 'c':
			ore_config = strdup(optarg);
			break;
		case 'p':
			ore_persist = strdup(optarg);
			break;
		case 'i':
			ore_tofork = strdup(ORED_FALSE);
			break;
		default:
			fprintf(stderr, "Usage: "); /* Inefficient, but not worth the string manipulation. */
			fprintf(stderr, ORED_USAGE_FORMAT, argv[0]);
			fprintf(stderr, "\n");
			exit(EXIT_FAILURE);
		}
	}

	/* Somewhat large. Reads configuration if available (stdin, file, or none.) */
	if (ore_config)
		read_config();

	/* Sets unset config options to defaults. */
	/* Warning: Uses GNU extension. */
	ore_log =      (ore_log)?      : strdup(ORED_DEFAULT_LOG_PATH);
	ore_java =     (ore_java)?     : strdup(ORED_DEFAULT_JAVA_BIN);
	ore_jar_flag = (ore_jar_flag)? : strdup(JAVA_JAR_FLAG);
	ore_bukkit =   (ore_bukkit)?   : strdup(ORED_DEFAULT_BUKKIT_BIN);
	ore_plugins =  (ore_plugins)?  : strdup(ORED_DEFAULT_PLUGIN_DIR);
	ore_debug =    (ore_debug)?    : ORED_DEFAULT_DEBUG_LEVEL;
	ore_tofork =   (ore_tofork)?   : strdup(ORED_TRUE);

	/* By setting up the log before daemonizing, write permission
	 * failure on the log file isn't mysterious.
	 */
	ore_logfd = open(ore_log, O_WRONLY | O_APPEND | O_CREAT,
	                 S_IRWXU | S_IRGRP | S_IROTH);
	if (ore_logfd == -1) {
		fprintf(stderr, "[Error]Daemon: Failed to open log path: %s.\n",
		        ore_log);
		fprintf(stderr, "[Error]Daemon: Reason: %s.\n", strerror(errno));
		exit(EXIT_FAILURE);
	}

	/* All further log calls should go to ore_logfd */

	/* All strings save "0" and (nocase) "false" cause the daemon to fork. */
	if (strcasecmp(ore_tofork, ORED_FALSE) && strcasecmp(ore_tofork, "0"))
		if (!daemonize(ORED_DEFAULT_DIR)) /* Directory set by persistence system. Depricated. */
			{
				fprintf(stderr, "[Error]Daemon: Unable to fork: %s\n", strerror(errno));
				exit(EXIT_FAILURE);
			}

	umask(0); /* Never fails. */


	/* Start up SSL server, connect to other daemons (start fillling vhosts.) */
	/* Start up local unix socket, add local vhosts. */
	/* Start up built-in host managing client. */
	/* Wait for exit call, message callback modules to close down shop. */
	/* Once everybody's out, exit peacefully. */

	/* If fail, emulate wining teenager that doesn't care anymore. */
	close(ore_logfd);

	free(ore_config);
	free(ore_log);
	free(ore_java);
	free(ore_jar_flag);
	free(ore_bukkit);
	free(ore_plugins);
	free(ore_tofork);
	free(ore_persist);

	exit(EXIT_SUCCESS);
}
