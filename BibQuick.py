# BibQuick v0.1.0 (Aug 26, 2024)
# Ryo Fukushima
#
import bibtexparser
import copy
import re
import sys
import os
import configparser

##########
#BibtexLocation = "bibtexlist/list_20240821.bib"
#CitationStyle = "A,s,Y,ps,T,ps,J,cs,V,cs,P,cs,U,p"
#AuthorStyle = "ScsI,cs,ps,p,& "
#YearPar = yes
#JournalAbb = False
#VolumeStyle = "V"

##########

config_ini = configparser.ConfigParser()
path = os.path.join(os.path.dirname(__file__), 'BibQuickParams.ini')
config_ini.read(path, encoding='utf-8')

BibtexLocation = config_ini["CurrentParameters"]["BibtexLocation"]
CitationStyle = config_ini["CurrentParameters"]["CitationStyle"]
AuthorStyle = config_ini["CurrentParameters"]["AuthorStyle"]
YearPar = config_ini["CurrentParameters"]["YearPar"]
TemplateName = config_ini["CurrentParameters"]["Template"]
##########

SignConverter = {"s": " ", "p": ".", "c": ",", "cl": ":", "ps": ". ", "cs": ", ", "cls": ": ", "n": "", 
                 "ap": "&", "a": "and", "aps": "& ", "as": "and "}
AuthorStyle_list = AuthorStyle.split(",")

##########
# open the bibtex file (as dict)
print("============================================================")
print("            BibQuick v0.1.0 by Ryo Fukushima")
print("============================================================")
print("Loading database...")
with open(BibtexLocation) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# make a list from dict
bib_datalist = list(bib_database.entries_dict.values())

print("Template: ", TemplateName)

# make a list of authors' names and years
names = []
years = []
bib_datalist_modified = []
for i in range(len(bib_datalist)):

    if ("author" in bib_datalist[i] and
        "year" in bib_datalist[i] and 
        bib_datalist[i]["year"].isdigit() == True and
        "title" in bib_datalist[i] and 
        "journal" in bib_datalist[i]):
        
        bib_datalist_modified.append(bib_datalist[i])
        names.append(bib_datalist[i]["author"].split(" and "))
        years.append(int(bib_datalist[i]["year"]))
   
# split names into firstnames and surnames
surnames = copy.deepcopy(names)
firstnames = copy.deepcopy(names)

for i in range(len(names)):
    for j in range(len(names[i])):

        if ", " in names[i][j] and "," in names[i][j]:
            surnames[i][j] = names[i][j].split(", ")[0]
            firstnames[i][j] = names[i][j].split(", ")[1]
        elif "," in names[i][j]:
            surnames[i][j] = names[i][j].split(",")[0]
            firstnames[i][j] = names[i][j].split(",")[1]
        elif " " in names[i][j]:
            firstnames[i][j] = " ".join(names[i][j].split(" ")[0:-1])
            surnames[i][j] = names[i][j].split(" ")[-1]
        else:
            firstnames[i][j] == names[i][j]
            surnames[i][j] == names[i][j]
         
# convert firstnames into initials 
firstnames_I = copy.deepcopy(firstnames)
spacelocation = []
divide = AuthorStyle_list[2]
endsign = AuthorStyle_list[3]

for i in range(len(names)):
    for j in range(len(names[i])):
        firstnames_I[i][j] = firstnames[i][j][0]

        spacelocation = [m.start() for m in re.finditer(" ", firstnames[i][j])]
        if len(spacelocation) > 0:
            for k in range(len(spacelocation)):
                firstnames_I[i][j] = firstnames_I[i][j] + SignConverter[divide] + firstnames[i][j][spacelocation[k] + 1]
        firstnames_I[i][j] += SignConverter[endsign]


# make a list of in-line citation and insert &
InLineCitations = []
surnames_and = copy.deepcopy(surnames)
firstnames_and = copy.deepcopy(firstnames)
firstnames_I_and = copy.deepcopy(firstnames_I)
andsign = AuthorStyle_list[4]

for i in range(len(names)):
    if len(names[i]) > 2:
        InLineCitations.append(surnames[i][0] + "+" + str(years[i]))
        surnames_and[i][-1] = SignConverter[andsign] + surnames_and[i][-1]
        firstnames_and[i][-1] = SignConverter[andsign] + firstnames_and[i][-1]
        firstnames_I_and[i][-1] = SignConverter[andsign] + firstnames_I_and[i][-1]

    elif len(names[i]) == 2:
        InLineCitations.append(surnames[i][0] + "&" + surnames[i][1] + str(years[i]))
        surnames_and[i][-1] = SignConverter[andsign] + surnames_and[i][-1]
        firstnames_and[i][-1] = SignConverter[andsign] + firstnames_and[i][-1]
        firstnames_I_and[i][-1] = SignConverter[andsign] + firstnames_I_and[i][-1]

    else:
        InLineCitations.append(surnames[i][0] + str(years[i]))
#%%
# make author expression
SF, SsF, SI, SsI, ScI, ScsI, ScsIp = [], [], [], [], [], [], []
FsS, IsS = [], []


for i in range(len(names)):
    SF.append([x + y for (x, y) in zip(surnames_and[i], firstnames[i])])
    SsF.append([x + " " + y for (x, y) in zip(surnames_and[i], firstnames[i])])
    SI.append([x + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    SsI.append([x + " " + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScI.append([x + "," + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScsI.append([x + ", " + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScsIp.append([x + ", " + y + "." for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    FsS.append([x + " " + y for (x, y) in zip(firstnames_and[i], surnames[i])])
    IsS.append([x + " " + y for (x, y) in zip(firstnames_I_and[i], surnames[i])])


##########
# StyleConverter
CitationStyleConverter = {"T": "title", "J": "journal", "V": "volume", "P":"pages", "U": "url"}
AuthorStyleConverter = {
    "SF": SF,
    "SsF": SsF,
    "SI": SI,
    "SsI": SsI,
    "ScI": ScI,
    "ScsI": ScsI,
    "ScsIp": ScsIp,
    "FsS": FsS,
    "IsS": IsS,
}

##########

def CitationExport(formattedauthor, **args): # args == bib_datalist_modified[i]

    CitationStyle_list = CitationStyle.split(",")

    result = []

    for i in range(len(CitationStyle_list)):
        if CitationStyle_list[i] == "A":
            result.append(formattedauthor)
        
        if CitationStyle_list[i] == "Y":
            if YearPar == "yes":
                result.append("(" + args["year"] + ")")
            else:
                result.append(args["year"])

        if CitationStyle_list[i] in CitationStyleConverter:
            if CitationStyleConverter[CitationStyle_list[i]] in args:
                result.append(args[CitationStyleConverter[CitationStyle_list[i]]])
            else: 
                result.append("")

        if CitationStyle_list[i] in SignConverter:
            result.append(SignConverter[CitationStyle_list[i]])

    return "".join(result)


#%% Search matched papers and export the citation

counter = 0

while counter < 1:
    SearchWord = input("\nType the reference name\n(ex. Surname+2024/Surname&Surname2024/Surname2024)\n(type 'e' to exit): ")

    if SearchWord == "e":
        sys.exit()

    CitationOutputs = []

    for i in range(len(names)):
        if InLineCitations[i] == SearchWord:
            Output = CitationExport(SignConverter[AuthorStyle_list[1]].join(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])
            CitationOutputs.append(Output)

    if not CitationOutputs:
        print("\nNo matched results")

    else:
        print(*CitationOutputs, sep = "\n")



# %%
