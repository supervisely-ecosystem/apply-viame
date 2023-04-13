import subprocess
import os

path = "pipe.txt"

with open(path, "w") as f:
    f.write(os.getenv("state.viame_pipeline"))
