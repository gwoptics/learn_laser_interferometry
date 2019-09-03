import os
import datetime
import shutil
import re
import subprocess
import fileinput
import sys
import toc


clean_name = lambda x: x[3:].replace("_", " ").replace(".ipynb", "")

# Walk into directories in filesystem
# Ripped from os module and slightly modified
# for alphabetical sorting
#
def sortedWalk(top, topdown=True, onerror=None):
    from os.path import join, isdir, islink
 
    names = os.listdir(top)
    names.sort()
    dirs, nondirs = [], []
 
    for name in names:
        if isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
 
    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if not os.path.islink(path):
            for x in sortedWalk(path, topdown, onerror):
                yield x
    if not topdown:
        yield top, dirs, nondirs

def doc_path(relpath, i, chapter, j=None, section=None, k=None, notebook=None):

	chapter = chapter.replace(" ", "_")
	
	if section !=None:
		section = section.replace(" ", "_")
	if notebook !=None:
		notebook = notebook.replace(" ", "_")

	if notebook != None:
		path = os.path.join(relpath, "{i:02d}_{chapter}/{j:02d}_{section}/{k:02d}_{notebook}.html")
		return path.format(i=i, j=j, k=k, chapter=chapter, section=section, notebook=notebook)
	else:
		if section != None:
			path = os.path.join(relpath, "{i:02d}_{chapter}/{j:02d}_{section}/index.html")
			return path.format(i=i, j=j, chapter=chapter, section=section)
		else:
			path = os.path.join(relpath, "{i:02d}_{chapter}/index.html")
			return path.format(i=i, chapter=chapter)
			
def make_toc(wdir, relpath, _toc):
	
	rtn = ""
	rtn += "<ul><li class=\"sep\"><a title='Online material to learn laser interferometry with Finesse' href='{0}/index.html'>Learn Home</a></li>".format(relpath)
	
	for i, chapter in enumerate(_toc):
		i += 1
		
		path = doc_path(relpath, i, chapter)
		rtn += " <li class=\"sep\"><a href='{2}'>{0} {1}</a>".format(i, chapter, path)
		rtn += "  <ul>"
	
		for j, section in enumerate(_toc[chapter]):
			j += 1
			
			path = doc_path(relpath, i, chapter, j, section)
			rtn += "   <li class=\"sep\"><a href='{3}'>{0}.{1} {2}</a></li>".format(i, j, section, path)
			
		rtn += "  </ul>"		
		rtn += " </li>"
	
	rtn += "</ul>"		
	
	return rtn
	
def make_chapter_toc(_chapter, wdir, relpath, _toc):
	rtn = ""
	
	for i, chapter in enumerate(_toc):
		i += 1

		if chapter == _chapter:
			rtn += "<h2>{0} {1}</h2>".format(i,chapter)
			rtn += "<ul style=\"list-style-type: none;\">"
			for j, section in enumerate(_toc[chapter]):
				j += 1
			
				path = doc_path(relpath, i, chapter, j, section)
				rtn += "   <li class=\"sep\"><a href='{3}'>{0}.{1} {2}</a></li>".format(i, j, section, path)
			
	
	rtn += "</ul>"		
	
	return rtn
	
	
def make_section_toc(_chapter, _section, wdir, relpath, _toc):
	rtn = ""
	
	for i, chapter in enumerate(_toc):
		i += 1
		
		if chapter == _chapter:
			rtn += "<h2>{0} {1}</h2>".format(i,chapter)
			for j, section in enumerate(_toc[chapter]):
				j += 1
				
				if section == _section:
					rtn += "<h3>{0}.{1} {2}</h3>".format(i,j,section)
					rtn += "<ul style=\"list-style-type: none;\">"
					for k, notebook in enumerate(_toc[chapter][section]):
						k += 1
						
						path = doc_path(relpath, i, chapter, j, section, k, notebook)
						rtn += "   <li class=\"sep\"><a href='{4}'>{0}.{1}.{2} {3}</a></li>".format(i,j,k, notebook, path)
						
					
			
	
	rtn += "</ul>"		
	
	return rtn
	


p = re.compile("^\d{2}_")

cwd = os.getcwd()

stamp = datetime.datetime.now().strftime("%Y_%M_%d_%H:%M:%S")

docwd = os.path.join(cwd, "html")

template = os.path.join(cwd, "web.tpl")
template2_header = os.path.join(cwd, "index_header.txt")
template2_footer = os.path.join(cwd, "index_footer.txt")

if os.path.exists(docwd):
	shutil.rmtree(docwd)
	
os.mkdir(docwd)


ignore = [".git", ".ipynb_checkpoints", "scripts"]
	
