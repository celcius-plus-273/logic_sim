import argparse
import random

def main():
     # instantiate argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Specify name of input circuit', required=True)
    parser.add_argument('-l', '--length', help='Specify length of circuit input vector', required=True)
    parser.add_argument('-i', '--iter', help='Specify number of random test cases to be generated', required=True)

    # read passed in argument
    args = vars(parser.parse_args())
    circuit_name = args['name']
    vector_length = args['length']
    num_vectors = args['iter']

    # max value
    max_value = (2 ** (int(vector_length))) - 1

    # generate i number of test vectors and write them onto an input vector file
    f = open(f'results/{circuit_name}_input_vector.txt', 'w')
    for i in range(int(num_vectors)):
        rand_vec = random.randrange(0, max_value)
        write_out = str(bin(rand_vec)[2:]).zfill(int(vector_length))
        f.write(f'{write_out}\n')
        print(write_out)

if __name__ == '__main__':
    main()
