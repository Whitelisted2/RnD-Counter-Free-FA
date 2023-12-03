from lark import Lark, Transformer
import json
import sys

input_path = sys.argv[1]
# print(input_path)

grammar = r"""
    start: aut_type "\n" num_states "\n" size_alpha "\n" init_state "\n" final_states "\n" transition_table
    aut_type: TYPES
    TYPES: "DFA" | "NFA" | "ENFA"
    num_states: NUMBER
    size_alpha: NUMBER
    
    transition_table: transition_line (transition_line)*
    transition_line: transition_entry (" " transition_entry)* "\n"
    transition_entry: transition_alpha ("," transition_alpha)*
    transition_alpha: NUMBER | EMP
    EMP: "@"

    init_state: NUMBER
    final_states: NUMBER ("," NUMBER)*
    
    NUMBER: /\d+/
    """

lines = ""
with open(input_path, 'r') as f:
    lines = f.read()
# print(lines)



class AutTransformer(Transformer):
    def start(self, items):
        aut_type, num_states, size_alpha, init_state, final_states, transition_table = items
        aut_type = aut_type.children[0].value
        num_states = num_states.children[0].value
        size_alpha = size_alpha.children[0].value
        init_state = init_state.children[0].value
        final_state_list = []
        for state in final_states.children:
            final_state_list.append(state.value)
        
        ttable = []
        for line in transition_table.children:
            tline = []
            for entry in line.children:
                tentry = []
                for element in entry.children:
                    tentry.append(element.children[0].value)
                tline.append(tentry)
            ttable.append(tline)

        return aut_type, num_states, size_alpha, init_state, final_state_list, ttable
    
input_data = lines
parser_no_t = Lark(grammar, parser='lalr', transformer=AutTransformer())
result = parser_no_t.parse(input_data)
# print(result)

final_string_rhs = "Automaton("

if result[0] == "DFA":
    final_string_rhs += "\"det\""
elif result[0] == "NFA":
    final_string_rhs += "\"nondet\""
elif result[0] == "ENFA":
    final_string_rhs += "\"epsilon\"" # by default, last alphabet is considered epsilon. so input size of alphabet as real_size+1 for epsilon nfa
else:
    print("Invalid automaton type!")

final_string_rhs += ","
final_string_rhs += str(result[1]) # num of states
final_string_rhs += ","
final_string_rhs += str(result[2]) # size of alphabet
final_string_rhs += ","

if result[0] != "DFA":
    final_string_rhs += str(result[5]).replace("'","")
else:
    for line_num in range(len(result[5])):
        for entry_num in range(len(result[5][line_num])):
            result[5][line_num][entry_num] = result[5][line_num][entry_num][0]
    # print(result[5])
    final_string_rhs += str(result[5]).replace("'","")
final_string_rhs += ","
final_string_rhs += "["
final_string_rhs += str(result[3])
final_string_rhs += "]"
final_string_rhs += ","
final_string_rhs += str(result[4]).replace("'","")
final_string_rhs += ")"

print(final_string_rhs)