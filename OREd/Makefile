CC = cc
CFLAGS = -O3 -Wall

OBJS = main.o daemon.o console.o server.o client.o

build: $(OBJS) 
	$(CC) -o OREd $(OBJS)
        
clean:
	rm -f OREd $(OBJS)

daemon.o: src/daemon.c src/daemon.h
	$(CC) $(CFLAGS) -c src/daemon.c

console.o: src/console.c src/console.h
	$(CC) $(CFLAGS) -c src/console.c

server.o: src/server.c src/server.h
	$(CC) $(CFLAGS) -c src/server.c

client.o: src/client.c src/client.h
	$(CC) $(CFLAGS) -c src/client.c

main.o: src/main.c
	$(CC) $(CFLAGS) -c src/main.c

