#!/bin/bash

# first clean off previous results
make wipe

for i in {5..50}; do
    iterations=${i} ./run_coverage.sh
done
