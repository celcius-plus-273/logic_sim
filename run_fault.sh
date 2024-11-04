#!/bin/bash

# simulation type
sim_type=fault

# specify output file
output_file=results/${sim_type}_result.txt

circuits="
s27  
s298f_2
s344f_2
s349f_2"

test_vectors=(
    '1101101'
    '0101001'
    '10101011110010101'
    '11101110101110111'
    '101010101010111101111111'
    '111010111010101010001100'
    '101000000010101011111111'
    '111111101010101010001111'
)

make clean

i=0

for val in ${circuits}; do 
    echo "-----------------------------------" >> ${output_file}
    echo "${sim_type} SIMULATION FOR CIRCUIT ${val}" >> ${output_file}
    echo "-----------------------------------" >> ${output_file}
    
    echo "--------" >> ${output_file}
    echo "TEST 1:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$i]} >> ${output_file}
    
    echo "--------" >> ${output_file}
    echo "TEST 2:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$((i + 1))]} >> ${output_file}
    
    i=$((i+2))
done

echo "simulation Finished!"
echo "Results have been stored in ${output_file}"
