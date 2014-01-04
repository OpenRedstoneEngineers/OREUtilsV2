CC = g++
CFLAGS = -O3 -Wall

OBJS = main.o Console.o Server.o Client.o ProtoServer.o Manager.o Auth.o RSAKey.o Handler.o

build: $(OBJS) 
	$(CC) -o OREd $(OBJS)

clean:
	rm -f OREd $(OBJS)

Console.o: src/Console.cpp src/Console.hpp
	$(CC) $(CFLAGS) -c src/Console.cpp

Server.o: src/Server.cpp src/Server.hpp
	$(CC) $(CFLAGS) -c src/Server.cpp

Client.o: src/Client.cpp src/Client.hpp
	$(CC) $(CFLAGS) -c src/Client.cpp

ProtoServer.o: src/ProtoServer.cpp src/ProtoServer.hpp
	$(CC) $(CFLAGS) -c src/ProtoServer.cpp

Manager.o: src/Manager.cpp src/Manager.hpp
	$(CC) $(CFLAGS) -c src/Manager.cpp

Auth.o: src/Auth.cpp src/Auth.hpp
	$(CC) $(CFLAGS) -c src/Auth.cpp

RSAKey.o: src/RSAKey.cpp src/RSAKey.hpp
	$(CC) $(CFLAGS) -c src/RSAKey.cpp

Handler.o: src/Handler.cpp src/Handler.hpp
	$(CC) $(CFLAGS) -c src/Handler.cpp

main.o: src/main.cpp
	$(CC) $(CFLAGS) -c src/main.cpp

