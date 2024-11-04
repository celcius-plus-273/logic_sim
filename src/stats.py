# parse the faults_detected files based on cricuit name and output coverage
# input: faults_detected file
# input: total_num of faults
import argparse
from fault import fault

def main():
     # instantiate argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Specify name of input circuit file', required=True)

    # read passed in argument
    args = vars(parser.parse_args())
    file_name = args['name']

    f = open(f'results/{file_name}_faults_detected.txt', 'r')

    lines = f.readlines()

    total_faults = 0
    num_tests = 0
    fault_list = []

    for line in lines:
        params = line.split(' ')

        if (params[0].strip() == 'total'):
            total_faults = int(params[1].strip())
            num_tests += 1
        elif (params[0].strip() == 'fault'):
            # extract the wire idx
            wire_idx = int(params[1].strip())

            # get the stuck at value
            sa_val = int(params[4].strip())

            # create fault object
            fault_in = fault(wire_idx, sa_val)

            # now check if it's already in fault_list and append if not
            if (fault_in not in fault_list):
                fault_list.append(fault_in)
    f.close()

    # now compute the statistics
    faults_detected = len(fault_list)

    f = open(f'reports/{file_name}_faults_stats.rpt', 'w')
    f.write(f'Total Faults Detected: {faults_detected}\n')
    f.write(f'Total Number of Faults: {total_faults}\n')
    f.write(f'Number of Tests: {num_tests}\n')
    f.write(f'Coverage: {(float(faults_detected) / total_faults):04f}\n')

if __name__ == '__main__':
    main()
