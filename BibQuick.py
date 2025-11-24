#%%
# BibQuick v1.2.0 (Nov 25, 2025)
# Ryo Fukushima
#
import bibtexparser
import copy
import re
import sys
import os
import configparser
import datetime

##### Read parameter values from BibQuickParams.ini #####

config_ini = configparser.ConfigParser()

default_configs = {"CurrentParameters":{
                                        "AddLetters":"",
                                        "LastDelimiterIgnore":"no",
                                        "ManyAuthors":"no",
                                        "ManyAuthorsOption":"",
                                        "EtAlExpression":"",
                                        "YearPar":"yes",
                                        "NoPar":"yes",
                                        "Template":"",
                                        "PlainConvert":"yes", 
                                        }  
                   }

config_ini.read_dict(default_configs)

path = os.path.join(os.path.dirname(__file__), "BibQuickParams.ini")
config_ini.read(path, encoding="utf-8")

BibtexLocation = config_ini["CurrentParameters"]["BibtexLocation"]
ExportOption = config_ini["CurrentParameters"]["InteractiveExport"]
CitationStyle = config_ini["CurrentParameters"]["CitationStyle"]
AddLetters = config_ini["CurrentParameters"]["AddLetters"] 
AuthorStyle = config_ini["CurrentParameters"]["AuthorStyle"]
LastDelimiterIgnore = config_ini["CurrentParameters"]["LastDelimiterIgnore"]
ManyAuthors = config_ini["CurrentParameters"]["ManyAuthors"]
ManyAuthorsOption = config_ini["CurrentParameters"]["ManyAuthorsOption"]
EtAlExpression = config_ini["CurrentParameters"]["EtAlExpression"]
YearPar = config_ini["CurrentParameters"]["YearPar"]
NoPar = config_ini["CurrentParameters"]["NoPar"]
TemplateName = config_ini["CurrentParameters"]["Template"]
PlainConvert = config_ini["CurrentParameters"]["PlainConvert"]


BatchConvert = config_ini["CurrentParameters"]["BatchConvert"]
AlphabeticalSorting = config_ini["CurrentParameters"]["AlphabeticalSorting"]

##### Define some lists #####

SignConverter = {"s": " ", "p": ".", "c": ",", "cl": ":", "ps": ". ", "cs": ", ", "cls": ": ", "n": "", "sc": ";", "scs": "; ",
                 "q": "'", "dq": '"',
                 "ap": "&", "a": "and", "aps": "& ", "as": "and ", "bsap": "\&", "bsaps": "\& ",
                 "sap": " &", "sa": " and", "saps": " & ", "sas": " and ", "sbsap": " \&", "sbsaps": " \& "}

CitationStyle_list = CitationStyle.split(",")
AuthorStyle_list = AuthorStyle.split(",")
ManyAuthorsOption_list = ManyAuthorsOption.split(",")
AddLetters_list = AddLetters.split(",")

