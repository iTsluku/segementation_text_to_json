# sondergerichtsakten-regesten

## Introduction

Das Projekt Sondergerichtsakten zielt auf eine automatisierte Erfassung der Regesten ab 
und ermöglich die Transformation eines semi-strukturierten Textbestandes zu einem strukturierten Format.
Das Projekt basiert auf mehreren sequentiellen Prozessen. Im Prozess davor wurde der analog vorliegende 
Dokumentenbestand gescannt und mittels Tesseract (Software für OCR-Verfahren) zu Text- bzw. HOCR-Dokumenten transformiert.
Der Tesseract Output dient als Input für diesen Prozess. 

Mögliche Input-Formate (Tesseract Output basierend auf Seitensegmentierungs-Modus): Zeilenformat (--psm 6), Spaltenformat (--psm 4), HOCR.


## Project structure

    .
    ├── input                   # Tesseract output (row-format, column-format, hocr)
    ├── output                  # JSON (output.json)
    ├── special_court_munich    # Parser and regex extraction implementation
    ├── tests                   # Unit tests
    ├── README.md               # Documentation
    ├── eval_output.ipynb       # Evaluation
    ├── main.py                 # Execution script
    ├── requirements.txt        # Python module requirements
    └── setup.py                # Setup script

## Example

### JSON output

   ```json
   {
     "meta": {
       "page": "621",
       "document_name": "DHUP_NSJ_00665_Band_3_Sondergericht_München_Teil_3_1939_00621.hocr",
       "type": "Prozeß",
       "processing_date": "09/08/2022, 15:26:38",
       "error_tags": []
     },
     "proceeding": {
       "ID": "3133",
       "shelfmark": "9161",
       "duration": "28, Spt. 1938 15. Apr. 1942",
       "registration_no": "(1 KLs So 10/39)",
       "text_original": "(3133) 9161 Prozeß gegen den Techniker Karl OELLER (geb. 22. Jul. 1882) aus München wegen Diebstahls. Urteils Unterbringung in einer Heil- und Pflegeanstalt (8 3 HG, 88 42, 242 StGB) 15. Apr. 1942 Weglegung der Akten. 28, Spt. 1938 - 15. Apr. 1942 (1 KLs So 10/39)",
       "text_preprocessed": "Prozeß gegen den Techniker Karl OELLER (geb. 22. Jul. 1882) aus München wegen Diebstahls. Urteils Unterbringung in einer Heilund Pflegeanstalt (8 3 HG, 88 42, 242 StGB) 15. Apr. 1942 Weglegung der Akten. 28, Spt. 1938 15. Apr. 1942 (1 KLs So 10/39)",
       "people": [
         {
           "first_name": "Karl",
           "last_name": "OELLER",
           "occupation": "Techniker",
           "date_of_birth": "1882-07-22",
           "accusation": "Diebstahls",
           "law": "(8 3 HG, 88 42, 242 StGB)",
           "result": "Urteils Unterbringung in einer Heilund Pflegeanstalt",
           "residence": "München",
           "attachements": null,
           "add_prosecution": null
         }
       ]
     }
   }
   ```

### Text input
   ```txt
   (3133) 9161 Prozeß gegen den Techniker Karl OELLER
   (geb. 22. Jul. 1882) aus München wegen
   Diebstahls.
   
   Urteils Unterbringung in einer Heil- und
   Pflegeanstalt
   (8 3 HG, 88 42, 242 StGB)
   
   15. Apr. 1942 Weglegung der Akten.
   
   28, Spt. 1938 - 15. Apr. 1942
   
   (1 KLs So 10/39)
   ```
