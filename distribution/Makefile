all: distribution

distribution.o: fair_distribution.cpp fair_distribution.h
	g++ fair_distribution.cpp -c -o distribution.o

distribution: distribution.o
	g++ main.cpp distribution.o -o distribution

clean:
	rm -rf ./distribution *.o