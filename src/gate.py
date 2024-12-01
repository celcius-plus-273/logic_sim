from enum import Enum
from wire import wire
from list_helper import compute_union, compute_intersect

# enumeration class for gate types
class GateType(Enum):
    INV = 0
    AND = 1
    OR = 2
    NAND = 3
    NOR = 4
    BUF = 5

class gate:
    # some member variables
    in_a: wire = None
    in_b: wire = None
    out: wire = None
    logic_done: bool = False
    fault_done: bool = False

    def __init__(self, idx, type):
        self.idx = idx
        self.type = type

    def __str__(self):
        return f'{self.type.name} Gate: #{self.idx} \
                \n    in_a: {self.in_a} \
                \n    in_b: {self.in_b} \
                \n    out: {self.out}'

    # method to check whether the inputs of a gate are ready
    # this will only return true if the output hasn't been already computed
    def check_input_logic(self) -> bool:
        # for NOT and BUF there is only one input that needs to be checked
        if ((self.type == GateType.INV) or (self.type == GateType.BUF)):
            return (not self.logic_done) and (self.in_a.val > -1) # only check in_a
        else:
            # need to validate both in_a and in_b
            return (not self.logic_done) and ((self.in_a.val > -1) and (self.in_b.val > -1)) 

    def check_input_fault(self) -> bool:
        if ((self.type == GateType.INV) or (self.type == GateType.BUF)):
            return (not self.fault_done) and (self.in_a.fault_list is not None) # only check in_a
        else:
            # need to validate both in_a and in_b
            return (not self.fault_done) and \
                ((self.in_a.fault_list is not None) and (self.in_b.fault_list is not None)) 

    def get_input_x(self) -> wire:
        # for NOT and BUF there is only one input that needs to be checked
        if ((self.type == GateType.INV) or (self.type == GateType.BUF)):
            if (self.in_a.val == -1):
                return self.in_a
        else:
            if (self.in_a.val == -1):
                return self.in_a
            elif (self.in_b.val == -1):
                return self.in_b
        print(f'[PANIC]: {self} has no unassigned input')

    def get_controlling_val(self) -> int:
        if (self.type == GateType.NAND) or (self.type == GateType.AND):
            return 0
        elif (self.type == GateType.OR) or (self.type == GateType.NOR):
            return 1
        else:
            print(f'[PANIC]: {self} is in D-frontier and has no controlling value...')

    def compute_logic(self):
        if (self.type == GateType.INV):
            self.out.val = int(not self.in_a.val)
        elif (self.type == GateType.AND):
            self.out.val = self.in_a.val & self.in_b.val
        elif (self.type == GateType.OR):
            self.out.val = self.in_a.val | self.in_b.val
        elif (self.type == GateType.NAND):
            self.out.val = int(not(self.in_a.val & self.in_b.val))
        elif (self.type == GateType.NOR):
            self.out.val = int(not(self.in_a.val | self.in_b.val))
        elif (self.type == GateType.BUF):
            self.out.val = self.in_a.val
        else:
            print(f'Error computing logic output of gate: {self.idx}')

    # propagates the fault list accordingly
    def compute_fault(self):
        ################
        ### INVERTER ###
        ################
        if (self.type == GateType.INV):
            # get reference to output wire
            out_wire = self.out

            # fault_list = prev_list + out toggle
            out_wire.fault_list = self.in_a.fault_list.copy()

            # check val of output and append fault if it toggles output
            out_wire.append_output_fault()

        ##############
        ### BUFFER ###
        ##############
        elif (self.type == GateType.BUF):
            # get reference to output wire
            out_wire = self.out

            # fault_list = prev_list + out toggle
            out_wire.fault_list = self.in_a.fault_list.copy()

            # check val of output and append fault if it toggles output
            out_wire.append_output_fault()

        #######################
        ### AND & NAND GATE ###
        #######################
        elif (self.type == GateType.AND) or (self.type == GateType.NAND):
            # reference to output wire
            out_wire = self.out
            wire_a = self.in_a
            wire_b = self.in_b

            # controlling value in AND = 0 (c = o)
            if (wire_a.val == 0) and (wire_b.val == 0):
                # get intersection between both
                out_wire.fault_list = compute_intersect(wire_a.fault_list, wire_b.fault_list)

            elif (wire_a.val == 0) and (wire_b.val == 1):
                # output list is just a list
                out_wire.fault_list = wire_a.fault_list.copy()

            elif (wire_a.val == 1) and (wire_b.val == 0):
                # output list is just b_list
                out_wire.fault_list = wire_b.fault_list.copy()

            elif (wire_a.val == 1) and (wire_b.val == 1):
                # union of the two
                out_wire.fault_list = compute_union(wire_a.fault_list, wire_b.fault_list)

            else:
                print(f'Invalid wire value found in {self.type} gate when propagating the fault list')

            # check bit flipping at output wire
            out_wire.append_output_fault()

        #####################
        ### OR & NOR GATE ###
        #####################
        elif (self.type == GateType.OR) or (self.type == GateType.NOR):
            # reference to output wire
            out_wire = self.out
            wire_a = self.in_a
            wire_b = self.in_b

            # controlling value in OR = 1 (c = 1)
            if (wire_a.val == 0) and (wire_b.val == 0):
                # get intersection between both
                out_wire.fault_list = compute_union(wire_a.fault_list, wire_b.fault_list)

            elif (wire_a.val == 0) and (wire_b.val == 1):
                # output list is just a list
                out_wire.fault_list = wire_b.fault_list.copy()

            elif (wire_a.val == 1) and (wire_b.val == 0):
                # output list is just b_list
                out_wire.fault_list = wire_a.fault_list.copy()

            elif (wire_a.val == 1) and (wire_b.val == 1):
                # union of the two
                out_wire.fault_list = compute_intersect(wire_a.fault_list, wire_b.fault_list)

            else:
                print(f'Invalid wire value found in {self.type} gate when propagating the fault list')

            # check bit flipping at output wire
            out_wire.append_output_fault()

        else:
            print(f'Error computing fault output of gate: {self.idx}')
