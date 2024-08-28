#%%
# BibQuick v0.2.0 (Aug 28, 2024)
# Ryo Fukushima
#
import bibtexparser
import copy
import re
import sys
import os
import configparser
import datetime

##########
#BibtexLocation = "bibtexlist/list_20240821.bib"
#CitationStyle = "A,s,Y,ps,T,ps,J,cs,V,cs,P,cs,U,p"
#AuthorStyle = "ScsI,cs,ps,p,& "
#YearPar = yes
#TemplateName = Nature
#ExportOption = no
#PlainConvert = yes


##########

config_ini = configparser.ConfigParser()
path = os.path.join(os.path.dirname(__file__), "BibQuickParams.ini")
config_ini.read(path, encoding="utf-8")

BibtexLocation = config_ini["CurrentParameters"]["BibtexLocation"]
ExportOption = config_ini["CurrentParameters"]["Export"]
CitationStyle = config_ini["CurrentParameters"]["CitationStyle"]
AuthorStyle = config_ini["CurrentParameters"]["AuthorStyle"]
YearPar = config_ini["CurrentParameters"]["YearPar"]
TemplateName = config_ini["CurrentParameters"]["Template"]
PlainConvert = config_ini["CurrentParameters"]["PlainConvert"]

##########

SignConverter = {"s": " ", "p": ".", "c": ",", "cl": ":", "ps": ". ", "cs": ", ", "cls": ": ", "n": "", 
                 "ap": "&", "a": "and", "aps": "& ", "as": "and "}
AuthorStyle_list = AuthorStyle.split(",")

PlainConverter = {"--": "–", '\\"o': "ö", "\\'e": "é", "\\'a": "á", "\\v c": "č", '\\"u': "ü", '\\"a': "ä"}

##########
# open the bibtex file (as dict)
print("============================================================")
print("             BibQuick v0.2.0 by Ryo Fukushima")
print("============================================================")
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print(timestamp)
print("Loading database......")
with open(BibtexLocation) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# make a list from dict
bib_datalist = list(bib_database.entries_dict.values())

print("Template:", TemplateName)

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

if PlainConvert == "yes":
    for i in range(len(names)):
        for j in range(len(names[i])):

            names[i][j] = names[i][j].replace("{", "")
            names[i][j] = names[i][j].replace("}", "")
            
            for bf, af in PlainConverter.items():
                names[i][j] = names[i][j].replace(bf, af)


print("%i/%i items read"% (len(bib_datalist_modified), len(bib_datalist)))

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

        firstnames[i][j] = firstnames[i][j].replace("-", " ")

        firstnames[i][j] = re.sub("([A-Z])([A-Z])","\\1 \\2", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3 \\4", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3 \\4 \\5", firstnames[i][j])

        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.","\\1 \\2", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3 \\4", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3 \\4 \\5", firstnames[i][j])
         
# convert firstnames into initials 
firstnames_I = copy.deepcopy(firstnames)
spacelocation = []
divide = AuthorStyle_list[2]
endsign = AuthorStyle_list[3]

for i in range(len(names)):
    for j in range(len(names[i])):
        
        firstnames_I[i][j] = firstnames[i][j][0].upper()

        spacelocation = [m.start() for m in re.finditer(" ", firstnames[i][j])]
        if len(spacelocation) > 0:
            for k in range(len(spacelocation)):
                firstnames_I[i][j] = firstnames_I[i][j] + SignConverter[divide] + firstnames[i][j][spacelocation[k] + 1].upper()
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
CitationStyleConverter = {"T": "title", "J": "journal", "V": "volume", "P":"pages", "U": "url", "D": "doi"}
# A, Y, DL is implemented separately below

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

        if CitationStyle_list[i] == "DL":
            if ("doi" in args) and ("doi:" not in args["doi"]) and ("https://doi.org/" not in args["doi"]):
                result.append("https://doi.org/" + args["doi"])
            elif ("doi" in args) and ("https://doi.org/" in args["doi"]):
                result.append(args["doi"])
            elif ("doi" in args) and ("doi:" in args["doi"]):
                result.append("https://doi.org/" + args["doi"].replace("doi:", ""))
            else:
                result.append("")

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
outputpath = os.path.join(os.path.dirname(__file__), "%s.txt"%timestamp)

if ExportOption == "yes":
    file = open(outputpath, 'a')

while counter < 1:
    SearchWord = input("\nType the reference name\n(ex. Surname+2024/Surname&Surname2024/Surname2024)\n(type 'e' to exit; type 'list' to display database): ")

    if SearchWord == "e":
        if ExportOption == "yes":
            file.close()
        sys.exit()

    if SearchWord == "list":
        print(*InLineCitations)
        continue

    CitationOutputs = []

    for i in range(len(names)):
        if InLineCitations[i] == SearchWord:
            Output = CitationExport(SignConverter[AuthorStyle_list[1]].join(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])

            if PlainConvert == "yes":
                
                Output = Output.replace("{", "")
                Output = Output.replace("}", "")
                for bf, af in PlainConverter.items():
                     Output = Output.replace(bf, af)

            CitationOutputs.append(Output + "\n")

    if not CitationOutputs:
        print("\nNo matched results")

    else:
        print(*CitationOutputs)

        if ExportOption == "yes":
            file.writelines(CitationOutputs)

    




# %%
