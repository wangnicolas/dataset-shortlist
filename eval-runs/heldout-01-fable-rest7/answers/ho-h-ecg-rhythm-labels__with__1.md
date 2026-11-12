You can start today: four large, openly downloadable sets meet all your must-haves, and PTB-XL is the best first download. Access and licence were checked on 12 November 2026 against each host's own record; anything I'm relying on from memory is marked.

## What I assumed you need
- **R1 (must):** standard 12-lead resting ECG, about 10 seconds.
- **R2 (must):** diagnostic labels for AF, bundle branch blocks and AV block.
- **R3 (must):** at least a few thousand recordings.
- **R4 (must):** direct download, with no application, credentialing, ethics approval or signed agreement.
- **R5 (nice):** labels assigned or confirmed by cardiologists.
- **R6 (nice):** licence allows research use and publication. I assumed academic use and adult patients.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PTB-XL | Direct download, no account | CC BY 4.0 | 21,799 ECGs / 18,869 patients | Strong | today |
| 2 | Chapman–Shaoxing–Ningbo ("A large scale 12-lead ECG database for arrhythmia study") | Direct download, no account | CC BY 4.0 | 45,152 patients | Strong | today |
| 3 | PhysioNet/CinC Challenge 2021 collection | Direct download, no account | CC BY 4.0 | about 88,000 ECGs (from memory), 13.6 GB | Strong | today |
| 4 | CODE-15% | Direct download, no account | CC BY 4.0 | 345,779 ECGs / 233,770 patients | Strong | today |
| 5 | SPH (Shandong Provincial Hospital) | Direct download, from memory; figshare blocked the check | CC BY 4.0 | 25,770 ECGs / 24,666 patients | Strong, access unconfirmed | DOI today, access from memory |
| 6 | CODE-test | Direct download, no account | CC BY 4.0 | 827 ECGs | Partial (test set only) | today |
| 7 | Conduction-abnormality test set (Mendeley Data) | Direct download | CC BY 4.0 | 828 ECGs | Partial (test set only) | today |
| 8 | MIMIC-IV-ECG | Direct download, no account | ODbL 1.0 | about 800,000 ECGs / 160,000 patients | Partial (machine labels) | today |

## Details

