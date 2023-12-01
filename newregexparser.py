### for the property file with one angular-bracket-delimited regex in it.
# first, must make the 'inductive' form of regex. then, put into GAP and manipulate
# this is a bit more robust than regexparser.py

# from lark import Lark, Transformer
import subprocess
import os
import sys
import openpyxl
import json

with open("sandbox/config.json", "r") as json_file:
    data = json.load(json_file)

want_excel = 0
decision = "False"
ratex_dict = {}
rid = 0
file_path = "sandbox/property_files/shortlist.txt" # default

if len(sys.argv) == 2:
    file_path = sys.argv[1] # within sandbox ...

if not os.path.isfile(file_path):
    print("\n Enter path of the file within 'sandbox/' (File does not seem to exist) \n")
    os._exit(1)

command = """ 
    cd sandbox/regex_formatter/;
    make clean;
    make compiler;
    bash runme.sh ../../"""+ file_path +""" ../output.txt;
    """
regex_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
regex_output = regex_output.decode('utf-8')
# print(regex_output)


def IsAperiodicExp(line):
    global decision, rid, ratex_dict, data
    want_folder = data["output_params"]["want_output_folder"]

    insert_flag = ""
    if(want_folder):
        insert_flag = "flag := true;\n"

    cmd = """
    
    touch sandbox/PeriodicList.txt;
    ./bin/gap.sh -r -b -q << EOI
    flag := false;

    """+insert_flag+"""

    LoadPackage(\"automata\");;
    LoadPackage(\"semigroup\");;

    rat := """+ line +""";
    Print(rat);
    if flag then PrintTo(\"sandbox/tmp/temp1.ratex\", rat); fi;

    ss := SyntacticSemigroupLang(rat);;
    
    Print(\"\\nAperiodic? \");
    AperiodicStatus := IsAperiodicSemigroup(ss);
    if flag then PrintTo(\"sandbox/tmp/temp1.aperiodicity\", AperiodicStatus); fi;
    Print(AperiodicStatus);
    Print(\"\\n\");

    aut := RatExpToAut(rat);;
    Print(aut);
    if flag then PrintTo(\"sandbox/tmp/temp1.dotstring\", DotStringForDrawingAutomaton(aut)); fi;

    if AperiodicStatus then
        # aperiodic
        Print(\"\\nTransition Semigroup: \");
        if flag then PrintTo(\"sandbox/tmp/temp1.automaton\", aut); fi;
        ts := TransitionSemigroup(aut);;
        tsset := Elements(ts);
        if flag then PrintTo(\"sandbox/tmp/temp1.semigroup\", tsset); fi;
        Print(ts);
        Print(\"\\n\");

        ss3 := SemigroupByGenerators(ts);;
        gen := GeneratorsOfSemigroup(ss3);;
        mon := MonoidByGenerators(gen);;

        Print(\"\\nGenerators: \");
        Print(gen);

        Print(\"\\nMultiplication Table: \\n\");
        mult := MultiplicationTable(mon);
        if flag then PrintTo(\"sandbox/tmp/temp1.mult\", mult); fi;
        Print(mult);
        Print(\"\\n\");
    else
        # periodic
        Print(\"\\nPeriodic: \");

        if flag then PrintTo(\"sandbox/tmp/temp1.automaton\", aut); fi;
        n := NumberStatesOfAutomaton(aut);
        ts := TransitionSemigroup(aut);
        ss3 := SemigroupByGenerators(ts);
        gen := GeneratorsOfSemigroup(ss3);
        mon := MonoidByGenerators(gen);
        mult := MultiplicationTable(mon);
        if flag then PrintTo(\"sandbox/tmp/temp1.mult\", mult); fi;
        
        tsset := Elements(ts);
        if flag then PrintTo(\"sandbox/tmp/temp1.semigroup\", tsset); fi;
        # monset := Elements(mon);
        # monset := [ts[1]];

        real_gen := GeneratorsOfSemigroup(ts);
        # each ele of realgen to be enumerated to disambiguate the list... s, p, sp, ss, ps, pp, ....

        open := [];
        closed := [];
        hash := HashMap();
        for ele in real_gen do                 # init open list
            Append(open, [ele]);
            hash[ele] := [Position(real_gen, ele)];
            # Append(closed, [ele]);
        od;

        while (not IsEmpty(open)) do
            curr := Remove(open,1);             # s p
            curr_path := hash[curr];
            for ele in real_gen do
                child := curr*ele; # hashmap bfs
                temp := ShallowCopy(curr_path);
                # Print(\"\\ncurr = \", curr);
                # Print(\"\\nhash = \", hash);
                # Print(\"\\ntemp = \", curr_path);
                Append(temp, [Position(real_gen, ele)]);
                if ((not (child in Keys(hash))) and (not (child in real_gen)) and (not (child = curr))) then
                    hash[child] := temp;
                fi;
                if ((not (child in open)) and (not (child in closed)) and (not (child = curr)) and (not (child in real_gen))) then
                    Append(open, [child]);
                else
                    # Print(\"\\nhey! hash=\");
                fi;
            od;
            Append(closed, [curr]);
        od;
        
        
        # for ele in closed do
        #     Print(\"\\nElement: \", ele, \" id = \", hash[ele]);
        # od;

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
    
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    print(output)

    output_arr = output.split("\n")

    if output.find("Aperiodic? true") == -1:
        decision = "periodic"
        cmd2 = """ 
        python3 sandbox/graphchecker.py;
        rm sandbox/PeriodicList.txt;
        """
        output2 = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT)
        output2 = output2.decode('utf-8')
        print(output2)

    else:
        decision = "aperiodic"
        cmd2 = """ rm sandbox/PeriodicList.txt; """
        output2 = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT)
        output2 = output2.decode('utf-8')
    rid += 1
    ratex_dict[rid] = (output_arr[2], decision)


with open("sandbox/output.txt", "r") as file:
    # open the regex inductive file
    lines = file.read()
    lines = lines.split("\n")
    for line in lines:
        if line != "":
            IsAperiodicExp(line)

if want_excel:
       workbook = openpyxl.Workbook()
       sheet = workbook.active
       sheet["A1"] = "Rational Expression"
       sheet["B1"] = "Aperiodic?"
    #    sheet["C1"] = "Note: The 'false' ones may not have been processed by gap (in the current format) properly."
       for i in range(2, rid+2):
              sheet["A"+str(i)] = ratex_dict[i-1][0]
              sheet["B"+str(i)] = ratex_dict[i-1][1]
       # if os.path.exists('sandbox/output.xlsx'):
       #        os.remove('sandbox/output.xlsx')
       workbook.save('sandbox/output.xlsx')
       print("Output is saved in sandbox/output.xlsx")
else:
       print(ratex_dict)

