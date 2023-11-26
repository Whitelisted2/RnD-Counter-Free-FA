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
- An input file whose path is specified using ```config.json``` must contain exactly ONE regex, with characters delimited by angular brackets, and with the regex ending in a newline. Examples of such inputs include: ```(<a><a>)*```, ```(<aa><ab>)*```, etc. Note that ```(<a><bc>)*``` is different from ```(<a><b><c>)*``` in this way. Some sample inputs have been provided in the folder ```test_regex/```

### Example 1: ```(<a><b>)*```

### Example 2: ```(<a><b><a><b>)*```
