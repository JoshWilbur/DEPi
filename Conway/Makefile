# Compiler choice and flags
CC = gcc
CFLAGS = -Wall -Wextra -g

# Source and header files
SRCS = conway_gol.c
OBJS = $(SRCS:.c=.o)

# Output executable name
EXEC = gol

# Make process
all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) -o $@ $^ $(CFLAGS)
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(EXEC) $(OBJS)