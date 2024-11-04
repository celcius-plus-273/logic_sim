# from gate import gate
from fault import fault, FaultType
from typing import List

class wire:
    # member variables
    val = -1 # value on wire defaults to -1 for unassgined
    fault_list: List[fault] = None
    faults: List[bool] = [False, False]

    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        return f'Wire #{self.idx}: {self.val}'

    # method to compute if a fault in the set of faults will toggle the output bit
    def append_output_fault(self):
        # parse through the assigned faults and append to fault list
        if self.faults[FaultType.SA_0.value] and (self.val == 1):
            # instantiate new fault
            new_fault = fault(self.idx, 0)

            # append new fault to fault_list on input wire
            self.fault_list.append(new_fault)
            
        if self.faults[FaultType.SA_1.value] and (self.val == 0):
            # instantiate new s-a-1 fault
            new_fault = fault(self.idx, 1)

            # append fault to fault_list
            self.fault_list.append(new_fault)
