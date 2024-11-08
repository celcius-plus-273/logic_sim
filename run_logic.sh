#!/bin/bash

# simulation type
sim_type=logic

# specify output file
output_file=results/${sim_type}_result.txt

circuits="
s27  
s298f_2
s344f_2
s349f_2"

test_vectors=(
'1110101'
'0001010'
'1010101'
'0110111'
'1010001'
'10101010101010101'
'01011110000000111'
'11111000001111000'
'11100001110001100'
'01111011110000000'
'101010101010101011111111'
'010111100000001110000000'
'111110000011110001111111'
'111000011100011000000000'
'011110111100000001111111'
'101010101010101011111111'
'010111100000001110000000'
'111110000011110001111111'
'111000011100011000000000'
'011110111100000001111111'
)

make clean

i=0

for val in ${circuits}; do 
    echo "-----------------------------------" >> ${output_file}
    echo "SIMULATION FOR CIRCUIT ${val}" >> ${output_file}
    echo "-----------------------------------" >> ${output_file}
    
    echo "--------" >> ${output_file}
    echo "TEST 1:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$i]} >> ${output_file}
    
    echo "--------" >> ${output_file}
    echo "TEST 2:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$((i + 1))]} >> ${output_file}
    
    echo "--------" >> ${output_file}
    echo "TEST 3:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$((i + 2))]} >> ${output_file}

    echo "--------" >> ${output_file}
    echo "TEST 4:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$((i + 3))]} >> ${output_file}

    echo "--------" >> ${output_file}
    echo "TEST 5:" >> ${output_file}
    echo "--------" >> ${output_file}
    make ${sim_type} CIRCUIT_NAME=${val} TEST_VECTOR=${test_vectors[$((i + 4))]} >> ${output_file}

    i=$((i+5))
done

echo "simulation Finished!"
echo "Results have been stored in ${output_file}"
