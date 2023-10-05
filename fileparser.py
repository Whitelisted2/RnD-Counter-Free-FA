from lark import Lark, Transformer
import subprocess
import openpyxl
import os

## to test the file regex list

want_excel = 0
file_path = "sandbox/longlist.txt"
ratex = ""
rid = 0 # dict populator
decision = "False"

ratex_dict = {}

l_file = Lark(r"""
       start: (module)* /[\n]+/

       module: "p" id ": spec: " property "\np" id ": ugly_RE: " initregex "\np" id ": bad_RE: " initregex "\np" id ": good_RE: " initregex "\n\n"

       initregex: /[^\n]+/  -> print_str
              |
                     
       regex: character
              | "(" regex "|" regex ")"
              | regex regex
              | regex "*"
              | "(" regex ")"
       
       character: "<" name ">"
                     
       id: SIGNED_NUMBER
              
       name: /[a-zA-z]+/
         
       property: /[^\n]+/
       
       WS: /[\t]+/
                   
       %import common.ESCAPED_STRING
       %import common.SIGNED_NUMBER
       %import common.WS_INLINE
       %ignore WS_INLINE
              
       """)

class MyTransformer(Transformer):
       # def print_id(self, token):
       #        print(token[0].children[0].value)

       def print_str(self, token):
              global ratex, rid, ratex_dict
              ratex = token[0].replace("|", "U").replace("<", "").replace(">", "")
              # print(ratex) (ratex,)
              # print(ratex)
              new = token[0].replace("|", " ").replace(")", "").replace("(", "").replace("*","").replace("><", "> <").split(" ")
              new = set(new)
              # print(new)
              # print(len(new))
              IsAperiodicExp(ratex)
              
              # print("ratex"+str(rid))
              rid+=1
              ratex_dict[rid] = (ratex, decision)
              # os._exit(1)

def IsAperiodicExp(exp):
       global decision
       cmd = """
       ./bin/gap.sh -r -b -q << EOI
       LoadPackage(\"automata\");
       LoadPackage(\"semigroup\");

       rat := RationalExpression(\""""+ exp +"""\");
       ss := SyntacticSemigroupLang(rat);

       Print(\"Aperiodic? \");
       Print(IsAperiodicSemigroup(ss));
       Print(\"\\n\");
       quit;

       EOI
       """
       # print(cmd)
       output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
       output = output.decode('utf-8')
       print(output)
       if output.find("true") == -1:
              decision = "false"
       else:
              decision = "true"


with open(file_path, 'r') as file:
       prop_str = file.read()
       #  print(prop_str)
       tokens = l_file.parse(prop_str)
       #  print(tokens)
       #  parse_tree_json = tokens.pretty()
       result = MyTransformer().transform(tokens)

if want_excel:
       workbook = openpyxl.Workbook()
       # workbook = openpyxl.load_workbook('sandbox/output.xlsx')
       sheet = workbook.active
       sheet["A1"] = "Rational Expression"
       sheet["B1"] = "Aperiodic?"
       sheet["C1"] = "Note: The 'false' ones may not have been processed by gap (in the current format) properly."
       for i in range(2, rid+2):
              # print(ratex_dict[i][0])
              # print(ratex_dict[i][1])
              sheet["A"+str(i)] = ratex_dict[i-1][0]
              sheet["B"+str(i)] = ratex_dict[i-1][1]
       # if os.path.exists('sandbox/output.xlsx'):
       #        os.remove('sandbox/output.xlsx')
       workbook.save('sandbox/output.xlsx')
       print("Output is saved in sandbox/output.xlsx")
else:
       print(ratex_dict)