PlainConverter = {"--": "–", 
                  
                  "\\alpha": "α","\\beta": "β","\\gamma": "γ","\\delta": "δ","\\epsilon": "ϵ",
                  "\\varepsilon": "ε","\\zeta": "ζ","\\eta": "η","\\theta": "θ","\\vartheta": "ϑ",
                  "\\iota": "ι","\\kappa": "κ","\\lambda": "λ","\\mu": "μ","\\nu": "ν",
                  "\\xi": "ξ","\\pi": "π","\\varpi": "ϖ","\\rho": "ρ","\\varrho": "ϱ",
                  "\\sigma": "σ","\\varsigma": "ς","\\tau": "τ","\\upsilon": "υ","\\phi": "ϕ",
                  "\\varphi": "φ","\\chi": "χ","\\psi": "ψ","\\omega": "ω",
                  
                  "\\Gamma": "Γ","\\Lambda": "Λ","\\Sigma": "Σ","\\Psi": "Ψ","\\Delta": "Δ",
                  "\\Xi": "Ξ","\\Upsilon": "Υ","\\Omega": "Ω","\\Theta": "Θ","\\Pi": "Π",
                  "\\Phi": "Φ",
                  
                  '\\"u': "ü", '\\"a': "ä", '\\"o': "ö", '\\"\\i': "ï",
                  '\\"U': "Ü", '\\"A': "Ä", '\\"O': "Ö", '\\"\\I': "Ï",
 
                  "\\'e": "é", "\\'a": "á", "\\'\\i": "í","\\'u": "ú", "\\'o": "ó",
                  "\\'E": "É", "\\'A": "Á", "\\'\\I": "Í","\\'U": "Ú", "\\'O": "Ó",
                  
                  "\\`e": "è", "\\`a": "à", "\\`\\i": "ì","\\`u": "ù", "\\`o": "ò",
                  "\\`E": "È", "\\`A": "À", "\\`\\I": "Ì","\\`U": "Ù", "\\`O": "Ò",

                  "\\^\\i": "î",
                  "\\^\\I": "Î",

                  "\\v c": "č", "\\v s": "š", "\\v r": "ř", "\\v g": "ğ", "\\v e": "ě", "\\v z": "ž",
                  "\\v{c": "č", "\\v{s": "š", "\\v{r": "ř", "\\v{g": "ğ", "\\v{e": "ě", "\\v{z": "ž",
                  "\\v C": "Č", "\\v S": "Š", "\\v R": "Ř", "\\v G": "Ğ", "\\v E": "Ě", "\\v Z": "Ž",
                  "\\v{C": "Č", "\\v{S": "Š", "\\v{R": "Ř", "\\v{G": "Ğ", "\\v{E": "Ě", "\\v{Z": "Ž",

                  "\\c s" : "ş", "\\c c" : "ç",
                  "\\c{s" : "ş", "\\c{c" : "ç", 
                  "\\c S" : "Ş","\\c C" : "Ç",
                  "\\c{S" : "Ş","\\c{C" : "Ç", 

                  "\.I": "İ",

                  "\\o":"ø", 
                  "\\O":"Ø", 

                  "\\aa": "å",
                  "\\AA" : "Å",

                  "\\l": "ł", "\\L": "Ł",

                  "\\'c": "ć", "\\'C": "Ć",
                  "\\'{c": "ć", "\\'{C": "Ć",

                  "\\~n": "ñ", "\\~N": "Ñ",
                  "\\~{n": "ñ", "\\~{N": "Ñ",

                  "\\~a": "ã", "\\~A": "Ã",
                  "\\~{a": "ã", "\\~{A": "Ã",

                  "\\'n": "ń", "\\'N": "Ń",
                  "\\'{n": "ń", "\\'{N": "Ń",

                  "\\copyright": "©", "\\textcopyright": "©", "\\&": "&", "\\%":"%", "\\textordmasculine": "°"}

CitationStyleConverter = {"T": "title", "J": "journal", "V": "volume", "P":"pages", "U": "url", "D": "doi", "M": "month", "ID": "ID"}
# A, Y, N, DD, DL is implemented separately in the CitationExport function

##### Start UI (session no. = timestamp) #####

print("============================================================\n")
print("                     BibQuick v1.2.0")
print(" Repository URL: https://github.com/Ryo-fkushima/BibQuick   \n")
print("============================================================")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
print("Session No. " + timestamp)
print("Loading database......")

##### Open bibtex database as dict (bib_database) #####

