# **BibQuick: Citation export assistant (v1.0.0)**

> *If you are struggling to prepare reference lists, try **BibQuick**!*

**BibQuick** is a python-based citation export assistant. From a BibTeX file that includes bibliographic information, 
this program export references with any citation style.

## How to use

0. Install python3 (>3.8 is recommended) to your computer and install the [**bibtexparser**](https://pypi.org/project/bibtexparser/) module.

1. Make a new directory and put **BibQuick.py** and **BibQuickParams.ini** there.

2. Prepare a BibTeX file of the bibliographic information (e.g., **example_F24.bib**) and put it anywhere accessible.

### i. Interactive mode

3. Edit `CurrentParameters` in **BibQuickParams.ini** as follows:
   
   * `BibTexLocation` should be a path to the BibTeX database file. Enter the full path here.
   * `InteractiveExport` is the option for exporting results. Set `yes` to get your results as a .txt file, or `no` to see results only in the console.
   * `BatchConvert` is the option to switch the interactive mode and batch convert mode. Here, set `no`. 
   * `AlphabeticalSorting` is the option for alphabetical sorting of the output when you set `BatchConvert=yes`. Here, this value is irrelevant.
   * Other parameters determine the citation style. Copy & paste any template in **BibQuickParams.ini**.

4. Move into the directory via your console and run **BibQuick.py**, and follow the instructions appearing in the console. (When you set `InteractiveExport=yes`, you can finally get **[Session No].txt** in the directory.)

### ii. Batch convert from a .txt file

3. Prepare a .txt file that includes the input list (e.g., **batch_example.txt**) and put it anywhere accessible.

4. Edit `CurrentParameters` in **BibQuickParams.ini** as follows:
   
   * `BibTexLocation`: same as above
   * `InteractiveExport` is irrelevant here.
   * Set `BatchConvert` as `yes`. 
   * Set `AlphabeticalSorting` as `yes` or `no` according to your preference.
   * Other parameters: same as above

5. Move into the directory via your console and run **BibQuick.py**. You will be asked the path to the input list. You can finally get **[Session No].txt** in the directory.

## Note

- From the BibTeX file, only bibliographic data of journals with `author`, `year` (as number), and `journal` will be successfully read. Other incomplete data will not be imported.
- This version doesn't support generating journal abbreviations, changing capitalization in the paper's title, or handling specific characters (e.g., Asian characters).
- In the batch convert mode, this program will search any strings of `[surname][year]` (1 author), `[surname1]&[surname2][year]` (2 authors), and `[surname]+[year]` (>3 authors) from the input list. Any space in the surnames should be removed beforehand.
- As for the citation style setting, please refer to **CitationStyleManual.md**.


## Requirement

Required module: [bibtexparser](https://pypi.org/project/bibtexparser/) (tested with v1.4.1)

The script was tested on: Python 3.11.6/3.8.18 (macOS Ventura, MacBook Air 2020 with Intel CPU), and Python 3.9.13 (Windows 11, Minisforum EliteMini X500 with AMD Ryzen CPU).

## Author

Ryo Fukushima (rpifukushima@gmail.com)

## Updates

Sep 05, 2024: v1.0.0 was released.
