# RnD-Counter-Free-FA
This repository contains files related to RnD Project (Autumn 2023).

### Instructions
- Download the latest version of the GAP software from [here](https://www.gap-system.org/Download/).
- Create a folder called sandbox within GAP (may appear as ```gap-<version>/```), and place all of this repo's files in this ```sandbox/``` folder.
- Modify ```sandbox/config.json``` according to the input you need, and to specify output location(s). (Note that, here, paths begin from the ```sandbox/``` folder. Absolute paths would create issues in the current form of the code.)
  - ```is_regex_or_aut``` refers to whether the input file contains a regex (```"reg"```) or an automaton (```"aut"```). 
  - ```input_filepath``` refers to the location of the input file. 
  - ```output_folder``` refers to the folder that would be created to store all of the output files. Ensure that this folder does not have files that you want to keep saved, and that the directory that holds this folder exists already.
  - ```output_name``` denotes the common prefix that the output files will have, such as ```<output_name>.dotstring```, ```<output_name>.mult```, etc.
- Run ```python3 sandbox/driver.py``` to generate output according to the specified inputs.
Example of config file configurations are as follows:
- For Example 1:
  ![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/edd53bca-62bc-4231-a6b8-aecb4c1fab6c)
- For Example 4:
  ![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/125d095f-8794-48ab-8400-b3421b678e4b)


### Format of input file (regex)
- An input file whose path is specified using ```config.json``` must contain exactly ONE regex, with characters delimited by angular brackets, and with the regex ending in a newline. Examples of such inputs include: ```(<a><a>)*```, ```(<aa><ab>)*```, etc. Note that ```(<a><bc>)*``` is different from ```(<a><b><c>)*``` in this way. Some sample inputs have been provided in the folder ```test_regex/```. An example:
  ![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/aa3f6578-d4cc-4555-9b8b-f63bc4ceda4f)

### Format of input file (automaton)
- An input file path whose path is specified using ```config.json``` must contain an automaton in the following format:
  - Line 1: Type of automaton ( ```DFA```, ```NFA``` or ```ENFA```)
  - Line 2: Number of states (one positive integer number)
  - Line 3: Size of alphabet (one positive integer number) (Note: If ENFA, then last letter of alphabet is presumed to be $\epsilon$. So, if alphabet is ${a, b}$ for an ENFA, then set this line to 3)
  - Line 4: Initial state of automaton (one positive integer number)
  - Line 5: Final state (or states, separated by commas)
  - Line 6 onwards: Transition table, with each line denoting the resultant state/states for the transition from each given state based on some alphabet. (Empty/dead entries are not handled as of now, so in such cases, please use a trap state)
- Two examples of such an input file are below: (Other examples are listed in the ```test_aut/``` directory.

![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/37638243-0c92-4aac-8b1b-e059d6468848)

![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/a4ea034a-9e49-498c-9bc8-1d4b1c13b7af)


### General Working
- First, ```newregexparser.py``` is invoked, and it passes the input regex into GAP in a comprehensible format. Most outputs are taken from GAP and dumped into the specific input files. (For automata, the process is very similar; the program ```automatonparser.py``` puts the input automaton into the GAP format, and then this is converted into a regex in GAP. The rest of the process is same as that of the regex.)
- For counter-based information, if the regex entered represents a periodic event, ```graphchecker.py``` constructs the permutation graphs of each transformation present in the monoid associated with the regex. Based on this, the counter is specified using the word ```w``` and the Mod-N-ness of the counter.

### Example 1: ```(<a><b>)*``` (via regex)
- The output generated on running  ```python3 sandbox/driver.py``` with the above regex placed in the input file mentioned in ```config.json``` is as follows:
![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/e9b74a73-ec82-4b4e-975f-29edd8bf6e45)


### Example 2: ```(<a><b><a><b>)*``` (via regex)
- The output generated on running  ```python3 sandbox/driver.py``` with the above regex placed in the input file mentioned in ```config.json``` is as follows:
![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/4ade3453-4566-41ed-8182-36611ec443dc)

### Example 3: ```(<a><a>)*``` (via automaton)
- The output generated on running  ```python3 sandbox/driver.py``` with the automaton for the above placed in the input file (```test_aut/aa.txt```) mentioned in ```config.json``` is as follows:
![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/39ea7076-0959-4054-9546-bdf1ba3eb6b9)

### Example 3: ```(<a>)*``` (via automaton)
- The output generated on running  ```python3 sandbox/driver.py``` with the automaton for the above placed in the input file (```test_aut/a1.txt```) mentioned in ```config.json``` is as follows:
![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/3fb3901a-31f6-4f21-8481-46258b8986a6)


> "Energy may be likened to the bending of a crossbow; decision, to the releasing of a trigger" — Sun Tzu, The Art of War
