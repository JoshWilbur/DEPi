# Compiler choice and flags
CC = gcc
CFLAGS = -Wall -Wextra -g -lncurses -O3 -fopenmp
LFLAGS = -fopenmp

# Source and header files
SRCS = conway_serial.c
OBJS = $(SRCS:.c=.o)

# Output executable name
EXEC = gol_serial

# Make process
all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) -o $@ $^ $(CFLAGS)
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(EXEC) $(OBJS)