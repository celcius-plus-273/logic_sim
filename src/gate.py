from enum import Enum

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
    in_a = None
    in_b = None
    out = None
    checked = False

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
    def check_inputs(self) -> bool:
        # for NOT and BUF there is only one input that needs to be checked
        if ((self.type == GateType.INV) or (self.type == GateType.BUF)):
            return (not self.checked) and (self.in_a.val > -1) # only check in_a
        else:
            # need to validate both in_a and in_b
            return (not self.checked) and ((self.in_a.val > -1) and (self.in_b.val > -1)) 
    
    def compute_out(self):
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
            print(f'Error computing output of gate: {self.idx}')
