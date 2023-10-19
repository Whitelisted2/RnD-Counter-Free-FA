import json
import subprocess
from datetime import datetime
import sys
import re

with open("sandbox/config.json", "r") as json_file:
    data = json.load(json_file)
# print(data)

# data is the whole dictionary
inputfilepath = data["input_params"]["input_filepath"] # within sandbox
# print(inputfilepath)

# use given folder name, else 
folder_name_op = [ re.sub(r'\W+', '', str(data["output_params"]["output_name"])) if (data["output_params"]["output_name"] != "output" and re.sub(r'\W+', '', data["output_params"]["output_name"]) != "") else re.sub(r'\W+', '', str(datetime.now().strftime("%H:%M:%S"))) ]
outputfolder = "sandbox/output/" + folder_name_op[0] # to make new folder

if(data["output_params"]["output_folder"] == True):
    cmd = """ rm -rf """+ outputfolder +""";
            mkdir """+ outputfolder +""" ;"""
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    prefix = outputfolder + "/" + folder_name_op[0]

    data["output_params"]["prefix"] = prefix
    with open("sandbox/config.json", "w") as write_file:
      json.dump(data, write_file, indent=4)

    # creating files before dumping output
    # cmd = """
    # touch """+ prefix +""".periodicity;
    # touch """+ prefix +""".automaton;
    # touch """+ prefix +""".semigroup;
    # touch """+ prefix +""".counters;
    # touch """+ prefix +""".mult;
    # touch """+ prefix +""".regex;
    # """
    # output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    # output = output.decode('utf-8')

    cmd = """ 
    python3 sandbox/regexparser.py """ + inputfilepath + """ ;
    """
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    print(output)

    data["output_params"]["prefix"] = ""
    with open("sandbox/config.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    cmd = """
        cp sandbox/tmp/temp1.aperiodicity """+ prefix +""".aperiodicity;
        cp sandbox/tmp/temp1.automaton """+ prefix +""".automaton;
        cp sandbox/tmp/temp1.semigroup """+ prefix +""".semigroup;
        cp sandbox/tmp/temp1.counters """+ prefix +""".counters;
        cp sandbox/tmp/temp1.mult """+ prefix +""".mult;
        cp sandbox/tmp/temp1.regex """+ prefix +""".regex;
        cp sandbox/tmp/temp1.dotstring """+ prefix +""".dotstring;
        rm -rf sandbox/tmp/* ;
        """
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    

else:
    cmd = """ 
        python3 sandbox/regexparser.py """ + inputfilepath + """ ;
        """

    # print(cmd)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    print(output)

# to rewrite to json if reqd
# with open("sandbox/data_file.json", "w") as write_file:
#     json.dump(data, write_file, indent=4)