# imports
from collections import deque
from gate import *
from wire import *

### HELPER METHODS ###

# assigns wire in unassigned wire list and pops it from the list 
def assign_wire(wire_idx: int, new_val: int, wires_list: deque):
    # iterate through list of wires
    for wire in wires_list:
        # find the correct wire index
        if (wire.idx == wire_idx):
            # assign the corresponding value
            wire.val = new_val

            # now pop this wire off the list
            wires_list.remove(wire)
            
            # done
            return True

    # this should only happen if there's unconnected/floating wires
    print(f'Wire {wire_idx} is not in list...')
    return False # think of it as an error code 

# parses the gates form the input netlist
def parse_input_gate(gates_list: deque, wires_list: deque, params, i: int, num_inputs: int):
    param_type = params[0].strip()
    if (num_inputs == 1):
        new_gate = gate(i, GateType[param_type])
        in_a = int(params[1].strip())
        out = int(params[2].strip())

        # check if wire already exists
        for wire_x in wires_list:
            # assign a reference of it to the new_gate input
            if (wire_x.idx == in_a):
                new_gate.in_a = wire_x
                # wire_x.load.append(new_gate) # attach a reference of this gate :)
                # print(f'{new_gate.type.name} #{i} has wire {wire_x.idx} as an input')
                
            # assign a reference of it to the new_gate output
            if (wire_x.idx == out):
                new_gate.out = wire_x
                # wire_x.drive = new_gate # attach a reference of this gate :)
                # print(f'{new_gate.type.name} #{i} has wire {wire_x.idx} as an output')

        # if it doesn't exist, create it and assign it
        if (new_gate.in_a == None):
            new_wire = wire(in_a) # crate new wire
            new_gate.in_a = new_wire # update new_gate
            # new_wire.load.append(new_gate) # attach a reference of this gate :)
            # print(f'{new_gate.type.name} #{i} has wire {new_wire.idx} as an input')
            wires_list.append(new_wire)
    
        if (new_gate.out == None):
            new_wire = wire(out)
            new_gate.out = new_wire
            # new_wire.drive = new_gate
            # print(f'{new_gate.type.name} #{i} has wire {new_wire.idx} as an output')
            wires_list.append(new_wire)

        # add gate to list of gates
        gates_list.append(new_gate)
    
    elif (num_inputs == 2):
        # these are two input gates 
        new_gate = gate(i, GateType[param_type])
        in_a = int(params[1].strip())
        in_b = int(params[2].strip())
        out = int(params[3].strip())

        # check if wire already exists
        for wire_x in wires_list:
            # assign a reference of it to the new_gate input
            if (wire_x.idx == in_a):
                new_gate.in_a = wire_x
                # wire_x.load.append(new_gate)
                # print(f'{new_gate.type.name} #{i} has wire {wire_x.idx} as an input')

            if (wire_x.idx == in_b):
                new_gate.in_b = wire_x
                # wire_x.load.append(new_gate)
                # print(f'{new_gate.type.name} #{i} has wire {wire_x.idx} as an input')

            # assign a reference of it to the new_gate output
            if (wire_x.idx == out):
                new_gate.out = wire_x
                # wire_x.drive = new_gate
                # print(f'{new_gate.type.name} #{i} has wire {wire_x.idx} as an output')

        # if it doesn't exist, create it and assign it
        if (new_gate.in_a == None):
            new_wire = wire(in_a)
            new_gate.in_a = new_wire
            # new_wire.load.append(new_gate)
            wires_list.append(new_wire)
            # print(f'{new_gate.type.name} #{i} has wire {new_wire.idx} as an input')

        if (new_gate.in_b == None):
            new_wire = wire(in_b)
            new_gate.in_b = new_wire
            # new_wire.load.append(new_gate)
            wires_list.append(new_wire)
            # print(f'{new_gate.type.name} #{i} has wire {new_wire.idx} as an input')
   
        if (new_gate.out == None):
            new_wire = wire(out)
            new_gate.out = new_wire
            # new_wire.drive = new_gate
            wires_list.append(new_wire)
            # print(f'{new_gate.type.name} #{i} has wire {new_wire.idx} as an output')

        # add gate to list of gates
        gates_list.append(new_gate)