with open(BibtexLocation, encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

##### Make editable list from bib_database (bib_datalist) #####

bib_datalist = list(bib_database.entries_dict.values())

print("Template:", TemplateName)

##### Make lists of authors' names and years (names, years) #####

names = []
years = []
bib_datalist_modified = []
for i in range(len(bib_datalist)):

    if ("author" in bib_datalist[i] and
        "year" in bib_datalist[i] and 
        bib_datalist[i]["year"].isdigit() == True and 
        "journal" in bib_datalist[i]): # only data with author, year, journal will be imported
        
        bib_datalist_modified.append(bib_datalist[i]) # extracted database with valid author, year, journal data (bib_datalist_modified)

        bib_datalist[i]["author"] = " ".join(bib_datalist[i]["author"].split())
        names.append(bib_datalist[i]["author"].split(" and "))
        years.append(int(bib_datalist[i]["year"]))

if PlainConvert == "yes": # TeX style -> plain text

    for i in range(len(names)):
        for j in range(len(names[i])):

            for bf, af in PlainConverter.items():
                names[i][j] = names[i][j].replace(bf, af)

            names[i][j] = names[i][j].replace("{", "")
            names[i][j] = names[i][j].replace("}", "")
            names[i][j] = names[i][j].replace("\\i", "ı")

print("%i/%i items read from the database"% (len(bib_datalist_modified), len(bib_datalist)))

##### Split names into firstnames and surnames (firstnames, surnames) #####

surnames = copy.deepcopy(names)
firstnames = copy.deepcopy(names)

for i in range(len(names)):
    for j in range(len(names[i])):

        if ", " in names[i][j] and "," in names[i][j]:     # Fukushima, Ryo
            surnames[i][j] = names[i][j].split(", ")[0]
            firstnames[i][j] = names[i][j].split(", ")[1]
        elif "," in names[i][j]:                           # Fukushima,Ryo
            surnames[i][j] = names[i][j].split(",")[0]
            firstnames[i][j] = names[i][j].split(",")[1]
        elif " " in names[i][j]:                          # Ryo Fukushima
            firstnames[i][j] = " ".join(names[i][j].split(" ")[0:-1])
            surnames[i][j] = names[i][j].split(" ")[-1]

        firstnames[i][j] = firstnames[i][j].replace("-", " ") # Jun-ichi -> Jun ichi

        # TJB -> T J B (max. 5 letters)

        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3 \\4 \\5", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3 \\4", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])([A-Z])","\\1 \\2 \\3", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])([A-Z])","\\1 \\2", firstnames[i][j])
        
        # T.J.B. -> T J B (max. 5 letters)

        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3 \\4 \\5", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3 \\4", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.([A-Z])\.","\\1 \\2 \\3", firstnames[i][j])
        firstnames[i][j] = re.sub("([A-Z])\.([A-Z])\.","\\1 \\2", firstnames[i][j])
        
##### Convert firstnames into initials (firstnames_I) #####
         
firstnames_I = copy.deepcopy(firstnames)
spacelocation = []
divide = AuthorStyle_list[2]  # T J B -> TdJdBe (d = divide, e = endsign)
endsign = AuthorStyle_list[3] 

for i in range(len(names)):
    for j in range(len(names[i])):
        
        firstnames_I[i][j] = firstnames[i][j][0].upper() # Jun ichi -> J

        spacelocation = [m.start() for m in re.finditer(" ", firstnames[i][j])]
        if len(spacelocation) > 0:
            for k in range(len(spacelocation)):
                firstnames_I[i][j] = firstnames_I[i][j] + SignConverter[divide] + firstnames[i][j][spacelocation[k] + 1].upper() # Jun ichi -> JdI
        firstnames_I[i][j] += SignConverter[endsign] # JdI -> JdIe


##### Make a list for search and insert & before the last author #####

InLineCitations = []                            # list for search (e.g., fukushima+2024)
IDs = []                            # list for ID search
surnames_and = copy.deepcopy(surnames)          # xxx_and: those with & before the last author's name
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

    InLineCitations[i] = InLineCitations[i].lower()            # lowercase for the search list
    InLineCitations[i] = InLineCitations[i].replace(" ","")    # van keken+2002 -> vankeken+2002

    IDs.append(bib_datalist_modified[i]["ID"])   
    IDs[i] = "@" + IDs[i].lower()

                 

##### Make lists of authors' names #####

SsF, ScsF, SsI, ScsI = [], [], [], []
FsS, FcsS, IsS, IcsS = [], [], [], []
S = surnames_and


