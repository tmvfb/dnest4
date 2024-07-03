CFLAGS = -std=c++14 -O3 -DNDEBUG -Wall -Wextra -pedantic -I/usr/local/Cellar/gsl/2.8/include -I/Users/igorkvachenok/exp/dnest4/DNest4/code -I./eigen/
LIBS = -L/usr/local/Cellar/gsl/2.8/lib -lgsl -lgslcblas -L/Users/igorkvachenok/exp/dnest4/DNest4/code -ldnest4

default:
	g++ $(CFLAGS) -c *.cpp
	g++ -pthread -o main *.o $(LIBS)
	rm -f *.o

