!pip3 install -r requirements.txt 

model_build_commands = """#!/bin/bash
            pip3 install -r requirements.txt"""

with open("cdswbuild.sh", "w") as file:
    file.write(model_build_commands)
