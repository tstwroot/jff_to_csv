import xmltodict
from sys import argv
import os

class JFF2CSV:
    def __init__(self):
        pass

    def __haveTransitions(self, object:dict, id:str) -> bool:
        for transition in object['transition']:
            if(transition['from'] == id):
                return True
        return False
    
    def convert(self, input:str, output:str):
        last_string_output = ""
        with open(input) as input_file:
            jff_dict = xmltodict.parse(input_file.read())['structure']['automaton']
            with open(output, "w") as output_file:
                for state in jff_dict['state']:
                    if(self.__haveTransitions(jff_dict, state['@id'])):
                        for transition in jff_dict['transition']:
                            if(transition['from'] == state['@id']):
                                if 'initial' in dict.keys(state) and last_string_output != "->":
                                    output_file.write("->")
                                    last_string_output = "->"

                                if 'final' in dict.keys(state) and last_string_output != "*":
                                    output_file.write("*")
                                    last_string_output = "*"
                                    continue
                                
                                last_string_output = f"{state['@name']},{transition['read']},q{transition['to']}\n"
                                output_file.write(last_string_output)
                    else:
                        last_string_output = f"*{state['@name']},-,-\n"
                        output_file.write(last_string_output)

if(__name__ == '__main__'):
    if argv.__len__() != 3:
        print(f"Usage: python3 ./{os.path.basename(__file__)} <input.jff> <output.csv>")
        exit(1)
    
    jff2csv = JFF2CSV()
    jff2csv.convert(argv[1], argv[2])

