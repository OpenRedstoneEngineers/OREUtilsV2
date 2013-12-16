CC = cc
CFLAGS = -O3 -Wall

OBJS = main.o daemon.o console.o

build: $(OBJS) 
	$(CC) -o OREd $(OBJS)
        
clean:
	rm -f OREd $(OBJS)

daemon.o: src/daemon.c src/daemon.h
	$(CC) $(CFLAGS) -c src/daemon.c

console.o: src/console.c src/console.h
	$(CC) $(CFLAGS) -c src/console.c

main.o: src/main.c
	$(CC) $(CFLAGS) -c src/main.c