### HOCR input
   ```html
    ...
    <p class='ocr_par' id='par_1_1' lang='deu' title="bbox 616 299 4041 604">
     <span class='ocr_line' id='line_1_1' title="bbox 616 299 4041 416; baseline 0.008 -33; x_size 103; x_descenders 19; x_ascenders 17">
      <span class='ocrx_word' id='word_1_1' title='bbox 616 299 948 400; x_wconf 96'>(3133)</span>
      <span class='ocrx_word' id='word_1_2' title='bbox 1218 312 1439 398; x_wconf 87'>9161</span>
      <span class='ocrx_word' id='word_1_3' title='bbox 1708 325 2065 397; x_wconf 94'>Prozeß</span>
      <span class='ocrx_word' id='word_1_4' title='bbox 2141 347 2440 416; x_wconf 96'>gegen</span>
      <span class='ocrx_word' id='word_1_5' title='bbox 2510 331 2686 399; x_wconf 96'>den</span>
      <span class='ocrx_word' id='word_1_6' title='bbox 2755 332 3300 405; x_wconf 96'>Techniker</span>
      <span class='ocrx_word' id='word_1_7' title='bbox 3368 339 3603 407; x_wconf 92'>Karl</span>
      <span class='ocrx_word' id='word_1_8' title='bbox 3679 340 4041 411; x_wconf 92'>OELLER</span>
     </span>
     <span class='ocr_line' id='line_1_2' title="bbox 1722 411 4039 533; baseline 0.008 -37; x_size 106; x_descenders 21; x_ascenders 33">
      <span class='ocrx_word' id='word_1_9' title='bbox 1722 411 1992 515; x_wconf 96'>(geb.</span>
      <span class='ocrx_word' id='word_1_10' title='bbox 2080 428 2238 502; x_wconf 95'>22.</span>
      <span class='ocrx_word' id='word_1_11' title='bbox 2323 432 2546 504; x_wconf 91'>Jul.</span>
      <span class='ocrx_word' id='word_1_12' title='bbox 2639 420 2917 518; x_wconf 96'>1882)</span>
      <span class='ocrx_word' id='word_1_13' title='bbox 3003 455 3173 507; x_wconf 96'>aus</span>
      <span class='ocrx_word' id='word_1_14' title='bbox 3243 439 3670 512; x_wconf 96'>München</span>
      <span class='ocrx_word' id='word_1_15' title='bbox 3735 461 4039 533; x_wconf 95'>wegen</span>
     </span>
     <span class='ocr_line' id='line_1_3' title="bbox 1706 528 2360 604; baseline 0.012 -8; x_size 89.100021; x_descenders 20.100019; x_ascenders 18">
      <span class='ocrx_word' id='word_1_16' title='bbox 1706 528 2360 604; x_wconf 96'>Diebstahls.</span>
     </span>
    </p>

    <p class='ocr_par' id='par_1_2' lang='deu' title="bbox 1706 732 4159 1039">
     <span class='ocr_line' id='line_1_4' title="bbox 1706 732 4159 832; baseline 0.008 -30; x_size 92; x_descenders 21; x_ascenders 20">
      <span class='ocrx_word' id='word_1_17' title='bbox 1706 732 2111 806; x_wconf 73'>Urteils</span>
      <span class='ocrx_word' id='word_1_18' title='bbox 2198 736 2990 832; x_wconf 96'>Unterbringung</span>
      <span class='ocrx_word' id='word_1_19' title='bbox 3062 744 3176 813; x_wconf 96'>in</span>
      <span class='ocrx_word' id='word_1_20' title='bbox 3247 747 3543 816; x_wconf 93'>einer</span>
      <span class='ocrx_word' id='word_1_21' title='bbox 3610 750 3906 820; x_wconf 91'>Heil-</span>
      <span class='ocrx_word' id='word_1_22' title='bbox 3978 752 4159 821; x_wconf 96'>und</span>
     </span>
     <span class='ocr_line' id='line_1_5' title="bbox 2197 841 2986 932; baseline 0.006 -23; x_size 91.100021; x_descenders 20.100019; x_ascenders 20">
      <span class='ocrx_word' id='word_1_23' title='bbox 2197 841 2986 932; x_wconf 91'>Pflegeanstalt</span>
     </span>
     <span class='ocr_line' id='line_1_6' title="bbox 2211 927 3713 1039; baseline -0.002 -13; x_size 126.19415; x_descenders 27.194143; x_ascenders 30">
      <span class='ocrx_word' id='word_1_24' title='bbox 2211 927 2308 1026; x_wconf 44'>(8</span>
      <span class='ocrx_word' id='word_1_25' title='bbox 2385 944 2433 1022; x_wconf 85'>3</span>
      <span class='ocrx_word' id='word_1_26' title='bbox 2502 945 2663 1032; x_wconf 94'>HG,</span>
      <span class='ocrx_word' id='word_1_27' title='bbox 2756 933 2861 1030; x_wconf 92'>88</span>
      <span class='ocrx_word' id='word_1_28' title='bbox 2937 939 3093 1036; x_wconf 94'>42,</span>
      <span class='ocrx_word' id='word_1_29' title='bbox 3184 942 3354 1020; x_wconf 96'>242</span>
      <span class='ocrx_word' id='word_1_30' title='bbox 3430 940 3713 1039; x_wconf 71'>StGB)</span>
     </span>
    </p>

    <p class='ocr_par' id='par_1_3' lang='deu' title="bbox 1711 1088 3771 1191">
     <span class='ocr_line' id='line_1_7' title="bbox 1711 1088 3771 1191; baseline 0.008 -32; x_size 96; x_descenders 19; x_ascenders 26">
      <span class='ocrx_word' id='word_1_31' title='bbox 1711 1091 1865 1168; x_wconf 96'>15.</span>
      <span class='ocrx_word' id='word_1_32' title='bbox 1949 1092 2172 1180; x_wconf 96'>Apr.</span>
      <span class='ocrx_word' id='word_1_33' title='bbox 2265 1088 2492 1174; x_wconf 93'>1942</span>
      <span class='ocrx_word' id='word_1_34' title='bbox 2563 1097 3112 1191; x_wconf 92'>Weglegung</span>
      <span class='ocrx_word' id='word_1_35' title='bbox 3182 1103 3357 1173; x_wconf 96'>der</span>
      <span class='ocrx_word' id='word_1_36' title='bbox 3426 1103 3771 1178; x_wconf 95'>Akten.</span>
     </span>
    </p>

    <p class='ocr_par' id='par_1_4' lang='deu' title="bbox 1705 1241 3477 1338">
     <span class='ocr_line' id='line_1_8' title="bbox 1705 1241 3477 1338; baseline 0.007 -30; x_size 95.105629; x_descenders 20.073334; x_ascenders 24.1">
      <span class='ocrx_word' id='word_1_37' title='bbox 1705 1241 1865 1312; x_wconf 90'>28,</span>
      <span class='ocrx_word' id='word_1_38' title='bbox 1951 1243 2171 1331; x_wconf 95'>Spt.</span>
      <span class='ocrx_word' id='word_1_39' title='bbox 2265 1246 2493 1323; x_wconf 92'>1938</span>
      <span class='ocrx_word' id='word_1_40' title='bbox 2569 1286 2612 1296; x_wconf 81'>-</span>
      <span class='ocrx_word' id='word_1_41' title='bbox 2695 1249 2848 1325; x_wconf 96'>15.</span>
      <span class='ocrx_word' id='word_1_42' title='bbox 2932 1250 3156 1338; x_wconf 96'>Apr.</span>
      <span class='ocrx_word' id='word_1_43' title='bbox 3248 1246 3477 1331; x_wconf 95'>1942</span>
     </span>
    </p>

    <p class='ocr_par' id='par_1_5' lang='deu' title="bbox 1718 1327 2665 1432">
     <span class='ocr_line' id='line_1_9' title="bbox 1718 1327 2665 1432; baseline 0.021 -24; x_size 111; x_descenders 18; x_ascenders 24">
      <span class='ocrx_word' id='word_1_44' title='bbox 1718 1327 1802 1425; x_wconf 92'>(1</span>
      <span class='ocrx_word' id='word_1_45' title='bbox 1887 1345 2061 1413; x_wconf 91'>KLs</span>
      <span class='ocrx_word' id='word_1_46' title='bbox 2136 1345 2243 1415; x_wconf 96'>So</span>
      <span class='ocrx_word' id='word_1_47' title='bbox 2327 1334 2665 1432; x_wconf 95'>10/39)</span>
     </span>
    </p>
    ...
   ```

