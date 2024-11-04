# standard packages
import argparse
from collections import deque

# helper classes
from helper import *
from gate import *
from wire import *

def main():
    # instantiate argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Specify path of input circuit file', \
                        default='src/circuit', required=False)
    parser.add_argument('-n', '--name', help='Specify name of input circuit file', required=True)
    parser.add_argument('-t', '--test', help='Input test vector', required=True)

    parser.add_argument('-v', '--verbose', help='Enable debug output', default=False, required=False)

    # read passed in argument
    args = vars(parser.parse_args())
    file_path = args['path']
    file_name = args['name']
    
    # input test vector
    input_vector = args['test']
    vector_counter = 0;

    # debug print 
    verbose = args['verbose']

    # insntantiate a deque to hold all the gates
    gates_list = deque()

    # instantiate deque to hold all the assigned wires
    wires_list = deque() # list of unassigned wires

    # we will also keep a list of the input wires
    input_list = deque() # so far we don't need it...

    # instantiate the output list   
    output_list = deque()

    ### READ INPUT FILE ###
    circuit_file_path = f'{file_path}/{file_name}.txt'
    file_reader = open(circuit_file_path, 'r')
    netlist = file_reader.readlines()
    
    # parse the input netlist
    for i, net in enumerate(netlist):
        params = net.strip().split(' ')

        # first element will always be the type of the parameter
        param_type = params[0].strip()

        # parse input pin definitions
        if (param_type == 'INPUT'):
            if verbose:
                print('Parsing input line...')
            
            # assign the values and pop from unassgined wires list
            for i in range(1, len(params) - 1):
                # get rid of blank spaces... 
                if params[i].strip() == '':
                    continue

                # assign the appropriate value and pop it off the list
                wire_idx = int(params[i].strip())

                # the value from inputs comes from the input test vector
                # NOTE: we should never run into an index out of bounds issue
                new_val = int(input_vector[vector_counter])
                # by using a separate counter we can avoid having to synchronize both indexes
                vector_counter += 1

                # now call the assignment function
                assign_input_values(wire_idx, new_val, wires_list, input_list)

        # parse output pins
        elif (param_type == 'OUTPUT'):
            # assign the circuit outputs
            if verbose:
                print('Parsing output line...')
            
            # outputs pins are indexes 1 to n-2
            for i in range(1, len(params) - 1):
                # some spaces are left blank...
                if params[i].strip() == '':
                    continue
                
                # if a non-blank space is found then append to list!
                wire_idx = int(params[i].strip())

                for tmp_wire in wires_list:
                    if (tmp_wire.idx == wire_idx):
                        output_list.append(tmp_wire)

        # parse gates
        elif (param_type == 'INV' or param_type == 'BUF'):
            parse_input_gate(gates_list, wires_list, params, i, num_inputs=1)
        else:
            parse_input_gate(gates_list, wires_list, params, i, num_inputs=2)    

    gates_ready = deque()
    for gate_x in gates_list:
        # print(f'checking gate: {gate_x}')
        if (gate_x.check_input_logic()):
            # print(f'appending it to the list!')
            gate_x.logic_done = True
            gates_ready.append(gate_x)
    
    while True:
        if (len(gates_ready) <= 0):
            break

        while (len(gates_ready) > 0):
            # pop all available gates
            curr_gate = gates_ready.popleft()

            # compute the new value 
            curr_gate.compute_logic() # this changes the output wire's val

        # find new gates that are ready now :)
        for gate_x in gates_list:
            # print(f'checking gate: {gate_x}')
            if (gate_x.check_input_logic()):
                # print(f'appending it to the list!')
                gate_x.logic_done = True
                gates_ready.append(gate_x)   

    # now format the output using the assigned output wires 
    output_vector = ''
    for output_wire in output_list:
        output_vector = output_vector + f'{output_wire.val}'

    # print outputs once all wires are assigned 
    print(f'Inputs: {input_vector}')
    print(f'Output: {output_vector}')

if __name__ == '__main__':
    main()
