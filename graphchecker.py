import networkx as nx
from lark import Lark, Transformer
import ast # for (list) string to list

file_path = "sandbox/PeriodicList.txt"
n = -1

l_trans = Lark(r"""
               start: "Transformation" array word
               array: /([^\n]+):/ -> get_array
                word: /[^\n]+/ -> get_word
                """)

word_dict = {}
trans_key = []
trans_value = ""

class MyTransformer2(Transformer):
    def get_array(self, token):
        global trans_key
        trans_key = token[0].replace("(", "").replace(")", "").replace(":", "") # not currently in use. perhaps when the word is identified

    def get_word(self, token):
        global trans_value
        trans_value = generate_word_from_index(token[0])
        word_dict[trans_key] = trans_value

def generate_word_from_index(arrstr):
    res = ast.literal_eval(arrstr)
    word = ""
    for i in range(len(res)):
        res[i] = getExcelCol(res[i])
        word = word + res[i]
    return word

def getExcelCol(num):
    name = "";
    while (num > 0):
        modulo = (num - 1) % 26;
        name = chr(ord('a') + modulo) + name;
        num = int((num - modulo)/26);
    return name

with open(file_path, 'r') as file:
    # print("_______________________________________")
    tr_unfiltered = ""
    for line in file:
        if n == -1:
            n = int(line) # get num of nodes in graph
        elif str(line).replace("\n", "").replace(" ", "")[-1] != ']':
            tr_unfiltered += str(line).replace("\n", "").replace(" ", "")[:-1]
            # print(tr_unfiltered)
        else:
            tr_unfiltered += str(line).replace("\n", "").replace(" ", "")
            # print(tr_raw)
            # print("hello", tr_unfiltered)
            tr_split = tr_unfiltered.split(":")
            tr_raw = tr_split[0]
            tr_word_raw = tr_split[1]
            if tr_raw == "IdentityTransformation":
                continue
            # print(tr_unfiltered)
            tokens = l_trans.parse(tr_unfiltered)
            result = MyTransformer2().transform(tokens)
            # print(result)
            #     pass

            tr_name = tr_raw.replace("Transformation", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "")
            # print(tr_name)
            tr_instance = [
                int(item) if item.isdigit() else item
                for item in tr_name.split(',')
            ]
            # print(tr_instance)

            edges = []
            for i in range(1, n+1):
                if(i > len(tr_instance)):
                    # edges.append((i, i))
                    pass
                else:
                    if i != tr_instance[i-1]:
                        edges.append((i, tr_instance[i-1]))

            # print(edges)
            # print(word_dict)

            G = nx.DiGraph(edges)
            key = "["+ tr_name +"]"

            # f = open("sandbox/tmp/temp1.counters", "w")
            # f.close()

            f = open("sandbox/tmp/temp1.counters", "a")
            for cycle in nx.simple_cycles(G):
                word = word_dict[key]
                
                opstring = "Mod "+str(len(cycle))+" counter for "+ word
                print(opstring)
                f.write(opstring+"\n")

            f.close()
            tr_unfiltered = ""
                
    # print("_______________________________________")

# edges = [(1, 2),(3, 4),(4, 3),(3, 4)]

# G = nx.DiGraph(edges)

# for cycle in nx.simple_cycles(G):
#     print(cycle)