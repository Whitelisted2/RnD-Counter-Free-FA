#!/bin/bash



g++ getData.cpp -o getData.o;
./getData.o $1;
rm -rf getData.o

./bin/gap.sh -r -b -q << EOI

Read("sandbox/loadPackages.g");
Read("sandbox/inputAutomaton.g");
Read("sandbox/autoOps.g");

EOI