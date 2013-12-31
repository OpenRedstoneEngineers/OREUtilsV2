CC = g++
CFLAGS = -O3 -Wall

OBJS = main.o daemon.o Console.o Server.o Client.o ProtoServer.o

build: $(OBJS) 
	$(CC) -o OREd $(OBJS)
        
clean:
	rm -f OREd $(OBJS)

daemon.o: src/daemon.c src/daemon.h
	$(CC) $(CFLAGS) -c src/daemon.c

Console.o: src/Console.cpp src/Console.hpp
	$(CC) $(CFLAGS) -c src/Console.cpp

Server.o: src/Server.cpp src/Server.hpp
	$(CC) $(CFLAGS) -c src/Server.cpp

Client.o: src/Client.cpp src/Client.hpp
	$(CC) $(CFLAGS) -c src/Client.cpp

ProtoServer.o: src/ProtoServer.cpp src/ProtoServer.hpp
	$(CC) $(CFLAGS) -c src/ProtoServer.cpp

main.o: src/main.cpp
	$(CC) $(CFLAGS) -c src/main.cpp

