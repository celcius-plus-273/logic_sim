import argparse
from collections import deque
from podem_util import parse_input, check_gate_parity
from gate import gate
from wire import wire
from fault import fault

### GLOBAL LISTS ###
wire_list = deque()
gate_list = deque()
input_list = deque()
output_list = deque()
d_frontier = deque()

### Objective ###
objective_fault = None
objective_wire = None
objective_val = None

# Backtrace function
#   k = output wire of a gate
#   v_k = value to be assigned on k
def backtrace(k: wire, v_k: int) -> (wire, int):
    # backtrace returns PI and value to be assigned (j, v_j)
    v = v_k # copy value of v_k
    while (k not in input_list):
        # find gate that contains k as the output
        gate_k = k.drive

        # get the inversion parity of that gate
        i_parity = check_gate_parity(gate_k)
        v = v ^ i_parity # v xor i

        # select unassigned input of gate_k
        k = gate_k.get_input_x()
    
    return (k, v)

def objective() -> (wire, int):
    # return objective as objective :)
    if (objective_wire.val == -1):
        return (objective_wire, objective_val)

    # pop gate from d_frontier
    curr_d_gate = d_frontier.popleft()
    
    # get controlling value
    c = curr_d_gate.get_controlling_val()
    
    # select input with value -1
    j = curr_d_gate.get_input_x()

    # objective is to assign non-controlling value to other gate inputs
    return (j, not(c))

def imply():
    pass

def podem():
    pass

def main():
    # instantiate argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Specify path of input circuit file', \
                        default='src/circuit', required=False)
    parser.add_argument('-n', '--name', help='Specify name of input circuit file', required=True)
    parser.add_argument('-w', '--wire', help='Stuck-at-fault wire', required=True)

    parser.add_argument('-v', '--value', help='Stuck-at-fault value', required=True)

    # read passed in argument
    args = vars(parser.parse_args())

    # parse input netlist and populate gate, wire, input, and output lists
    parse_input(args, gate_list, wire_list, input_list, output_list)

    # objective
    objective_wire_idx = int(args['wire'])
    objective_sa_val = int(args['value'])
    objective_fault = fault(objective_wire_idx, objective_sa_val)

    # initial objective is exciting objective fault
    objective_val = not(objective_fault.sa_val)
    for curr_wire in wire_list:
        if curr_wire.idx == objective_fault.wire_idx:
            objective_wire = curr_wire
