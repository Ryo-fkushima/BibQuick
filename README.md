# **BibQuick: Citation export assistant (v1.1.4)**

> *If you are struggling to prepare reference lists, try **BibQuick**!*

**BibQuick** is a python-based citation export assistant. From a BibTeX file that includes bibliographic information, 
this program exports references with any citation style.

**BibQuick**は、BibTeXファイルから引用文献リストをテキストで出力するPythonツールです。普段文献管理ソフトを使用しない方々向けに、英語論文執筆時の引用文献リスト出力のみに特化して開発しました。

## How to use

0. Install python3 (>3.8 is recommended) to your computer and install the [**bibtexparser**](https://pypi.org/project/bibtexparser/) module.

1. Make a new directory and put **BibQuick.py** and **BibQuickParams.ini** there.

2. Prepare a BibTeX file of the bibliographic information (e.g., **example_F24.bib**) and put it anywhere accessible.

   <img width = "600" src = "./fig1.png">

Once you have prepared the BibTeX database file, there are two options next: *interactive mode* and *batch convert mode*:

### i. Interactive mode

3. Edit `CurrentParameters` in **BibQuickParams.ini** as follows:
   
   * `BibtexLocation` should be a path to the BibTeX database file. Enter the full path here.
   * `InteractiveExport` is the option for exporting results. Set `yes` to get your results as a .txt file, or `no` to see results only in the console.
   * `BatchConvert` is the option to switch the interactive mode and batch convert mode. Here, set `no`. 
   * `AlphabeticalSorting` is the option for alphabetical sorting of the output when you set `BatchConvert=yes`. Here, this value is irrelevant.
   * Other parameters determine the citation style. Copy any template in **BibQuickParams.ini** and paste it inside the `CurrentParameters` section.
   
   For example:
   ```
   [CurrentParameters]
   BibtexLocation=/Users/fukushimaryou/BibQuick/demo/example_F24.bib
   InteractiveExport=no
   ;
   BatchConvert=no
   AlphabeticalSorting=yes
   ;
   CitationStyle=A,s,Y,ps,T,ps,J,cs,V,N,cs,P,cs,DL,p
   AddLetters=
   AuthorStyle=ScsI,cs,ps,p,aps
   ManyAuthors=yes
   ManyAuthorsOption=20,19,1
   EtAlExpression=@ . . . @
   YearPar=yes
   NoPar=yes
   PlainConvert=yes
   Template=APA
   ```

4. Move into the directory via your console and run **BibQuick.py**, and follow the instructions appearing in the console. You can search papers by typing their contracted names (e.g., `fukushima+2024`) or their BibTeX IDs (e.g., `@fukushima2024simulation`; `@` must be placed before the ID). If you set `InteractiveExport=yes`, you will finally get **[Session No].txt** in the directory.

   <img width = "600" src = "./fig2.png">

### ii. Batch convert from a .txt file

3. Prepare a .txt file that includes the input list (e.g., **batch_example.txt**, **batch_example2.txt**) and put it anywhere accessible.

4. Edit `CurrentParameters` in **BibQuickParams.ini** as follows:
   
   * `BibtexLocation`: same as above
   * `InteractiveExport` is irrelevant here.
   * Set `BatchConvert` as `yes`. 
   * Set `AlphabeticalSorting` as `yes` or `no` according to your preference.
   * Other parameters: same as above
  
   For example:
   ```
   [CurrentParameters]
   BibtexLocation=/Users/fukushimaryou/BibQuick/demo/example_F24.bib
   InteractiveExport=no
   ;
   BatchConvert=yes
   AlphabeticalSorting=yes
   ;
   CitationStyle=A,s,Y,ps,T,ps,J,cs,V,N,cs,P,cs,DL,p
   AddLetters=
   AuthorStyle=ScsI,cs,ps,p,aps
   ManyAuthors=yes
   ManyAuthorsOption=20,19,1
   EtAlExpression=@ . . . @
   YearPar=yes
   NoPar=yes
   PlainConvert=yes
   Template=APA
   ```

5. Move into the directory via your console and run **BibQuick.py**. You will be asked the path to the input list. You can finally get **[Session No].txt** in the directory.

## Tips for preparing the BibTeX database file

- One option to get the BibTeX data is using the function of [Google Scholar](https://scholar.google.co.jp). You can copy the BibTeX information on the browser, and add it into your local .bib file. However, if you require DOIs, you'll have to access the journal website and add `doi` manually. **Note: when you add a new field on each article, don't forget to put commas between different fields!**
  
- Another option is using some web service to get BibTeX from DOI (e.g., [doi2bib](https://www.doi2bib.org)).
  
- From the BibTeX database, only bibliographic data of journals with `author`, `year` (as number), and `journal` fields will be successfully read. Other incomplete data will not be imported.

- You can search papers by their BibTeX IDs. If you use [PubMed](https://pubmed.ncbi.nlm.nih.gov) to search papers, you can add PMID as a BibTeX ID when preparing the BibTeX database file. This enables to find papers by @PMID.

  For example:
  ```
  @article{37707320,
  title = {Nanoscopic Elucidation of Spontaneous Self-Assembly of Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2) Open Reading Frame 6 (ORF6) Protein},
  volume = {14},
  ISSN = {1948-7185},
  url = {http://dx.doi.org/10.1021/acs.jpclett.3c01440},
  DOI = {10.1021/acs.jpclett.3c01440},
  number = {38},
  journal = {The Journal of Physical Chemistry Letters},
  publisher = {American Chemical Society (ACS)},
  author = {Nishide,  Goro and Lim,  Keesiang and Tamura,  Maiki and Kobayashi,  Akiko and Zhao,  Qingci and Hazawa,  Masaharu and Ando,  Toshio and Nishida,  Noritaka and Wong,  Richard W.},
  year = {2023},
  month = sep,
  pages = {8385–8396}
  }
  ``` 

## Tips for preparing the input list for batch convert

- In the batch convert mode, this program will search any strings of `[surname][year]` (1 author), `[surname1]&[surname2][year]` (2 authors), and `[surname]+[year]` (>3 authors) from the input list. Any space in the search word should be removed beforehand.
- In addition, any string starting from `@` will be also read and used to search papers by their BibTeX IDs.

## Note

- This version doesn't support generating journal abbreviations, changing capitalization in the paper's title, or handling specific characters (e.g., Asian characters).
- As for the citation style setting, please refer to [**CitationStyleManual.md**](./CitationStyleManual.md).


## Requirement

Required module: [bibtexparser](https://pypi.org/project/bibtexparser/) (tested with v1.4.1)

The script was tested on: Python 3.11.6/3.8.18 (macOS Ventura, MacBook Air 2020 with Intel CPU), and Python 3.9.13 (Windows 11, Minisforum EliteMini X500 with AMD Ryzen CPU).

## Author

Ryo Fukushima (rpifukushima@gmail.com)

## Updates

Jan 02, 2025 (v1.1.4): Bug fixed. Surnames with apostrophes are now correctly read in the batch convert mode.

Nov 25, 2024 (v1.1.3): Bug fixed for the AlphabeticalSorting option and special characters were additionaly implemented.

Nov 07, 2024 (v1.1.2): Bug fixed for Windows OS and special characters were additionaly implemented.

Sep 17, 2024 (v1.1.1): Bug fixed. Surnames with a hyphen are now correctly read in the batch convert mode.

Sep 12, 2024 (v1.1.0): ID Search function was implemented. New blocks (M, ID) were added.

Sep 07, 2024 (v1.0.1): A few special characters were additionally implemented. 

Sep 05, 2024: v1.0.0 was released.
