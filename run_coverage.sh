#!/bin/bash

# specify output file
output_file=results/coverage.log

# all circuits
circuits="
s27  
s298f_2
s344f_2
s349f_2"

input_lengths=(
    '7'
    '17'
    '24'
    '24'
)

# read -p "Number of Random Tests: " iterations
: ${iterations:=100}

echo "Running ${iterations} iterations"

# RUN CLEAN
make clean

# FIRST NEED TO GENERATE RANDOMIZE TEST VECTORS
i=0
echo "Generating Random Tests..."
for val in ${circuits}; do

    echo "--------------------------------------------" >> ${output_file}
    echo "GENERATING RANDOM INPUT VECTORS FOR CIRCUIT ${val}" >> ${output_file}
    echo "--------------------------------------------" >> ${output_file}
    
    make random CIRCUIT_NAME=${val} INPUT_LENGTH=${input_lengths[$i]} NUM_RAND_TESTS=${iterations} >> ${output_file}
    
    i=$((i+1))

    echo "--------------------------------------------" >> ${output_file}
    echo "TEST GENERATION FOR ${val} DONE" >> ${output_file}
    echo "--------------------------------------------" >> ${output_file}
done

# RUN FAULT SIMULATION
echo "Fault Simulation..."
for val in ${circuits}; do 
    echo "-----------------------------------" >> ${output_file}
    echo "SIMULATION FOR CIRCUIT ${val}" >> ${output_file}
    echo "-----------------------------------" >> ${output_file}
    
    filename="results/${val}_input_vector.txt"

    while read line; do 

        make fault CIRCUIT_NAME=${val} TEST_VECTOR=${line} >> ${output_file}

    done < $filename

    echo "-----------------------------------" >> ${output_file}
    echo "SIMULATION FOR CIRCUIT ${val}" DONE  >> ${output_file}
    echo "-----------------------------------" >> ${output_file}
done

# RUN STATS FOR EACH CIRCUIT
echo "Runing Statistics..."
for val in ${circuits}; do

    echo "--------------------------------------------" >> ${output_file}
    echo "COMPUTING STATISTICS FOR CIRCUIT ${val}" >> ${output_file}
    echo "--------------------------------------------" >> ${output_file}
    
    make stats CIRCUIT_NAME=${val} >> ${output_file}

    echo "--------------------------------------------" >> ${output_file}
    echo "STATISTICS FOR CIRCUIT ${val}" DONE >> ${output_file}
    echo "--------------------------------------------" >> ${output_file}
done
