You can start today: six open datasets fit, and the best first download is PTB-XL (21,799 ten-second ECGs, cardiologist-annotated, no account needed). The main gap is that no open dataset has many cardiologist-confirmed second- or third-degree AV block cases.

## What I assumed you need
- **R1 (must):** 12-lead resting ECG waveforms of about 10 seconds.
- **R2 (must):** diagnostic labels covering AF, bundle branch blocks and AV block.
- **R3 (nice):** labels assigned or confirmed by cardiologists.
- **R4 (must):** at least a few thousand recordings.
- **R5 (must):** downloadable now, with no application, credentialing, data use agreement or ethics approval. I treated a click-through agreement as failing this.
- **R6 (assumed):** licence allows research use and publication.

## Shortlist
Access and licence were checked today (12 Nov 2026) for every row; "from memory" marks label or count details I did not re-read.

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PTB-XL | Direct download, no account | CC BY 4.0 | 21,799 ECGs, 3.2 GB | Strong | today; class counts from memory |
| 2 | Chapman–Shaoxing–Ningbo | Direct download, no account | CC BY 4.0 | 45,152 ECGs, 5.5 GB | Strong | today; AF and AV-block labels from memory |
| 3 | PhysioNet/CinC Challenge 2021 | Direct download, no account | CC BY 4.0 | about 88,000 ECGs, 13.6 GB | Strong | today; composition from memory |
| 4 | SPH (Shandong Provincial Hospital) | Direct download from figshare | CC BY 4.0 | 25,770 ECGs | Strong | registry record today; page not readable by script |
| 5 | CODE-15% | Direct download, no account | CC BY 4.0 | 345,779 exams, 46 GB | Partial | today; label provenance from memory |
| 6 | CODE-test | Direct download, no account | CC BY 4.0 | 827 ECGs | Partial (test set only) | today |
| 7 | Mendeley conduction test set | Direct download (not tested) | CC BY 4.0 | 828 ECGs | Partial (test set only) | registry record today |
| 8 | MIMIC-IV-ECG | Direct download, no account | ODbL 1.0 | about 800,000 ECGs, 97 GB | Partial (no expert labels) | today |

## Details

