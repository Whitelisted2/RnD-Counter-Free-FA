### consider a file conatining one regex, or perhaps a list of regex.

from lark import Lark, Transformer
import subprocess
import os

file_path = "sandbox/test_regex/regex1.txt"
ratex = ""
rid = 0 # dict populator
decision = "False"
ratex_dict = {}

command = """ 
    cd sandbox/regex_formatter/;
    make clean;
    make compiler;
    bash runme.sh ../longlist.txt ../output.txt;
    """
regex_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
regex_output = regex_output.decode('utf-8')
print(regex_output)

class MyTransformer(Transformer):
    def print_ratex(self, token):
        global ratex, rid, ratex_dict
        ratex = token[0].replace("|", "U").replace("<", "").replace(">", "")
        # print(ratex) (ratex,)
        # print(ratex)
        new = token[0].replace("|", " ").replace(")", "").replace("(", "").replace("*","").replace("><", "> <").split(" ")
        new = set(new)
        # print(ratex)
        # print(len(new))
        
        # run regex_formatter
        IsAperiodicExp(ratex)
        
        # print("ratex"+str(rid))
        rid+=1
        ratex_dict[rid] = (ratex, decision)
        # os._exit(1)

def IsAperiodicExp(exp):
        global decision

        cmd = """
        ./bin/gap.sh -r -b -q << EOI
        LoadPackage(\"automata\");;
        LoadPackage(\"semigroup\");;
        LoadPackage(\"datastructures\");;

        rat := RationalExpression(\""""+ exp +"""\");
        # rat := (_____)
        ss := SyntacticSemigroupLang(rat);

        Print(\"Aperiodic? \");
        AperiodicStatus := IsAperiodicSemigroup(ss);
        Print(AperiodicStatus);
        Print(\"\\n\");

        if AperiodicStatus then
            # aperiodic
            Print(\"\\nTransition Semigroup: \");
            aut := RatExpToAut(rat);;
            ts := TransitionSemigroup(aut);;
            Print(ts);
            Print(\"\\n\");

            ss3 := SemigroupByGenerators(ts);;
            gen := GeneratorsOfSemigroup(ss3);;
            mon := MonoidByGenerators(gen);;

            Print(\"\\nGenerators: \");
            Print(gen);

            Print(\"\\nMultiplication Table: \\n\");
            mult := MultiplicationTable(mon);
            Print(mult);
            Print(\"\\n\");
        else
            # periodic
            Print(\"\\nPeriodic: \");
            # Print(\"\\nSyntactic Semigroup: \");
            # Print(ss);

            aut := RatExpToAut(rat);
            n := NumberStatesOfAutomaton(aut);
            ts := TransitionSemigroup(aut);
            Print(aut);
            ss3 := SemigroupByGenerators(ts);
            gen := GeneratorsOfSemigroup(ss3);
            mon := MonoidByGenerators(gen);

            # Print(\"\\nTransition Semigroup: \");
            # Print(ts);
            # Print(\"\\n\");

            # Print(\"\\nMultiplication Table: \\n\");
            # mult := MultiplicationTable(mon);
            # OutputLogTo(\"sandbox/PeriodicList.txt\");
            # Print(mon);
            # OutputLogTo();
            Print(\"\\n\");
            
            tsset := Elements(ts);
            # monset := Elements(mon);
            # monset := [ts[1]];

            real_gen := GeneratorsOfSemigroup(ts);
            # each ele of realgen to be enumerated to disambiguate the list... s, p, sp, ss, ps, pp, ....

            # Print(real_gen);
            # Print(tsset);
            # open := PlistDeque();

            open := [];
            closed := [];
            # curr_path := [];
            hash := HashMap();
            for ele in real_gen do                 # init open list
                Append(open, [ele]);
                hash[ele] := [Position(real_gen, ele)];
                # Append(closed, [ele]);
            od;
            # Print(\"\\nOpen:\");
            # Print(open);
            # Print(\"\\nClosed:\");
            # Print(closed);
            # for ele in open do
            #     Print(\"\\nElement: \", ele, \" id = \", hash[ele]);
            # od;
            while (not IsEmpty(open)) do
                # Print(\"\\nreenter\");
                curr := Remove(open,1);             # s p
                # Print(open);
                curr_path := hash[curr];
                for ele in real_gen do
                    child := curr*ele; # hashmap bfs
                    temp := ShallowCopy(curr_path);
                    # Print(\"\\ncurr = \", curr);
                    # Print(\"\\nhash = \", hash);
                    # Print(\"\\ntemp = \", curr_path);
                    Append(temp, [Position(real_gen, ele)]);
                    if ((not (child in Keys(hash))) and (not (child in real_gen)) and (not (child = curr))) then
                        # Print(\" yes \");
                        hash[child] := temp;
                        # Print(\"\\nhash[\", child, \"] =\", temp);
                    fi;
                    if ((not (child in open)) and (not (child in closed)) and (not (child = curr)) and (not (child in real_gen))) then
                        Append(open, [child]);
                        # Print(\"\\nFor \", child ,\", unique moment=\");
                        # Print(hash[child]);
                    else
                        # Print(\"\\nhey! hash=\");
                        # Print(hash[child]);
                    fi;
                od;
                Append(closed, [curr]);
                # Print(\"\\nOpen:\");
                # Print(open);
                # Print(\"\\nClosed:\");
                # Print(closed);
                
            od;
            
            
            # for ele in closed do
            #     Print(\"\\nElement: \", ele, \" id = \", hash[ele]);
            # od;
            ##################################
            OutputLogTo(\"sandbox/PeriodicList.txt\");;
                Print(n);;
                Print(\"\\n\");;
                for ele in tsset do
                    Print(ele);;
                    Print(" : ");;
                    Print(hash[ele]);;
                    Print(\"\\n\");;
                od;;
            OutputLogTo();;

            

        fi;
        quit;
        EOI
        """
        # print(cmd)
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        print(output)
        if output.find("Aperiodic? true") == -1:
            decision = "periodic"
            cmd2 = """ python3 sandbox/graphchecker.py """
            output2 = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT)
            output2 = output2.decode('utf-8')
            # print("_______________________________________")
            print(exp)
            print(output2)
            # print("_______________________________________")

        else:
            decision = "aperiodic"

        

# with open(file_path, 'r') as file:
#        prop_str = file.read()
#        #  print(prop_str)
#        tokens = l_regex.parse(prop_str)
#        #  print(tokens)
#        #  parse_tree_json = tokens.pretty()
#        result = MyTransformer().transform(tokens)

# print(ratex_dict)