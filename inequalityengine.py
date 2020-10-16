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
VALID_OP_NOSPACE = [ op.replace(' ','') for op in VALID_OP]
STD_OP = list(OP.keys())
RANGE_OP = [STD_OP[1], STD_OP[2], STD_OP[3], STD_OP[4]]
KEYWORDS = VALID_OP_NOSPACE+["True", "False"]

INVERTED_STD_OP = { op : op for op in STD_OP}
INVERTED_STD_OP[' > '] = ' < '
INVERTED_STD_OP[' >= '] = ' <= '
INVERTED_STD_OP[' < '] = ' > '
INVERTED_STD_OP[' <= '] = ' >= '

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

def get_num_op(input_string : str) -> list:
    return sum(input_string.count(op) for op in RANGE_OP)

def convert_ranges(input_string : str) -> list:
    if get_num_op(input_string) == 2:
        l = input_string.split(' ')
        l.insert(2, l[2])
        return [' '.join(l[0:3]), ' '.join(l[3:])]
    else:
        return [input_string.strip(' ').rstrip(' ')]

def expand_metadata(input_string : str, model : str = "models.DataIdentifier.") -> list:
    l = input_string.rstrip(' ').strip(' ').split(' ')
    for i,p in enumerate(l):
        try:
            float(eval(p))
        except:
            if not p in KEYWORDS: # Will be "if hasattr(models.DataIdentifier, p) and not p in VALID_OP_NOSPACE:"
                l[i] = model + p
    return ' '.join(l)

def get_dict(input_string : str, model : str = "models.DataIdentifier.") -> list:
    l = input_string.split(' ')
    if len(l) == 3:
        if model in l[0]:
            return {'model' : model.rstrip('.'), 'field' : l[0].replace(model,''), 'op' : l[1], 'value' : l[2]}
        elif model in l[2]:
            return {'model' : model.rstrip('.'), 'field' : l[2].replace(model,''), 'op' : INVERTED_STD_OP[' '+l[1]+' '], 'value' : l[0]}
    return {}

class inequality_engine:
    def __init__(self, input_string):
        input_string = ingest(input_string)
        or_groups = input_string.split(';')
        self.filters = []
        for og in or_groups:
            conditions = og.split(',')
            converted = []
            for cond in conditions:
                
                converted.extend(convert_ranges(expand_metadata(cond)))
            self.filters.append(converted)
        
        if not self.filters or self.filters == [['']]:
            raise ValueError("No filter defined. Aborting.")

    def run(self):
        return any(map(lambda and_group: all(map(lambda expr: eval(expr), and_group)), self.filters))

    def get_dicts(self):
        filter_dicts = []
        for fil in self.filters:
            dicts = []
            for cond in fil:
                dicts.append(get_dict(cond))
            filter_dicts.append(dicts)
        return filter_dicts

    def get_query_columns(self, fil : dict, model : str = "models.DataIdentifier."):
        columns = []
        for cond in fil:
            if not (model+cond['field']) in columns:
                columns.append(model+cond['field'])
        return columns

    def createQuery(self, session, model = "models.DataIdentifier"):
        queries = []
        for fil in self.get_dicts():
            query = session.query(tuple(self.get_query_columns(fil)))
            for cond in fil:
                query = query.filter(cond)
            queries.append(query)
        return queries

import sys

if __name__ == "__main__":
    string = ''.join(sys.argv[1:])
    ie = inequality_engine(string)
    print(ie.filters)
    print(ie.get_dicts())