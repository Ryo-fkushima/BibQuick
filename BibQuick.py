#%%
# BibQuick v1.0.0-beta2 (Sep 2, 2024)
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
ExportOption = config_ini["CurrentParameters"]["InteractiveExport"]
CitationStyle = config_ini["CurrentParameters"]["CitationStyle"]
AddLetters = config_ini["CurrentParameters"]["AddLetters"] 
AuthorStyle = config_ini["CurrentParameters"]["AuthorStyle"]
ManyAuthors = config_ini["CurrentParameters"]["ManyAuthors"]
ManyAuthorsOption = config_ini["CurrentParameters"]["ManyAuthorsOption"]
EtAlExpression = config_ini["CurrentParameters"]["EtAlExpression"]
YearPar = config_ini["CurrentParameters"]["YearPar"]
NoPar = config_ini["CurrentParameters"]["NoPar"]
TemplateName = config_ini["CurrentParameters"]["Template"]
PlainConvert = config_ini["CurrentParameters"]["PlainConvert"]


BatchConvert = config_ini["CurrentParameters"]["BatchConvert"]
TxtFileLocation = config_ini["CurrentParameters"]["TxtFileLocation"]
AlphabeticalSorting = config_ini["CurrentParameters"]["AlphabeticalSorting"]

##########

SignConverter = {"s": " ", "p": ".", "c": ",", "cl": ":", "ps": ". ", "cs": ", ", "cls": ": ", "n": "", "sc": ";", "scs": "; ",
                 "q": "'", "dq": '"',
                 "ap": "&", "a": "and", "aps": "& ", "as": "and "}
AuthorStyle_list = AuthorStyle.split(",")
ManyAuthorsOption_list = ManyAuthorsOption.split(",")
AddLetters_list = AddLetters.split(",")

PlainConverter = {"--": "–", '\\"o': "ö", "\\'e": "é", "\\'a": "á", "\\v c": "č", '\\"u': "ü", '\\"a': "ä",
                  "\\v s": "š", "\\v r": "ř", "\\'\\i": "í","\\'u": "ú", "\\'o": "ó", "\\o":"ø", '\\"\\i': "ï", "\\aa": "å"}

##########
# open the bibtex file (as dict)
print("============================================================")
print("                BibQuick v1.0.0-beta2 by RF")
print("============================================================")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
print("Session No. " + timestamp)
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
        "journal" in bib_datalist[i]):
        
        bib_datalist_modified.append(bib_datalist[i])
        #names.append(bib_datalist[i]["author"].split(" and "))
        bib_datalist[i]["author"] = " ".join(bib_datalist[i]["author"].split())
        names.append(bib_datalist[i]["author"].split(" and "))
        years.append(int(bib_datalist[i]["year"]))

if PlainConvert == "yes":

    for i in range(len(names)):
        for j in range(len(names[i])):

            names[i][j] = names[i][j].replace("{", "")
            names[i][j] = names[i][j].replace("}", "")
            
            for bf, af in PlainConverter.items():
                names[i][j] = names[i][j].replace(bf, af)

print("%i/%i items read from the database"% (len(bib_datalist_modified), len(bib_datalist)))

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


        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3 \\4 \\5", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3 \\4", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])","\\1 \\2", firstnames[i][j])
        
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3 \\4 \\5", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3 \\4", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.","\\1 \\2", firstnames[i][j])
        
         
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

    InLineCitations[i] = InLineCitations[i].lower()
    InLineCitations[i] = InLineCitations[i].replace(" ","")
                 


# make author expression
SsF, ScsF, SsI, ScsI = [], [], [], []
FsS, FcsS, IsS, IcsS = [], [], [], []


