def get_toc():
    import re
    import os
    import collections
    from collections import OrderedDict
    from os import path
    
    os.chdir("../../") # relative path to start of document
    
    clean_name = lambda x: x[3:].replace("_", " ").replace(".ipynb", "")
    
    # check first two are digits
    p = re.compile("^\d{2}_")

    toc = OrderedDict()

    chapter_paths = [folder for folder in os.listdir() if p.match(folder)]

    for chapter in chapter_paths:
        os.chdir(chapter)
    
        cname = clean_name(chapter)
    
        toc[cname] = OrderedDict()
    
        section_paths = [folder for folder in os.listdir() if p.match(folder)]
    
        for section in section_paths:
            os.chdir(section)
        
            sname = clean_name(section)
        
            toc[cname][sname] = [clean_name(folder) for folder in os.listdir() if p.match(folder)]
        
            os.chdir("..")
    
        os.chdir("..")
        
    return toc
    
def print_github_toc(toc):    
    def github_path(i, chapter, j, section, k, notebook):
    
        chapter = chapter.replace(" ", "_")
        section = section.replace(" ", "_")
        notebook = notebook.replace(" ", "_")
    
        path = "https://github.com/gwoptics/learn_laser_interferometry/blob/master/{i:02d}_{chapter}/{j:02d}_{section}/{k:02d}_{notebook}.ipynb"
    
        return path.format(i=i, j=j, k=k, chapter=chapter, section=section, notebook=notebook)
    
    for i, chapter in enumerate(toc):
        i += 1
        print("* {0} - {1}".format(i, chapter))
    
        for j, section in enumerate(toc[chapter]):
            j += 1
            print("  * {0}.{1} - {2}".format(i,j,section))
        
            for k, notebook in enumerate(toc[chapter][section]):
                k += 1
                path = github_path(i, chapter, j, section, k, notebook)
                print("    * {0}.{1}.{2} - [{3}]({4})".format(i,j,k,notebook,path))
            
            
            
if __name__ == "__main__":
    toc = get_toc()
    print_github_toc(toc)