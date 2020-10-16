#!/usr/bin/env python3

OP = {
        ' == ' : ['==', ' = ', ' eq ', ' -eq '],
        ' > ' : [' > ', ' gt ', ' -gt '],
        ' >= ' : ['>=', ' ge ', ' -ge '],
        ' < ' : [' < ', ' lt ', ' -lt '],
        ' <= ' : ['<=', ' le ', ' -le '],
        ' and ' : ['&&', ' & ', ' and '],
        ' or ' : ['||', ' | ', ' or '],
        }
VALID_OP = sum(OP.values(),[])
STD_OP = list(OP.keys())
RANGE_OP = [STD_OP[1], STD_OP[2], STD_OP[3], STD_OP[4]]

def clear_double_spaces(input_string : str) -> str:
    input_string = input_string.strip().rstrip()
    while '  ' in input_string:
        input_string = input_string.replace('  ',' ')
    return input_string

def translate(input_string : str) -> str:
    for translated_op in STD_OP:
        op_list = OP[translated_op]
        for op in op_list:
            input_string = input_string.replace(op, translated_op)
    return input_string

def ingest(input_string : str) -> str:
    return clear_double_spaces(translate(clear_double_spaces(input_string)))

def convert_ranges(input_string : str) -> list:
    numop = sum(input_string.count(op) for op in RANGE_OP)
    if numop == 2:
        l = input_string.split(' ')
        l.insert(2, l[2])
        return [' '.join(l[0:3]), ' '.join(l[3:])]
    else:
        return [input_string.strip(' ').rstrip(' ')]

class inequality_engine:
    def __init__(self, input_string):
        input_string = ingest(input_string)
        or_groups = input_string.split(';')
        self.filters = []
        for og in or_groups:
            conditions = og.split(',')
            converted = []
            for cond in conditions:
                converted.extend(convert_ranges(cond))
            self.filters.append(converted)
        
        if not self.filters or self.filters == [['']]:
            raise ValueError("No filter defined. Aborting.")

    def run(self):
        return any(map(lambda and_group: all(map(lambda expr: eval(expr), and_group)), self.filters))

import sys

if __name__ == "__main__":
    string = ''.join(sys.argv[1:])
    ie = inequality_engine(string)
    print(ie.filters)
    print(ie.run())