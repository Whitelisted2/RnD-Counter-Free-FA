# RnD-Counter-Free-FA
This repository contains files related to RnD Project (Autumn 2023).

### Instructions
- Download the latest version of the GAP software from [here](https://www.gap-system.org/Download/).
- Create a folder called sandbox within GAP (may appear as ```gap-<version>/```), and place all of this repo's files in this ```sandbox/``` folder.
- Modify ```config.json``` according to the input you need, and to specify output location(s).
  - ```input_filepath``` refers to the location of the input file.
  - ```output_folder``` refers to the folder that would be created to store all of the output files. Ensure that this folder does not have files that you want to keep saved, and that the directory that holds this folder exists already.
  - ```output_name``` denotes the common prefix that the output files will have, such as ```<output_name>.dotstring```, ```<output_name>.mult```, etc.
- Run ```python3 sandbox/driver.py``` to generate output according to the specified inputs.

### Format of input file
- An input file whose path is specified using ```config.json``` must contain exactly ONE regex, with characters delimited by angular brackets, and with the regex ending in a newline. Examples of such inputs include: ```(<a><a>)*```, ```(<aa><ab>)*```, etc. Note that ```(<a><bc>)*``` is different from ```(<a><b><c>)*``` in this way. Some sample inputs have been provided in the folder ```test_regex/```.

### General Working
- First, ```newregexparser.py``` is invoked, and it passes the input regex into GAP in a comprehensible format. Most outputs are taken from GAP and dumped into the specific input files.
- For counter-based information, if the regex entered represents a periodic event, ```graphchecker.py``` constructs the permutation graphs of each transformation present in the monoid associated with the regex. Based on this, the counter is specified using the word ```w``` and the Mod-N-ness of the counter.

### Example 1: ```(<a><b>)*```
- The output generated on running  ```python3 sandbox/driver.py``` with the above regex placed in the input file mentioned in ```config.json``` is as follows:
![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/e9b74a73-ec82-4b4e-975f-29edd8bf6e45)


### Example 2: ```(<a><b><a><b>)*```
- The output generated on running  ```python3 sandbox/driver.py``` with the above regex placed in the input file mentioned in ```config.json``` is as follows:
![image](https://github.com/Whitelisted2/RnD-Counter-Free-FA/assets/90827725/4ade3453-4566-41ed-8182-36611ec443dc)


