CC=/usr/bin/g++

CFLAGS=-std=c++11 -Wall


single_all_to_all: single_all_to_all.cpp type.hpp
	$(CC) $(CFLAGS) single_all_to_all.cpp -o single_all_to_all

clean:
	rm -rf *.o single_all_to_all


