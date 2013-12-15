#include <sys/types.h>
#include <sys/stat.h>

#include <fcntl.h>
#include <unistd.h>
#include <syslog.h>

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

FILE* logFile;

void SignalHandler(int signal)
{
	switch (signal)
	{
		case SIGTERM:
		{
			fprintf(logFile, "Received SIGTERM. Terminating...\n");

			break;
		}
	}
}

void Start(void)
{
	FILE* server = popen("/usr/bin/java -jar craftbukkit.jar", "r");

	if (server == NULL)
	{
		fprintf(logFile, "Could not start craftbukkit.\n");

		fclose(logFile);
		exit(EXIT_FAILURE);
	}

	char buffer[256];

	while (fgets(buffer, sizeof(buffer) - 1, server) != NULL)
	{
		printf("[MC] %s", buffer);
	}

	pclose(server);

	fprintf(logFile, "Exiting.\n");

	fclose(logFile);

	exit(EXIT_SUCCESS);
}

void Daemonize(void)
{
	pid_t pid = fork();

	if (pid < 0)
	{
		printf("Fork unsuccesful.\n");

		exit(EXIT_FAILURE);
	}

	if (pid > 0)
	{
		printf("Fork succesful. [PID: %i]\n", pid);

		exit(EXIT_SUCCESS);
	}

	umask(0);

	logFile = fopen("OREd.log", "w");

	if (logFile == NULL)
	{
		exit(EXIT_FAILURE);
	}

	pid_t sid = setsid();

	if (sid < 0)
	{
		fprintf(logFile, "Could not create a new session.\n");

		fclose(logFile);
		exit(EXIT_FAILURE);
	}

	if (chdir("/") < 0)
	{
		fprintf(logFile, "Could not change working directory.\n");

		fclose(logFile);
		exit(EXIT_FAILURE);
	}

	close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);

	signal(SIGTERM, SignalHandler);

	Start();
}

int main()
{
	Daemonize();
}