for i in range(len(names)):
    
    SsF.append([x + " " + y for (x, y) in zip(surnames_and[i], firstnames[i])])
    SsI.append([x + " " + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScsI.append([x + ", " + y for (x, y) in zip(surnames_and[i], firstnames_I[i])])
    ScsF.append([x + ", " + y for (x, y) in zip(surnames_and[i], firstnames[i])])
    FsS.append([x + " " + y for (x, y) in zip(firstnames_and[i], surnames[i])])
    FcsS.append([x + ", " + y for (x, y) in zip(firstnames_and[i], surnames[i])])
    IsS.append([x + " " + y for (x, y) in zip(firstnames_I_and[i], surnames[i])])
    IcsS.append([x + ", " + y for (x, y) in zip(firstnames_I_and[i], surnames[i])])


AuthorStyleConverter = {
    "SsF": SsF,
    "ScsF": ScsF,

    "SsI": SsI,
    "ScsI": ScsI,
    
    "FsS": FsS,
    "FcsS": FcsS,

    "IsS": IsS,
    "IcsS": IcsS,

    "S": S,
}

##### Main function to export reference #####

def CitationExport(formattedauthor, **args):        # args == bib_datalist_modified[i]

    result = []

    for i in range(len(CitationStyle_list)):         
        if CitationStyle_list[i] == "A":           # A option
            result.append(formattedauthor)
        
        if CitationStyle_list[i] == "Y":            # Y option 
            if YearPar == "yes":
                result.append("(" + args["year"] + ")")
            else:
                result.append(args["year"])

        if CitationStyle_list[i] == "N":            # N option 
            if ("number" in args) and (NoPar == "yes"):
                result.append("(" + args["number"] + ")")
            elif ("number" in args):
                result.append(args["number"])
            else:
                result.append("")

        if CitationStyle_list[i] == "DD":           # DD option (DOI as a real doi)
            if ("doi" in args) and ("doi:" not in args["doi"]) and ("doi.org/" not in args["doi"]):
                result.append(args["doi"])
            elif ("doi" in args) and ("https://doi.org/" in args["doi"]):
                result.append(args["doi"].replace("https://doi.org/",""))
            elif ("doi" in args) and ("http://dx.doi.org/" in args["doi"]):
                result.append(args["doi"].replace("http://dx.doi.org/",""))
            elif ("doi" in args) and ("doi:" in args["doi"]):
                result.append(args["doi"].replace("doi:", ""))
            else:
                result.append("")

        if CitationStyle_list[i] == "DL":           # DL option (DOI as a link)
            if ("doi" in args) and ("doi:" not in args["doi"]) and ("doi.org/" not in args["doi"]):
                result.append("https://doi.org/" + args["doi"])
            elif ("doi" in args) and ("https://doi.org/" in args["doi"]):
                result.append(args["doi"])
            elif ("doi" in args) and ("http://dx.doi.org" in args["doi"]):
                result.append(args["doi"].replace("http://dx.doi.org", "https://doi.org/"))
            elif ("doi" in args) and ("doi:" in args["doi"]):
                result.append("https://doi.org/" + args["doi"].replace("doi:", ""))
            else:
                result.append("")

        if CitationStyle_list[i] in CitationStyleConverter:           # other options
            if CitationStyleConverter[CitationStyle_list[i]] in args:
                result.append(args[CitationStyleConverter[CitationStyle_list[i]]])
            else: 
                result.append("")

        if CitationStyle_list[i] in SignConverter:                    # signs
            result.append(SignConverter[CitationStyle_list[i]])

        if CitationStyle_list[i].isdigit() == True:                    # AddLetters
            result.append(AddLetters_list[int(CitationStyle_list[i])])

    return "".join(result)

##### function to handle many authors' option #####

def AuthorFormat(listofname):

    formatresult = []

    if (ManyAuthors == "yes") and (len(listofname) > int(ManyAuthorsOption_list[0])):
        formatresult = SignConverter[AuthorStyle_list[1]].join(listofname[0:int(ManyAuthorsOption_list[1])])
        formatresult += str(EtAlExpression)
            
        if int(ManyAuthorsOption_list[2]) == 1:
            formatresult += listofname[-1].replace(SignConverter[andsign], "")

    elif LastDelimiterIgnore == "yes":
        formatresult = SignConverter[AuthorStyle_list[1]].join(listofname[0:-1])
        formatresult += listofname[-1]
    else:
        formatresult = SignConverter[AuthorStyle_list[1]].join(listofname)

    return formatresult



#%%
##### Batch convert #####

outputpath = os.path.join(os.path.dirname(__file__), "%s.txt"%timestamp)

if BatchConvert == "yes":
    print("----------------------------")
    print("       Batch convert")
    print("----------------------------")

    TxtFileLocation = input("Type the path to the input txt file: ")
    TxtFileLocation = TxtFileLocation.strip()

    ConvertSource = open(TxtFileLocation, "r", encoding="utf-8")

    ConvertSource_list = re.findall(r"[\}\{\\\"\`\'\-a-zß-ÿĀ-ſ]+\d{4}|[\}\{\\\"\`\'\-a-zß-ÿĀ-ſ]+&[\}\{\\\"\`\'\-a-zß-ÿĀ-ſ]+\d{4}|[\}\{\\\"\`\'\-a-zß-ÿĀ-ſ]+\+\d{4}|@+\S+", ConvertSource.read().lower())

    #if AlphabeticalSorting == "yes":
     #   ConvertSource_list = sorted(ConvertSource_list)


#%%
    print("%i items read as input"% len(ConvertSource_list))

    print("Converting......\n")

    CitationOutputs = []

    SuccessCounter = 0
    SubCounter = 0

    for j in range(len(ConvertSource_list)):
        
        for i in range(len(names)):
            if (InLineCitations[i] == ConvertSource_list[j]) or (IDs[i] == ConvertSource_list[j]):
                
                Output = CitationExport(AuthorFormat(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])
                Output = Output.replace("@", "") # @ was first introduced to allow EtAlExpression to start/end with spaces, but removed here

                if PlainConvert == "yes": # TeX style -> plain text
                    
                    for bf, af in PlainConverter.items(): 
                        Output = Output.replace(bf, af)
                    
                    Output = Output.replace("\\{", "@lp") 
                    Output = Output.replace("\\}", "@rp") # $\{100\}$ -> $@lp100@rp$
                    Output = Output.replace("{", "")
                    Output = Output.replace("}", "") # remove { and }
                    Output = Output.replace("$", "") # $@lp100@rp$ -> @lp100@rp
                    Output = Output.replace("\\mathrm", "")
                    Output = Output.replace("\\rm", "")

                    Output = Output.replace("@lp", "{")
                    Output = Output.replace("@rp", "}") # @lp100@rp -> {100}

                    Output = Output.replace("\\i", "ı")

        

                CitationOutputs.append(Output + "\n")
                SubCounter += 1

        if SubCounter > 0:
            SuccessCounter += 1
            print(ConvertSource_list[j].lower() + " : " + str(SubCounter))
        else:
            print(ConvertSource_list[j].lower() + " --------------------------> Not found")

        SubCounter = 0

    print("\n%i/%i items are successfully converted"% (SuccessCounter, len(ConvertSource_list)))

    if AlphabeticalSorting == "yes":
        CitationOutputs = sorted(CitationOutputs, key=str.lower)

    file = open(outputpath, 'a', encoding="utf-8")
    file.writelines(CitationOutputs)
    print("\nThe result has been exported to",outputpath,"\n")

    file.close()



#%%
##### Interactive mode #####
else:

    print("----------------------------")
    print("      Interactive mode")
    print("----------------------------")

    if ExportOption == "yes":
        file = open(outputpath, 'a', encoding="utf-8")

    while True:
        SearchWord = input("\nType the reference name or @ID (case insensitive)\nex. surname+2024/surname&surname2024/surname2024\n(type 'e' to exit; type 'list' or 'idlist' to display database): ")
        SearchWord = SearchWord.strip()
        
        if SearchWord.lower() == "e":
            if ExportOption == "yes":
                file.close()
                print("\nThe result has been exported to",outputpath,"\n")
            sys.exit()

        if SearchWord.lower() == "list":
            
            print(*sorted(InLineCitations))
           
            continue

        if SearchWord.lower() == "idlist":
            
            print(*sorted(IDs))
           
            continue
        

        CitationOutputs = []

        for i in range(len(names)):

            if (InLineCitations[i] == SearchWord.lower()) or (IDs[i] == SearchWord.lower()):
                
                Output = CitationExport(AuthorFormat(AuthorStyleConverter[AuthorStyle_list[0]][i]), **bib_datalist_modified[i])
                Output = Output.replace("@", "")

                if PlainConvert == "yes": # TeX style -> plain text; same as above

                    for bf, af in PlainConverter.items():
                        Output = Output.replace(bf, af)
                    
                    Output = Output.replace("\\{", "@lp")
                    Output = Output.replace("\\}", "@rp")
                    Output = Output.replace("{", "")
                    Output = Output.replace("}", "")
                    Output = Output.replace("$", "")
                    Output = Output.replace("\\mathrm", "")
                    Output = Output.replace("\\rm", "")

                    Output = Output.replace("@lp", "{")
                    Output = Output.replace("@rp", "}")

                    Output = Output.replace("\\i", "ı")

                CitationOutputs.append(Output + "\n")

        if not CitationOutputs:
            print("\nNo matched results\n")

        else:
            print("")
            print(*CitationOutputs)

            if ExportOption == "yes":
                file.writelines(CitationOutputs)

    




# %%
