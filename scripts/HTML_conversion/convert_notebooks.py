import os
import datetime
import shutil
import re
import subprocess
import fileinput
import sys
import toc

p = re.compile("^\d{2}_")

cwd = os.getcwd()

stamp = datetime.datetime.now().strftime("%Y_%M_%d_%H:%M:%S")

docwd = os.path.join(cwd, "html")

template = os.path.join(cwd, "web.tpl")

if os.path.exists(docwd):
    shutil.rmtree(docwd)
    
os.mkdir(docwd)

ignore = [".git", ".ipynb_checkpoints", "scripts"]

def make_toc(wdir, relpath):
    def doc_path(i, chapter, j, section, k, notebook):
    
        chapter = chapter.replace(" ", "_")
        section = section.replace(" ", "_")
        notebook = notebook.replace(" ", "_")
    
        path = os.path.join(relpath, "{i:02d}_{chapter}/{j:02d}_{section}/{k:02d}_{notebook}.html")
    
        return path.format(i=i, j=j, k=k, chapter=chapter, section=section, notebook=notebook)
        
    cwd = os.getcwd()
    os.chdir(wdir)
    
    _toc = toc.get_toc()

    rtn = ""
    rtn += "<ul>"
    
    for i, chapter in enumerate(_toc):
        i += 1
        rtn += " <li>{0} - {1}".format(i, chapter)
        rtn += "  <ul>"
        for j, section in enumerate(_toc[chapter]):
            j += 1
            rtn += "   <li>{0} - {1}".format(j, section)
            rtn += "    <ul>"
            for k, notebook in enumerate(_toc[chapter][section]):
                k += 1
                path = doc_path(i, chapter, j, section, k, notebook)
                rtn += "      <li><a href={2}>{0} - {1}</a></li> ".format(k, notebook, path)
                
            rtn += "    </ul>"    
        rtn += "   </li>"
        rtn += "  </ul>"
        rtn += " </li>"
    rtn += "</ul>"      
    
    os.chdir(cwd)
    return rtn
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

        os.chdir(os.path.join(docwd, path))
        
        with open("web_changed.tpl", "w") as ofile:
            with fileinput.FileInput(template) as ifile:
                for line in ifile:
                    if line.strip() == "%%%%TOC_REPLACE%%%%":
                        ofile.write(make_toc(cwd, os.path.relpath(docwd)))
                    else:
                        ofile.write(line)
        
        for f in files:
            if not f.endswith(".ipynb"):
                shutil.copy(os.path.join(wd, path, f), ".")
            else:
                # convert notebook to HTML
                shutil.copy(os.path.join(wd, path, f), ".")
                
                subprocess.call(["jupyter", "nbconvert", f, "--to", "HTML", "--template", "web_changed.tpl"])
                
                # clean up
                os.remove(f)
        
        if os.path.exists(os.path.join(docwd, "web_changed.tpl")):
            os.remove(os.path.join(docwd, "web_changed.tpl"))
                
        os.chdir(wd)
        
        
                
finally:
    os.chdir(cwd)