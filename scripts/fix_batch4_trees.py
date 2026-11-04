import re

with open(r"c:\Users\Sayantan Dutta\OneDrive\Desktop\Ready2Code\scripts\generate_batch4.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect how tree building was done and replace with BFS queue builder
print("Count of TreeNode in generate_batch4.py:", code.count("class TreeNode"))
