from helper import parse_input_gate
from gate import gate, GateType

verbose = False
def parse_input(args, gate_list, wire_list, input_list, output_list):

    file_path = args['path']
    file_name = args['name']
    
    # # insntantiate a deque to hold all the gates
    # gates_list = deque()
    #
    # # instantiate deque to hold all the assigned wires
    # wires_list = deque() # list of unassigned wires
    #
    # # we will also keep a list of the input wires
    # input_list = deque() # so far we don't need it...
    #
    # # instantiate the output list   
    # output_list = deque()

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

                # get the wire index
                wire_idx = int(params[i].strip())

                # find the wire in the existing wire list
                for curr_wire in wire_list:
                    # find the correct wire index
                    if (curr_wire.idx == wire_idx):

                        # add this wire to input list
                        input_list.append(curr_wire)

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

                for tmp_wire in wire_list:
                    if (tmp_wire.idx == wire_idx):
                        output_list.append(tmp_wire)

        # parse gates
        elif (param_type == 'INV' or param_type == 'BUF'):
            parse_input_gate(gate_list, wire_list, params, i, num_inputs=1)
        else:
            parse_input_gate(gate_list, wire_list, params, i, num_inputs=2)    


# returns gate parity (0 or 1)
def check_gate_parity(curr_gate) -> int:
    if (curr_gate.type == GateType.INV):
        return 1
    elif (curr_gate.type == GateType.NAND):
        return 1
    elif (curr_gate.type == GateType.NOR):
        return 1
    else:
        return 0

