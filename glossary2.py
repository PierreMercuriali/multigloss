"""
    glossary.py
    Glossary system with hyperlinks and multiple definitions
"""
import random

def close(w1, w2, threshold):
    if w1==w2:
        return True
    if w1==w2+"s" or w2==w1+"s":
        return True
    return len(set(w1+w2))/len(w1+w2) < threshold

def addToDict(d, e, c, s):
    #dictionary, entry, content, source
    if not e=="":
        if e in d.keys():        
            print("\tNew definition:", e)
            d[e].append([c, s])
        else:
            d[e] = [[c, s]]
glossary = {}

def cleanup(w):
    return w.lower().rstrip()

def filtre(words):#not super efficient but eh
    kept = {}
    for w in words:
        if w in kept.keys():
            kept[w].append(w)
        else:
            kept[w] = [w]
    for w in words:
        for k in kept.keys():
            if w in k:
                kept[k].append(w)
    classes = []
    for k in kept.keys():
        classes.append(sorted(kept[k])[0])
    return set(classes)


print("Loading P. Thagard's...")
with open("cognition1.txt", "r", encoding="utf-8") as f:
    data = [l.rstrip() for l in f.readlines() if len(l)>3]
for l in data:
    addToDict(glossary, cleanup(l.split("--")[0]), ' '.join(l.split("--")[1:]), " P. Thagard, Mind: Introduction to Cognitive Science, second edition, MIT Press, 2005")
print("\t", len(glossary.keys()), "entries now.")


print("Loading DANA's...")
with open("cognition2.txt", "r", encoding="utf-8") as f:
    data = [l.rstrip() for l in f.readlines() if len(l)>3]
for l in data:
    addToDict(glossary, cleanup(l.split(":")[0]), ': '.join(l.split(":")[1:]), "https://www.dana.org/explore-neuroscience/brain-basics/key-brain-terms-glossary/")
print("\t", len(glossary.keys()), "entries now.")

print("Loading SharpBrains's...")
with open("cognition3.txt", "r", encoding="utf-8") as f:
    data = [l.rstrip() for l in f.readlines() if len(l)>3]
for l in data:
    addToDict(glossary, cleanup(l.split(":")[0]), ': '.join(l.split(":")[1:]), "https://sharpbrains.com/resources/glossary")
print("\t", len(glossary.keys()), "entries now.")

print("Loading Richmond's...")
with open("cognition4.txt", "r", encoding="utf-8") as f:
    data = [l.rstrip() for l in f.readlines() if len(l)>3]
for l in data:
    addToDict(glossary, cleanup(l.split(":")[0]), ': '.join(l.split(":")[1:]), "https://web.archive.org/web/20090415100452/http://facultystaff.richmond.edu/~pli/teaching/psy333/glossary.html")
print("\t", len(glossary.keys()), "entries now.")

print("Loading Dawson's...")
with open("cognition5.txt", "r", encoding="utf-8") as f:
    data = [l.rstrip() for l in f.readlines() if len(l)>3]
for l in data:
    addToDict(glossary, cleanup(l.split("--")[0]), ' '.join(l.split("--")[1:]), "http://penta.ufrgs.br/edu/telelab/3/entries.htm")
print("\t", len(glossary.keys()), "entries now.")



#TODO: extract core concepts



print("Saving as html...")
res = """
<HTML>
    <HEAD>
        <META CHARSET="UTF-8">
        <meta http-equiv="Content-type" content="text/html; charset=UTF-8">
        <TITLE>COGNITION GLOSSARY</TITLE>
        <LINK REL="stylesheet" HREF="style.css">
    </HEAD>
    <BODY>
    
    <div class="content">
        <h1>Cognition glossary</h1>
        
        
"""
#filter to avoid double links
keys = filtre([w.lower() for w in glossary.keys()])
i = 0
for entry in sorted(glossary.keys()):
    i+=1
    res+="<div class=\"entry\">"
    definition_list = ''
    for definition in glossary[entry]:
        to_save = definition[0]
        saved_keys = ""
        for w in keys:
            if w in to_save and len(w)>1 and not w in saved_keys:
                saved_keys+=w
                s = "<a href=\"#" + w.lower() + "\">" + w + "</a>" 
                to_save = s.join(to_save.split(w))
        definition_list+=to_save+"<br><div class=\"source\">"+definition[1]+"</div><br>\n"
    
    res+="<p id=\""+entry+"\"> <div class=\"entrytitle\">" + entry.upper() + "<div style=\"float:right;\">" + str(i) + " </div></div><br>" + definition_list + "</p><br><br></div>\n\n"

res +="""

</div>
    
</BODY>
</HTML>
"""

with open("index"+''.join([random.choice("1234567890") for i in range(16)])+".html", "w", encoding="utf-8") as f:
    f.write(res)