**1. [PTB-XL](https://physionet.org/content/ptb-xl/1.0.3/)**
- **Contents:** "21799 clinical 12-lead ECGs from 18869 patients of 10 second length", from one German site.
- **Labels:** "annotated by up to two cardiologists", but some reports are "automatic interpretation by ECG-device". Filter on the `validated_by_human` column.
- **Classes (from memory):** about 1,500 AF, about 540 each of complete LBBB and RBBB, about 800 first-degree AV block, and under 20 each of second- and third-degree.
- **Splits:** use the provided `strat_fold` column, which keeps each patient in one fold.
- **Papers:** [data descriptor](https://doi.org/10.1038/s41597-020-0495-6), [benchmarks](https://doi.org/10.1109/jbhi.2020.3022989), [AF detection](https://doi.org/10.1016/j.ijcard.2020.11.053).

**2. [Chapman–Shaoxing–Ningbo](https://physionet.org/content/ecg-arrhythmia/1.0.0/)**
- **Contents:** "12-lead ECGs of 45,152 patients with a 500 Hz sampling rate", 10-second readings, from two Chinese hospitals.
- **Labels:** "a licensed physician labeled the rhythm and other cardiac conditions. Another licensed physician performed a secondary validation", with a senior physician resolving disagreements. The page says physicians, not cardiologists.
- **Classes:** RBBB and LBBB are named on the page; AF and AV-block labels are from memory.
- **Papers:** [data descriptor of the first part](https://doi.org/10.1038/s41597-020-0386-x), [rhythm classification](https://doi.org/10.1038/s41598-020-59821-7).

**3. [PhysioNet/CinC Challenge 2021](https://physionet.org/content/challenge-2021/1.0.3/)**
- **Contents:** one collection bundling PTB-XL, Chapman–Shaoxing, Ningbo, CPSC 2018, Georgia and others, with labels harmonised to SNOMED CT codes (composition from memory).
- **Why use it:** it is the only route I know to Georgia (about 10,000 US ECGs) and CPSC 2018, and it makes cross-site testing easy.
- **Caveats:** it contains datasets 1 and 2, so de-duplicate before combining. Some sources are not 10 seconds, and label quality varies by source.
- **Papers:** [organisers on label heterogeneity](https://doi.org/10.1088/1361-6579/ac79fd), [meta-analysis of the 2020 methods](https://doi.org/10.3389/fphys.2021.811661).

**4. [SPH](https://doi.org/10.6084/m9.figshare.c.5779802.v1)**
- **Contents:** "25770 12-lead clinical ECG records from 24666 patients", 500 Hz, "length of records ranges from 10 to 60 seconds", so crop to 10 seconds.
- **Labels:** 44 primary statements in the AHA/ACC/HRS standard. Cardiologist labelling is from memory; I did not check per-class counts.
- **Why use it:** it is independent of the Challenge collection, so it works as an external test set.
- **Access:** open the link in a browser; figshare blocks scripts.
- **Paper:** [data descriptor](https://doi.org/10.1038/s41597-022-01403-5).

**5. [CODE-15%](https://zenodo.org/records/4916206)**
- **Contents:** "345 779 exams from 233 770 patients" from Brazilian primary care, at 400 Hz; traces are 7 or 10 seconds, zero-padded.
- **Labels:** columns for AF, RBBB, LBBB and first-degree AV block only.
- **Label provenance (from memory):** derived from the reporting cardiologist's text combined with automated analysis, with manual review only on disagreement.
- **Paper:** [the CODE model and labelling](https://doi.org/10.1038/s41467-020-15432-4).

**6. [CODE-test](https://zenodo.org/records/3765780)**
- **Contents:** 827 tracings with the same six classes as CODE-15%.
- **Labels:** the cleanest on this list: "When the cardiologist 1 and cardiologist 2 agree, the common diagnosis was considered as gold standard", otherwise a third senior specialist decided.
- **Use:** evaluation only.

**7. [Mendeley conduction test set](https://doi.org/10.17632/6jd4rn2z9x.1)**
- **Contents:** 828 "standard 10-second, 12-lead ECGs" at 500 Hz.
- **Labels:** "Three board-certified actively-practicing cardiologists ... annotated by consensus". I did not read the class list, so check it before relying on it.

**8. [MIMIC-IV-ECG](https://physionet.org/content/mimic-iv-ecg/1.0/)**
- **Contents:** about 800,000 ECGs: "12 leads and are 10 seconds in length", 500 Hz.
- **Access:** "the project access has been changed to open instead of requiring credentialling".
- **Labels:** machine statements only in the open release. The cardiologist reports are consortium-only, and the ICD label set needs credentialing.
- **Use:** pretraining now; labelled work later if you get credentialed. ODbL is share-alike for derived datasets.

## Known, not confirmed
- **[ZZU critical-value ECG dataset](https://doi.org/10.6084/m9.figshare.31229326.v3):** 20,126 records, 7–198 seconds, 15 critical arrhythmias, "labeled and verified by professional physicians", CC BY 4.0. It might add high-grade AV block cases. The DOI is registered, but figshare refused automated reading, so check the class list in a browser.
- **CPSC 2018 original site:** it returned a server error today. The data (6,877 records, from memory) is inside the Challenge 2021 collection.

## Not recommended, and why
- **[MIMIC-IV-ECG-Ext-ICD](https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/):** "Only credentialed users who sign the DUA can access the files".
- **[Harvard-Emory ECG Database](https://bdsp.io/content/heedb/):** credentialed access plus a data use agreement.
- **[CODE full dataset](https://doi.org/10.17044/scilifelab.15169716.v1):** individual request, then a data user agreement.
- **[KURIAS-ECG](https://physionet.org/content/kurias-ecg/1.0/):** "Only registered users who sign the specified data use agreement can access the files". This is a click-through with no reviewer, so it becomes usable if you relax R5.
- **[EchoNext](https://physionet.org/content/echonext/1.1.1/):** needs a signed agreement, and its labels are structural heart disease, not rhythm or conduction.
- **[Challenge 2020](https://physionet.org/content/challenge-2020/1.0.2/) and the [Chapman figshare release](https://doi.org/10.6084/m9.figshare.c.4560497):** open, but contained in datasets 3 and 2.
- **[Sami-Trop](https://zenodo.org/records/4905618):** open, but annotated with age and mortality only.
- **MIT-BIH, INCART, Challenge 2017, LUDB:** ambulatory, single-lead, or too small.
- **Hugging Face and Zenodo re-uploads:** third-party copies; use the official sources.

## What I could not find
- An open dataset with many cardiologist-confirmed second- or third-degree AV block cases. Open data mainly supports first-degree AV block.
- A large open US or European set with uniformly cardiologist-confirmed labels beyond PTB-XL.

## Next step
Download PTB-XL and the Chapman–Shaoxing–Ningbo set today (under 9 GB together) and train on those. Hold out SPH and CODE-test as external test sets, and add Georgia from the Challenge 2021 collection for a US population. Even for open de-identified data, ask your institution early whether it needs an exempt determination before you publish.

The interactive shortlist is at `/private/tmp/e-GYPTSy/home/cwd/dataset-shortlist.html`.