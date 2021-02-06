"""
PURPOSE: Demonstrate best practice for building a script that has various
other scripts it references and files that it uses as inputs.

If there are standard inputs, they should be in subfolders of the script folder
and called with relative path, rather than calling with full path. By using 
relative path instead of absolute path, then if you move the package to a different
location or run on a different machine, the relative path references will not change
and thus not break.

"""

import os

script_dir = os.getcwd()

print(f"if nothing else specified, this script is running in {script_dir}")

# "subfolder" is a sub-folder of the folder in which the script is running
sd1 = "subfolder1"

out_txt = os.path.join(sd1,"test.txt")
with open(out_txt, 'w') as f:
    f.write('this is a line')
    
    
print('\n------\n')
out_txt_fullpath = os.path.abspath(out_txt)
print(f"wrote line of text to newly created {out_txt_fullpath}")