from fault import fault
from typing import List

def compute_intersect(a_list: List[fault], b_list: List[fault]) -> List[fault]:
    out_list = []

    # find all entries that are equal and add them to output list
    for fault_a in a_list:
        for fault_b in b_list:
            if (fault_a == fault_b):
                out_list.append(fault_a)

    return out_list

def compute_union(a_list: List[fault], b_list: List[fault]) -> List[fault]:
    # copy a_list
    out_list = a_list.copy()

    # check for each fault_b in b_list if it's already in out_list
    for fault_b in b_list:
        if (fault_b not in out_list):
            # append if not in out already
            out_list.append(fault_b)

    return out_list
