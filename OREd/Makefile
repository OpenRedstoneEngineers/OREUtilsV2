CC = gcc
CFLAGS = -Wall -g
LIBS= -pthread
OBJS = bin/main.o bin/packet.o bin/routing.o

build: bin/ $(OBJS) 
	$(CC) $(OBJS) $(LIBS) -o OREd

clean:
	rm -f OREd $(OBJS)

bin/:
	mkdir bin
	@echo "Making directory bin/."

bin/main.o: src/main.c src/daemon.h src/routing.h
	$(CC) $(CFLAGS) -c $< $(LIBS) -o $@

bin/packet.o: src/packet.c src/packet.h src/routing.h
	$(CC) $(CFLAGS) -c $< $(LIBS) -o $@

bin/routing.o: src/routing.c src/routing.h src/daemon.h
	$(CC) $(CFLAGS) -c $< $(LIBS) -o $@