try:
	os.chdir("../../")

	_toc = toc.get_toc()
	
	wd = os.getcwd()
	shutil.copytree(os.path.join(wd,"images"), os.path.join(docwd,"images"))
	
	for (path, folders, files) in os.walk("."):
		#for (path, folders, files) in sortedWalk("."):
		folders.sort()
		files.sort()
		if any(i in path for i in ignore):
			continue
		(parent, curfolder) = os.path.split(path)
		parfolder = os.path.split(parent)[1]
		print("** Current Folder : {}".format(curfolder))
		if parfolder == ".":
			cursection = None
			curchapter = clean_name(curfolder)
		else:
			cursection = clean_name(curfolder)
			curchapter = clean_name(parfolder)
			
		if not p.match(curfolder) and curfolder != ".":
			continue
		
		if not os.path.exists(os.path.join(docwd, path)):
			os.mkdir(os.path.join(docwd, path))

		os.chdir(os.path.join(docwd, path))
		
		with open("web_changed.tpl", "w") as ofile:
			with fileinput.FileInput(template) as ifile:
				for line in ifile:
					if line.strip() == "%%%%TOC_REPLACE%%%%":
						ofile.write(make_toc(cwd, os.path.relpath(docwd), _toc))
					elif line.strip() == "%%%%LEARN_REPLACE%%%%":
						ofile.write("<li><a title='Online material to learn laser interferometry with Finesse' href='{0}/index.html'>Learn</a>\n".format(os.path.relpath(docwd)))
					else:
						ofile.write(line)
		
		for f in files:
			if f.startswith("."):
				continue
				
			if f == "index.txt" and curfolder != ".":
				with open("index.html", "w") as ofile:
					with fileinput.FileInput(template2_header) as ifile:
						for line in ifile:
							if line.strip() == "%%%%TITLE_REPLACE%%%%":
								if cursection is None:
									if curchapter is None:
										ofile.write(" ")
									else:
										ofile.write("{0} ".format(curchapter))
								else:
									ofile.write("{0} ".format(cursection))
							elif line.strip() == "%%%%TOC_REPLACE%%%%":
								ofile.write(make_toc(cwd, os.path.relpath(docwd), _toc))
							elif line.strip() == "%%%%LEARN_REPLACE%%%%":
								ofile.write("<li><a title='Online material to learn laser interferometry with Finesse' href='{0}/index.html'>Learn</a>".format(os.path.relpath(docwd)))
							else:
								ofile.write(line)	
												
					with fileinput.FileInput(os.path.join(wd,path,f)) as ifile:
						for line in ifile:
							if line.strip() == "%%%%TOC_REPLACE%%%%":
								if cursection is None:
									ofile.write(make_chapter_toc(curchapter, cwd, os.path.relpath(docwd), _toc))
								else:
									ofile.write(make_section_toc(curchapter, cursection, cwd, os.path.relpath(docwd), _toc))
							else:
								ofile.write(line)
								
					with fileinput.FileInput(template2_footer) as ifile:
						for line in ifile:
							ofile.write(line)
			
			elif f == "main.txt" and curfolder == ".":
				
				with open("index.html", "w") as ofile:
					with fileinput.FileInput(template2_header) as ifile:
						for line in ifile:
							if line.strip() == "%%%%TITLE_REPLACE%%%%":
								ofile.write("Main ")				
							elif line.strip() == "%%%%TOC_REPLACE%%%%":
								ofile.write(make_toc(cwd, os.path.relpath(docwd), _toc))
							elif line.strip() == "%%%%LEARN_REPLACE%%%%":
								ofile.write("<li><a title='Online material to learn laser interferometry with Finesse' href='{0}/index.html'>Learn</a>".format(os.path.relpath(docwd)))
							else:
								ofile.write(line)	
						
					with fileinput.FileInput(os.path.join(wd,path,f)) as ifile:
						for line in ifile:
							if line.strip() == "%%%%TOC_REPLACE%%%%":	
								ofile.write(make_toc(cwd, os.path.relpath(docwd), _toc))
							else:
								ofile.write(line)
		
					with fileinput.FileInput(template2_footer) as ifile:
						for line in ifile:
							ofile.write(line)
							
			elif not f.endswith(".ipynb") and curfolder != ".":
				shutil.copy(os.path.join(wd, path, f), ".")
				
			elif curfolder != ".":
				# convert notebook to HTML
				shutil.copy(os.path.join(wd, path, f), ".")
				
				try:
					subprocess.call(["jupyter", "nbconvert", f, "--to", "HTML", "--template", "web_changed.tpl"])
				except FileNotFoundError:
					subprocess.call(["jupyter-nbconvert-3.4", f, "--to", "HTML", "--template", "web_changed.tpl"])
				
				# clean up
				os.remove(f)
		
		if os.path.exists("web_changed.tpl"):
			os.remove("web_changed.tpl")
				
		os.chdir(wd)
		
		
				
finally:
	os.chdir(cwd)