**1. PTB-XL** — https://physionet.org/content/ptb-xl/1.0.3/
- **Contents:** 10-second clinical 12-lead ECGs, "annotated by up to two cardiologists", with recommended train/test folds.
- **Your classes (from memory):** about 1,500 AF, 800 first-degree AV block, 540 each of complete LBBB and RBBB, and 1,100 incomplete RBBB. Second- and third-degree AV block have only about a dozen each.
- **Limits:** not every record was human-validated (filter on `validated_by_human`), and it is a single German source from 1989–1996.
- **Papers:** the data descriptor (https://doi.org/10.1038/s41597-020-0495-6) and a benchmark with baselines (https://doi.org/10.1109/jbhi.2020.3022989).

**2. Chapman–Shaoxing–Ningbo** — https://physionet.org/content/ecg-arrhythmia/1.0.0/
- **Contents:** 12-lead ECGs at 500 Hz from two Chinese hospitals; 10-second length is from memory.
- **Labels:** "a licensed physician labeled the rhythm and other cardiac conditions. Another licensed physician performed a secondary validation", with a senior physician settling disagreements. These are physicians, not stated to be cardiologists.
- **Note:** it supersedes the 2019 figshare release of 10,646 patients, which is a subset.

**3. Challenge 2021 collection** — https://physionet.org/content/challenge-2021/1.0.3/
- **Contents:** one download pooling PTB-XL, Chapman–Shaoxing, Ningbo, CPSC2018, Georgia and others, with labels harmonised to SNOMED CT codes.
- **Why use it:** it is the easiest route to multi-site training, and the Georgia (US) set exists only here.
- **Limits:** it contains #1 and #2, so never treat those as independent test data. Label quality varies by source, and some parts are longer than 10 seconds.
- **Paper:** a meta-analysis of the 2020 edition (https://doi.org/10.3389/fphys.2021.811661).

**4. CODE-15%** — https://zenodo.org/records/4916206
- **Contents:** Brazilian telehealth ECGs with six binary labels; the page confirms an AF column, and RBBB, LBBB and first-degree AV block are from memory.
- **Labels (from memory):** derived from the cardiologist report combined with automated analysis, with manual review of disagreements.
- **Limits:** traces are 7–10 seconds at 400 Hz, zero-padded to 4,096 samples. There is no higher-degree AV block label.
- **Paper:** https://doi.org/10.1038/s41467-020-15432-4.

**5. SPH** — https://doi.org/10.6084/m9.figshare.c.5779802
- **Contents:** records of 10–60 seconds at 500 Hz, labelled with AHA/ACC/HRS standard statements.
- **Check first:** open the page in a browser to confirm it downloads freely, and read the descriptor for who assigned the labels.

**6. CODE-test** — https://zenodo.org/records/3765780
- **Labels:** the cleanest on the list: "When the cardiologist 1 and cardiologist 2 agree, the common diagnosis was considered as gold standard", with a third senior specialist as tiebreak.
- **Use:** a test set. It comes from the same network as CODE-15%, so it is not fully external for models trained on that.

**7. Conduction test set** — https://doi.org/10.17632/6jd4rn2z9x.1
- **Labels:** "Three board-certified actively-practicing cardiologists … annotated by consensus".
- **Limits:** I did not read the exact class list, and it mixes in some Holter-derived traces.

**8. MIMIC-IV-ECG** — https://physionet.org/content/mimic-iv-ecg/1.0/
- **Contents:** 10-second 12-lead ECGs at 500 Hz, 97 GB; the page says "the project access has been changed to open".
- **Limits:** the open labels are the ECG machine's automated statements. The cardiologist reports and the ICD label extension need credentialed access.
- **Use:** pretraining, not ground truth. ODbL means any derived database must carry the same licence.

## Known, not confirmed
- **ZZU critical-value ECG dataset** (https://doi.org/10.6084/m9.figshare.31229326.v3): 20,126 records from 9,785 patients, 7–198 seconds, 15 critical arrhythmia types "labeled and verified by professional physicians". The DOI is registered with CC BY 4.0, but figshare blocked the page. It might add high-degree AV block cases, so check the class list.
- **CPSC2018 standalone:** the registry record I found returned a 404, and I did not verify the official challenge site. The data is inside #3 anyway.

## Not recommended, and why
- **KURIAS-ECG:** needs a signed agreement, and the page says the authors "have asked for downloads to be disabled until further notice".
- **MIMIC-IV-ECG-Ext-ICD and Harvard-Emory ECG Database:** "Only credentialed users who sign the DUA can access the files."
- **Full CODE cohort (2.3 M ECGs):** by application to the authors (from memory).
- **EchoNext:** needs a signed agreement, and its labels are structural heart disease.
- **PTB Diagnostic, MIT-BIH Arrhythmia, MIT-BIH AF, Challenge 2017, INCART:** open, but too small or not 10-second resting 12-lead recordings.
- **ZZU pediatric ECG database:** children aged 0–14.
- **Hugging Face copies of these sets:** third-party mirrors, one of which states licence terms that do not match the source. Use the official hosts.

## What I could not find
- No open set has enough second- or third-degree AV block for a dedicated classifier. Pooling #1, #2 and #5 is the best you can do without an application.
- No open North American set has cardiologist-confirmed labels.
- Dataset-specific paper lookups for CODE-15%, Chapman and SPH returned nothing useful, so those entries have fewer usage references.

## Next step
Download PTB-XL and the Chapman–Shaoxing–Ningbo set today, train on one and test on the other, and use CODE-test as a cardiologist-consensus check. Add CODE-15% when you need scale. Open data may still need an exemption determination from your institution, so ask early.

The interactive page with per-requirement evidence is at `/private/tmp/e-uHEHsn/home/cwd/dataset-shortlist.html`.