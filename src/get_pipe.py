import os

path = "pipe.txt"

pipe = os.getenv("state.viame_pipeline")

assert pipe, "pipe didn't read."
    
with open(path, "w") as f:
    f.write(pipe)
