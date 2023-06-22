CC = g++
TARGET = output_generator
OBJS = solve_2opt.o output_generator.o common.o

$(TARGET): $(OBJS)
	$(CC) -Wall -o $@ $^ -lm

clean:
	rm *.o *~