## Input format changes

| Input                        | Neue Scans | Erfasste Regesten |
|------------------------------|------------|-------------------|
| Textbestand der BA (Erhardt) | Nein       | 3437              |
| Spaltenformat                | Ja         | 7720              |
| Zeilenformat                 | Ja         | 7778              |
| HOCR                         | Ja         | 9562              |

## Installation

1. Clone the repo
   ```sh
   git clone https://git.fim.uni-passau.de/gassner/sondergerichtsakten-regesten.git
   ```
2. Install required modules
   ```sh
   pip install -r requirements.txt
   ```
3. Generate output.json (in output/)
   ```sh
   python main.py
   ```
   
## Requirements (RegEx extraction)

- [x] ID
- [x] shelfmark
- [x] proceedings
- [x] occupation
- [x] person
- [x] date_of_birth
- [x] residence
- [x] accusation
- [x] result
- [x] duration
- [x] registration_no

### (optional)

- [ ] person_background
- [x] law
- [x] attachments
- [ ] add_prosecution
   
## Limitations

Die Komplexität der Überführung in ein strukturiertes Format ergibt sich aus der Fehleranfälligkeit des OCR-Inputs 
und der Variation, wie der Inhalt der Regesten strukturiert und annotiert ist. Die Qualität des Inputs ist maßgeblich 
für den Output dieses Prozesses. Anbei folgt eine Liste mit bekannten/ offenen Problemen:

- Personen mit mehreren Berufen
- ...