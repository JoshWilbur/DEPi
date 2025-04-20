# Compiler choice and flags
CC = gcc
CFLAGS = -Wall -Wextra -g -lncurses -O3 -fopenmp -I/${PAPI_DIR}/include -L/${PAPI_DIR}/lib -lpapi

# Source and header files
SRCS_SERIAL = conway_serial.c
SRCS_SERIAL_PAPI = conway_serial_PAPI.c
SRCS_OMP = conway_omp.c

OBJS_SERIAL = $(SRCS_SERIAL:.c=.o)
OBJS_SERIAL_PAPI = $(SRCS_SERIAL_PAPI:.c=.o)
OBJS_OMP = $(SRCS_OMP:.c=.o)

# Output executable names
EXEC_SERIAL = gol_serial
EXEC_SERIAL_PAPI = gol_serial_PAPI
EXEC_OMP = gol_omp

# Make process
all: $(EXEC_SERIAL) $(EXEC_SERIAL_PAPI) $(EXEC_OMP)

# Build serial binary (non-papi)
$(EXEC_SERIAL): $(OBJS_SERIAL)
	$(CC) -o $@ $^ $(CFLAGS)

# Build serial binary (with papi)
$(EXEC_SERIAL_PAPI): $(OBJS_SERIAL_PAPI)
	$(CC) -o $@ $^ $(CFLAGS)

# Build OpenMP binary
$(EXEC_OMP): $(OBJS_OMP)
	$(CC) -o $@ $^ $(CFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(EXEC_SERIAL) $(EXEC_SERIAL_PAPI) $(EXEC_OMP) $(OBJS_SERIAL) $(OBJS_SERIAL_PAPI) $(OBJS_OMP)