!pip3 install -r requirements.txt 

model_build_commands = """#!/bin/bash
pip3 install -r requirements.txt"""

with open("cdsw-build.sh", "w") as file:
    file.write(model_build_commands)
