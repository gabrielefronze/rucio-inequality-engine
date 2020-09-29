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

def clear_double_spaces(input_string : str) -> str:
    input_string = input_string.strip().rstrip()
    while '  ' in input_string:
        input_string = input_string.replace('  ',' ')
    return input_string

def translate(input_string : str) -> str:
    for translated_op in OP.keys():
        op_list = OP[translated_op]
        for op in op_list:
            input_string = input_string.replace(op, translated_op)
    return input_string

class inequality_engine:
    def __init__(self, input_string):
        input_string = clear_double_spaces(translate(clear_double_spaces(input_string)))
        or_groups = input_string.split(';')
        self.filters = []
        for og in or_groups:
            self.filters.append(og.split(','))

    def run(self):
        return any(map(lambda and_group: all(map(lambda expr: eval(expr), and_group)), self.filters))

if __name__ == "__main__":
    string = "5 > 2, True and True, True or False; 6 < 5 > 4"
    ie = inequality_engine(string)
    print(ie.filters)
    print(ie.run())
    # x = 1
    # y = 0
    # for op in VALID_OP:
    #     string = 'x'+op+'y'+op+'-2'
    #     op_string = clear_double_spaces(translate(clear_double_spaces(string)))
    #     print('{} -> {}'.format(op_string, eval(op_string)))