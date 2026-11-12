Three datasets fit, and all are on PhysioNet as open access (CC BY 4.0). The PhysioNet pages for each say "Anyone can access the files, as long as they conform to the terms of the specified license." That means no account, credentialing, or data use agreement. I checked the pages for all three, but I haven't downloaded anything.

## Recommendations

**1. PTB-XL (best for cardiologist labels)**
- **Size:** 21,799 ten-second, 12-lead ECGs from 18,869 patients, about 3 GB.
- **Labels:** Up to two cardiologists annotated each record with SCP-ECG statements (71 in total, covering diagnostic, form and rhythm categories). A technical expert validated the signals. Folds 9 and 10 had at least one human evaluation, so their label quality is particularly high. That makes them a natural test set.
- **Your targets:** The page doesn't list the individual statements, so I couldn't confirm AF, bundle branch block or AV block labels from it. From memory, `scp_statements.csv` includes AFIB, CLBBB, CRBBB and 1AVB/2AVB/3AVB. Check that file first.
- **Download:** `physionet download ptb-xl --version 1.0.3`, or `aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ DEST`.

**2. Chapman-Shaoxing + Ningbo ("ecg-arrhythmia" v1.0.0; best for AF volume)**
- **Size:** 45,152 twelve-lead ECGs at 500 Hz, about 5.1 GB uncompressed (2.3 GB ZIP). A search result (not the PhysioNet page) says the Chapman-Shaoxing cohort alone has 3,889 AF subjects.
- **Labels:** A licensed physician labeled each recording, a second physician validated, and a senior physician settled disagreements. They are stored as SNOMED-CT codes in the `.hea` headers.
- **Download:** `physionet download ecg-arrhythmia --version 1.0.0`, or the `aws s3 sync --no-sign-request` command with `s3://physionet-open/ecg-arrhythmia/1.0.0/`.
- **Caveat:** The Scientific Data paper describes the first 10,646 patients as 10-second, 12-lead recordings. I didn't confirm the same for the Ningbo portion.

**3. PhysioNet/CinC Challenge 2021 training set (one SNOMED-coded bundle)**
- **Size:** More than 88,000 twelve-lead training ECGs, 12.6 GB. It includes CPSC 2018 and CPSC-Extra, Georgia, Chapman-Shaoxing/Ningbo, PTB/PTB-XL and INCART.
- **Why use it:** Several institutions in one uniform format with SNOMED-CT labels, which is useful for testing generalization across sites.
- **Download:** `physionet download challenge-2021 --version 1.0.3`.
- **Caveat:** The page says label quality varies by source, and some labels are human-overread machine labels. Use PTB-XL or ecg-arrhythmia if you need cardiologist-confirmed labels.

## Things to watch
- **Overlap:** The Challenge bundle already contains PTB-XL and Chapman/Ningbo. Don't combine it with those two datasets, or you'll get duplicates and leakage between train and test.
- **Recording length:** Not every Challenge source is a clean 10-second, 12-lead recording. For example, INCART is cut from Holter recordings. I'd drop INCART or check durations.
- **Label mapping:** PTB-XL uses SCP codes and the other two use SNOMED-CT, so you'll need a mapping table to harmonize them.
- **Version number:** The PTB-XL page gives two counts (21,799 and 21,801). I used 21,799, which the page and later papers mainly cite.

My suggestion is to start with PTB-XL, using folds 9 and 10 as your cleanly labeled test set. Then add ecg-arrhythmia for more AF and conduction cases and external validation.

Sources:
- [PTB-XL v1.0.3 (PhysioNet)](https://physionet.org/content/ptb-xl/1.0.3/)
- [PTB-XL paper (Scientific Data)](https://www.nature.com/articles/s41597-020-0495-6)
- [ecg-arrhythmia v1.0.0 (PhysioNet)](https://physionet.org/content/ecg-arrhythmia/1.0.0/)
- [Chapman-Shaoxing paper (Scientific Data)](https://www.nature.com/articles/s41597-020-0386-x)
- [PhysioNet/CinC Challenge 2021 v1.0.3](https://physionet.org/content/challenge-2021/1.0.3/)
- [Challenge 2021 site](https://moody-challenge.physionet.org/2021/)