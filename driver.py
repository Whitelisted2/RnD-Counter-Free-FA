import json
import subprocess
from datetime import datetime
import sys
import re
import os

with open("sandbox/config.json", "r") as json_file:
    data = json.load(json_file)
# print(data)

# data is the whole dictionary
inputfilepath = data["input_params"]["input_filepath"] # within sandbox
if not os.path.isfile(inputfilepath):
    print("ABORTED: Bad input filepath in config.")
    os._exit(3)
# print(inputfilepath)

# use given folder name, else 
file_name_op = [ re.sub(r'\W+', '', str(data["output_params"]["output_name"])) if (data["output_params"]["output_name"] != "output" and re.sub(r'\W+', '', data["output_params"]["output_name"]) != "") else re.sub(r'\W+', '', str(datetime.now().strftime("%H:%M:%S"))) ]
outputfolder = data["output_params"]["output_folder"] # to make new folder
prefix = outputfolder
if not os.path.isdir(outputfolder):
    try:
        cmd = """ mkdir """+ prefix +""";"""
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except:
        print("ABORTED: Bad output directory path in config.")
        os._exit(3)

if(data["output_params"]["want_output_folder"] == True):

    cmd = """ 
    python3 sandbox/newregexparser.py """ + inputfilepath + """ ;
    """
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    print(output)
    
    prefix = prefix + '/' + file_name_op[0]
    cmd = """
        cp sandbox/tmp/temp1.aperiodicity """+ prefix +""".aperiodicity;
        cp sandbox/tmp/temp1.automaton """+ prefix +""".automaton;
        cp sandbox/tmp/temp1.semigroup """+ prefix +""".semigroup;
        if [ -f "sandbox/tmp/temp1.counters" ]
        then
            cp sandbox/tmp/temp1.counters """+ prefix +""".counters; 
        fi;
        cp sandbox/tmp/temp1.mult """+ prefix +""".mult;
        cp sandbox/tmp/temp1.ratex """+ prefix +""".ratex;
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