for i in range(len(names)):
    
    SsF.append([x + " " + y for (x, y) in zip(surnames_and[i], firstnames[i])])
    SsI.append([x + " " + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScsI.append([x + ", " + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScsF.append([x + ", " + y for (x, y) in zip(surnames_and[i], firstnames[i])])
    FsS.append([x + " " + y for (x, y) in zip(firstnames_and[i], surnames[i])])
    FcsS.append([x + ", " + y for (x, y) in zip(firstnames_and[i], surnames[i])])
    IsS.append([x + " " + y for (x, y) in zip(firstnames_I_and[i], surnames[i])])
    IcsS.append([x + ", " + y for (x, y) in zip(firstnames_I_and[i], surnames[i])])


##########
# StyleConverter
CitationStyleConverter = {"T": "title", "J": "journal", "V": "volume", "P":"pages", "U": "url", "D": "doi"}
# A, Y, N, DD, DL is implemented separately below

AuthorStyleConverter = {
    "SsF": SsF,
    "ScsF": ScsF,

    "SsI": SsI,
    "ScsI": ScsI,
    
    "FsS": FsS,
    "FcsS": FcsS,

    "IsS": IsS,
    "IcsS": IcsS,
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

        if CitationStyle_list[i] == "N":
            if ("number" in args) and (NoPar == "yes"):
                result.append("(" + args["number"] + ")")
            elif ("number" in args):
                result.append(args["number"])
            else:
                result.append("")

        if CitationStyle_list[i] == "DD":
            if ("doi" in args) and ("doi:" not in args["doi"]) and ("https://doi.org/" not in args["doi"]):
                result.append(args["doi"])
            elif ("doi" in args) and ("https://doi.org/" in args["doi"]):
                result.append(args["doi"].replace("https://doi.org/",""))
            elif ("doi" in args) and ("doi:" in args["doi"]):
                result.append(args["doi"].replace("doi:", ""))
            else:
                result.append("")

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

        if CitationStyle_list[i].isdigit() == True:
            result.append(AddLetters_list[int(CitationStyle_list[i])])

    return "".join(result)



def AuthorFormat(listofname):

    formatresult = []

    if ManyAuthors == "yes":
        if len(listofname) > int(ManyAuthorsOption_list[0]):
            formatresult = SignConverter[AuthorStyle_list[1]].join(listofname[0:int(ManyAuthorsOption_list[1])])
            formatresult += str(EtAlExpression)
        
            if int(ManyAuthorsOption_list[2]) == 1:
                formatresult += listofname[-1]
                formatresult = formatresult.replace(SignConverter[andsign], "")

        else:

            formatresult = SignConverter[AuthorStyle_list[1]].join(listofname)

    else:
        #formatresult = SignConverter[AuthorStyle_list[1]].join(AuthorStyleConverter[AuthorStyle_list[0]][i])
        formatresult = SignConverter[AuthorStyle_list[1]].join(listofname)

    return formatresult




#%% Search matched papers and export the citation

outputpath = os.path.join(os.path.dirname(__file__), "%s.txt"%timestamp)

if BatchConvert == "yes":
    print("----------------------------")
    print("       Batch convert")
    print("----------------------------")

    ConvertSource = open(TxtFileLocation, "r", encoding="utf-8")

    ConvertSource_list = re.findall(r"[a-zß-ÿĀ-ſ]+\d+|[a-zß-ÿĀ-ſ]+&[a-zß-ÿĀ-ſ]+\d+|[a-zß-ÿĀ-ſ]+\+\d+", ConvertSource.read().lower())

    if AlphabeticalSorting == "yes":
        ConvertSource_list = sorted(ConvertSource_list)


#%%
    print("%i items read as input"% len(ConvertSource_list))

    print("Converting......\n")

    CitationOutputs = []

    SuccessCounter = 0
    SubCounter = 0
    HowManyAuthors = 0

    for j in range(len(ConvertSource_list)):
        
        for i in range(len(names)):
            if InLineCitations[i] == ConvertSource_list[j]:
                #Output = CitationExport(SignConverter[AuthorStyle_list[1]].join(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])
                Output = CitationExport(AuthorFormat(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])

                if PlainConvert == "yes":
                    
                    Output = Output.replace("\{", "@lp")
                    Output = Output.replace("\}", "@rp")
                    Output = Output.replace("{", "")
                    Output = Output.replace("}", "")
                    Output = Output.replace("$", "")
                    Output = Output.replace("\mathrm", "")
                    Output = Output.replace("\\rm", "")

                    Output = Output.replace("@lp", "{")
                    Output = Output.replace("@rp", "}")

                    for bf, af in PlainConverter.items():
                        Output = Output.replace(bf, af)

                CitationOutputs.append(Output + "\n")
                SubCounter += 1

        if SubCounter > 0:
            SuccessCounter += 1
            print(ConvertSource_list[j].lower() + ": " + str(SubCounter))
        else:
            print(ConvertSource_list[j].lower() + "--------------------------> Not found")

        SubCounter = 0

    print("\n%i/%i items are successfully converted"% (SuccessCounter, len(ConvertSource_list)))

    file = open(outputpath, 'a')
    file.writelines(CitationOutputs)
    file.close()



#%%
else:

    print("----------------------------")
    print("      Interactive mode")
    print("----------------------------")

    if ExportOption == "yes":
        file = open(outputpath, 'a')

    while True:
        SearchWord = input("Type the reference name (case insensitive)\nex. surname+2024/surname&surname2024/surname2024\n(type 'e' to exit; type 'list' to display database): ")

        if SearchWord.lower() == "e":
            if ExportOption == "yes":
                file.close()
            sys.exit()

        if SearchWord.lower() == "list":
            
            print(*sorted(InLineCitations))
           
            continue

        CitationOutputs = []

        for i in range(len(names)):
            if InLineCitations[i] == SearchWord.lower():
                #Output = CitationExport(SignConverter[AuthorStyle_list[1]].join(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])
                Output = CitationExport(AuthorFormat(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])

                if PlainConvert == "yes":

                    Output = Output.replace("\{", "@lp")
                    Output = Output.replace("\}", "@rp")
                    Output = Output.replace("{", "")
                    Output = Output.replace("}", "")
                    Output = Output.replace("$", "")
                    Output = Output.replace("\mathrm", "")
                    Output = Output.replace("\\rm", "")

                    Output = Output.replace("@lp", "{")
                    Output = Output.replace("@rp", "}")

                    for bf, af in PlainConverter.items():
                        Output = Output.replace(bf, af)

                CitationOutputs.append(Output + "\n")

        if not CitationOutputs:
            print("\nNo matched results\n")

        else:
            print("")
            print(*CitationOutputs)

            if ExportOption == "yes":
                file.writelines(CitationOutputs)

    




# %%
