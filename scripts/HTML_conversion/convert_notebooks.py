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
template2_header = os.path.join(cwd, "index_header.txt")
template2_footer = os.path.join(cwd, "index_footer.txt")

if os.path.exists(docwd):
	shutil.rmtree(docwd)
	
os.mkdir(docwd)

ignore = [".git", ".ipynb_checkpoints", "scripts"]
nbignore = ["index.txt"]

def make_toc(wdir, relpath):
	def doc_path(i, chapter, j=None, section=None, k=None, notebook=None):
	
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
				path = os.path.join(relpath, "{i:02d}_{chapter}/{j:02d}_{section}/")
				return path.format(i=i, j=j, chapter=chapter, section=section)
			else:
				path = os.path.join(relpath, "{i:02d}_{chapter}/")
				return path.format(i=i, chapter=chapter)
		
	cwd = os.getcwd()
	os.chdir(wdir)
	
	_toc = toc.get_toc()

	rtn = ""
	rtn += "<ul>"
	
	for i, chapter in enumerate(_toc):
		i += 1
		path = doc_path(i, chapter)
		rtn += " <li class=\"sep\"><a href={2}>{0} - {1}</a>".format(i, chapter, path)
		rtn += "  <ul>"
		for j, section in enumerate(_toc[chapter]):
			j += 1
			path = doc_path(i, chapter, j, section)
			rtn += "   <li class=\"sep\"><a href={2}>{0} - {1}</a>".format(j, section, path)
			rtn += "	<ul>"
			#for k, notebook in enumerate(_toc[chapter][section]):
			#	 k += 1
			#	 path = doc_path(i, chapter, j, section, k, notebook)
			#	 rtn += "	   <li><a href={2}>{0} - {1}</a></li> ".format(k, notebook, path)
			#	 
			rtn += "	</ul>"	  
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
			if f == "index.txt":
				with open("index.html", "w") as ofile:
					with fileinput.FileInput(template2_header) as ifile:
						for line in ifile:
							if line.strip() == "%%%%TOC_REPLACE%%%%":
								ofile.write(make_toc(cwd, os.path.relpath(docwd)))
							else:
								ofile.write(line)					
					with fileinput.FileInput(os.path.join(wd,path,f)) as ifile:
						for line in ifile:
							if line.strip() == "%%%%TOC_REPLACE%%%%":
								ofile.write(make_toc(cwd, os.path.relpath(docwd)))
							else:
								ofile.write(line)
					with fileinput.FileInput(template2_footer) as ifile:
						for line in ifile:
							ofile.write(line)					

		for f in files:
			if any(i in f for i in nbignore):
				continue
			
			if not f.endswith(".ipynb"):
				shutil.copy(os.path.join(wd, path, f), ".")
			else:
				# convert notebook to HTML
				shutil.copy(os.path.join(wd, path, f), ".")
				
				#subprocess.call(["jupyter", "nbconvert", f, "--to", "HTML", "--template", "web_changed.tpl"])
				subprocess.call(["jupyter-nbconvert-3.4", f, "--to", "HTML", "--template", "web_changed.tpl"])
				
				# clean up
				os.remove(f)
		
		if os.path.exists("web_changed.tpl"):
			os.remove("web_changed.tpl")
				
		os.chdir(wd)
		
		
				
finally:
	os.chdir(cwd)
