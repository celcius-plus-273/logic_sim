LOGIC_SRC = src/logic_sim.py
FAULT_SRC = src/fault_sim.py
STAT_SRC = src/stats.py
RANDOM_SRC = src/generate_random.py
CIRCUIT_NAME = s298f_2

# change this based on input test
TEST_VECTOR = 10101010101010101

INPUT_LENGTH = 7

NUM_RAND_TESTS = 100

VERBOSITY = False

logic:
	python3 ${LOGIC_SRC} -n ${CIRCUIT_NAME} -t ${TEST_VECTOR}

fault:
	python3 ${FAULT_SRC} -n ${CIRCUIT_NAME} -t ${TEST_VECTOR}

stats:
	python3 ${STAT_SRC} -n ${CIRCUIT_NAME}

random:
	python3 ${RANDOM_SRC} -n ${CIRCUIT_NAME} -l ${INPUT_LENGTH} -i ${NUM_RAND_TESTS}

clean:
	rm -rf src/__pycache__
	rm -rf out.txt
	rm -rf results/*
	
