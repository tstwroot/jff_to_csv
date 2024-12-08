import xmltodict
from sys import argv
from os import path, remove

class JFF2CSV:
    def __init__(self, input:str, output:str):
        self.input = input
        self.output = output
        
    def have_transitions(self, object:dict, id:str) -> bool:
        for transition in object['transition']:
            if(transition['from'] == id):
                return True
        return False
    
    def convert(self):
        with open(self.input) as jff_file:
            jff_dict = xmltodict.parse(jff_file.read())['structure']['automaton']
            
            with open(self.output, "w") as input_file:
                for state in jff_dict['state']:
                    if(self.have_transitions(jff_dict, state['@id'])):
                        for transition in jff_dict['transition']:
                            if(transition['from'] == state['@id']):
                                if 'initial' in dict.keys(state):
                                    input_file.write("->")

                                if 'final' in dict.keys(state):
                                    input_file.write("*")
                                    continue

                                input_file.write(f"{state['@name']},{transition['read']},q{transition['to']}\n")
                    else:
                        input_file.write(f"*{state['@name']},-,-\n")

if(__name__ == '__main__'):
    if argv.__len__() != 3:
        print(f"Usage: python3 ./{path.basename(__file__)} <input.jff> <output.csv>")
        exit(1)
    
    jff2csv = JFF2CSV(argv[1], argv[2])
    jff2csv.convert()