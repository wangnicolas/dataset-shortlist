Several large 12-lead ECG sets meet your constraints. You can download all of them today with no application, credentialing or data use agreement. I checked each registry record and landing page on 2026-11-11/12. I did not render the interactive shortlist page or run the "papers that used it" lookups, to keep this short.

## What I assumed you need
- **R1 (must):** 12-lead, resting, about 10 s recordings.
- **R2 (must):** labels for AF and conduction disorders (LBBB, RBBB, AV block), assigned or confirmed by physicians.
- **R3 (must):** a few thousand recordings or more.
- **R4 (must):** direct download, no application or credentialing.
- **R5 (nice):** a standard label vocabulary and train/test splits.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [PTB-XL](https://physionet.org/content/ptb-xl/1.0.3/) | Direct download, no account | CC-BY-4.0 | ~21.8k records | Strong | Access and licence today; counts from memory |
| 2 | [Chapman-Shaoxing/Ningbo ("large scale 12-lead ECG database for arrhythmia study")](https://physionet.org/content/ecg-arrhythmia/1.0.0/) | Direct download | CC-BY-4.0 | ~45k records (memory) | Strong | Access and licence today; count from memory |
| 3 | [PhysioNet/CinC Challenge 2020 training data](https://physionet.org/content/challenge-2020/1.0.2/) | Direct download | CC-BY-4.0 | >40k (memory) | Strong for pooling, mixed lengths | Access and licence today |
| 4 | [Challenge 2021 training data](https://physionet.org/content/challenge-2021/1.0.3/) | Direct download | CC-BY-4.0 | Larger superset of #3 (memory) | Same as #3 | Access and licence today |
| 5 | [CODE-15%](https://zenodo.org/records/4916206) | Direct download from Zenodo | CC-BY-4.0 | 345,779 exams | Good for scale, label quality needs care | Size, access and licence today |
| 6 | [CODE-test](https://zenodo.org/records/3765780) | Direct download | CC-BY-4.0 | 827 tracings | Too small for training; a good cardiologist-labelled test set | Today |

## Details
**1. PTB-XL** is the safest first choice.
- The page says "The raw waveform data was annotated by up to two cardiologists, who assigned potentially multiple ECG statements to each record."
- It comes with recommended 10-fold splits that respect patient assignment.
- From memory, the statement list includes AFIB, CLBBB, CRBBB, ILBBB, IRBBB and first-, second- and third-degree AV block. Check the `scp_statements.csv` file for the exact codes.
- From memory, records are 10 s at 100 Hz and 500 Hz.

**2. Chapman-Shaoxing/Ningbo** has a documented labelling process.
- The page says "a licensed physician labeled the rhythm and other cardiac conditions", a second physician validated, and "a senior physician intervened" on disagreements.
- Its settings are consistent with the Challenge 2021 databases.
- A smaller Shaoxing-only copy is also on [Zenodo](https://zenodo.org/records/16789324). I haven't confirmed which subset it holds; from memory it is about 10.6k records.
- It is strong for AF and bundle branch blocks. AV block is rarer.

**3 and 4. The Challenge sets** pool several sources under one SNOMED-CT label scheme.
- The 2020 page lists the sources, including CPSC 2018 (6,877 recordings), CPSC-Extra (3,453) and Georgia (10,344). Georgia is confirmed as 10 s at 500 Hz.
- CPSC recordings run 6–60 s, so you'd need to crop or filter them.
- Label provenance differs by source. Some labels are physician-assigned and others come from machine-read reports plus review. Check each source's description before calling every label cardiologist-confirmed.
- These sets are useful for external validation across hospitals and countries.

**5. CODE-15%** is the largest but the weakest on your "cardiologist-confirmed" criterion.
- From memory, its AF and conduction labels (including 1st-degree AV block, RBBB and LBBB) come partly from automatic or report-derived annotation, not manual review of each tracing.
- I could not confirm that on the page today, so check the paper before relying on it.
- It is better for pre-training.
- Use CODE-test as the matching expert-labelled evaluation set. The page says a third senior specialist resolved disagreements.

## Known, not confirmed
- The exact counts for #2, #3 and #4 and the AV-block counts in each set are from memory. Count them yourself from the header files before you plan a study.
- I did not check whether CODE-15% has a click-through step beyond the Zenodo download. The record is marked open.

## Not recommended, and why
- **MIT-BIH, INCART and the AF Challenge 2017 set:** these are single-lead, Holter or non-10 s data, not standard resting 12-lead ECGs.
- **KURIAS-ECG:** it needs a free PhysioNet account and restricted-data terms, so it fails your "this week, no credentialing" rule.
- **Hugging Face copies** of these datasets: use the official sources above. The copies' provenance and terms are unclear.

## What I could not find
Nothing on the open list is large and rich in cardiologist-verified second- and third-degree AV block. PTB-XL and Challenge 2021 are your best bets for that class, and it will be small.

## Next step
1. Download PTB-XL and Chapman/Ningbo first. Both are one `wget` or the `wfdb` Python package away.
2. Build your label map from the SNOMED codes or SCP statements.
3. Count positives per class.

I can write the download and label-extraction script if you want.