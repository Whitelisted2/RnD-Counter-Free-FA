### for the property file with regex in it.
# first, must make the 'inductive' form of regex. then, put into GAP and manipulate

# from lark import Lark, Transformer
import subprocess
# import os
import sys
import openpyxl

want_excel = 1
decision = "False"
ratex_dict = {}
rid = 0
filepath = "sandbox/property_files/shortlist.txt" # default

if len(sys.argv) == 2:
    filepath = sys.argv[1] # within sandbox ...

command = """ 
    cd sandbox/regex_formatter/;
    make clean;
    make compiler;
    bash runme.sh ../../"""+ filepath +""" ../output.txt;
    """
regex_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
regex_output = regex_output.decode('utf-8')
# print(regex_output)


def IsAperiodicExp(line):
    global decision, rid, ratex_dict
    cmd = """
    touch sandbox/PeriodicList.txt;
    ./bin/gap.sh -r -b -q << EOI
    LoadPackage(\"automata\");;
    LoadPackage(\"semigroup\");;
    LoadPackage(\"datastructures\");;

    rat := """+ line +""";
    Print(\"\\n----\");
    Print(rat);
    Print(\"|\");

    ss := SyntacticSemigroupLang(rat);;
    
    Print(\"\\nAperiodic? \");
    AperiodicStatus := IsAperiodicSemigroup(ss);
    Print(AperiodicStatus);
    Print(\"\\n\");

    if AperiodicStatus then
        # aperiodic
        Print(\"\\nTransition Semigroup: \");
        aut := RatExpToAut(rat);;
        ts := TransitionSemigroup(aut);;
        # Print(ts);
        # Print(\"\\n\");

        ss3 := SemigroupByGenerators(ts);;
        gen := GeneratorsOfSemigroup(ss3);;
        mon := MonoidByGenerators(gen);;

        # Print(\"\\nGenerators: \");
        # Print(gen);

        Print(\"\\nMultiplication Table: \\n\");
        mult := MultiplicationTable(mon);
        # Print(mult);
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
    # print(output)
    print("Processing ratex [", rid+1, "]")
    output_arr = output.split("\n")

    temprat = ""
    for ele in output_arr:
        if ele[-1] == "\\":
            temprat += ele[:-1]
        if ele[-1] == "|":
            temprat += ele[:-1]
            break
    
    genrat = temprat[4:]
    # print(output)
    # genrat = ""
    # for outputline in output_arr:
    #      if(len(outputline) > 3 and outputline[:4] == "----"):
    #           genrat = outputline[4:]

    if output.find("Aperiodic? true") == -1:
        decision = "periodic"
        cmd2 = """ 
        python3 sandbox/graphchecker.py;
        rm sandbox/PeriodicList.txt;
        """
        output2 = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT)
        output2 = output2.decode('utf-8')
        # print("_______________________________________")
        print(output2)
        # print("_______________________________________")

    else:
        decision = "aperiodic"
        cmd2 = """ rm sandbox/PeriodicList.txt; """
        output2 = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT)
        output2 = output2.decode('utf-8')
    rid += 1
    ratex_dict[rid] = (genrat, decision)


with open("sandbox/output.txt", "r") as file:
    lines = file.read()
    lines = lines.split("\n")
    for line in lines:
        # print(line)
        if line != "":
            IsAperiodicExp(line)

if want_excel:
       workbook = openpyxl.Workbook()
       # workbook = openpyxl.load_workbook('sandbox/output.xlsx')
       sheet = workbook.active
       sheet["A1"] = "Rational Expression"
       sheet["B1"] = "Aperiodic?"
    #    sheet["C1"] = "Note: The 'false' ones may not have been processed by gap (in the current format) properly."
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

