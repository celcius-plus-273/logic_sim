SRC_FILES = src/circuit_sim.py
CIRCUIT_NAME = s27

# change this based on input test
TEST_VECTOR = 0001010

VERBOSITY = False

sim:
	python3 ${SRC_FILES} -n ${CIRCUIT_NAME} -t ${TEST_VECTOR}

clean:
	rm -rf src/__pycache__
	rm -rf out.txt
	rm -rf results.txt
	
