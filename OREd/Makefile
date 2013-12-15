CC = cc
CFLAGS = -O3

OBJS = main.o

build: $(OBJS) 
	$(CC) -o OREd $(OBJS)
        
clean:
	rm -f OREd $(OBJS)

main.o: src/main.c
	$(CC) $(CFLAGS) -c src/main.c

