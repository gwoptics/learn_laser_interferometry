import os
import datetime
import shutil
import re
import subprocess

p = re.compile("^\d{2}_")

cwd = os.getcwd()

stamp = datetime.datetime.now().strftime("%Y_%M_%d_%H:%M:%S")

docwd = os.path.join(cwd, "doc")

template = os.path.join(cwd, "web.tpl")

if os.path.exists(docwd):
    shutil.rmtree(docwd)
    
os.mkdir(docwd)

ignore = [".git", ".ipynb_checkpoints", "scripts"]

try:
    os.chdir("../../")

    wd = os.getcwd()
    
    for (path, folders, files) in os.walk("."):
        
        if any(i in path for i in ignore):
            continue
    
        curfolder = os.path.split(path)[1]
        
        if not p.match(curfolder):
            continue
        
        os.mkdir(os.path.join(docwd, path))
        
        for f in files:
            if not f.endswith(".ipynb"):
                shutil.copy(os.path.join(path, f), os.path.join(docwd, path, f))
            else:
                # convert notebook to HTML
                shutil.copy(os.path.join(path, f), os.path.join(docwd, path, f))
                shutil.copy(template, os.path.join(docwd, path, "web.tpl"))
                
                os.chdir(os.path.join(docwd, path))
                subprocess.call(["jupyter", "nbconvert", f, "--to", "HTML", "--template", "web.tpl"])
                os.chdir(wd)
                
                # clean up
                os.remove(os.path.join(docwd, path, f))
                os.remove(os.path.join(docwd, path, "web.tpl"))
        
        

finally:
    os.chdir(cwd)