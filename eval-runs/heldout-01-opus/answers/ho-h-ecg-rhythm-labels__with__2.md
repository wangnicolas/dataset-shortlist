Several large datasets fit your constraints and can be downloaded today with no account, application or agreement. Everything below was checked on 2026-11-12 against the registry records and dataset pages unless it says "from memory". I didn't run the literature search for papers that used each dataset, to save time.

## What I assumed you need
- **R1 (must):** 10-second, 12-lead resting ECG waveforms
- **R2 (must):** labels for AF, right/left bundle branch block (RBBB/LBBB) and AV block
- **R3 (must):** at least a few thousand labelled recordings
- **R4 (must):** direct download with no application, data use agreement (DUA) or credentialing
- **R5 (nice to have):** labels assigned or confirmed by cardiologists
- I also assumed academic use. Every dataset below allows commercial use too.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | **PTB-XL** v1.0.3 | Open download, minutes | CC BY 4.0 | 21,799 ECGs | Strong; labels by cardiologists | today |
| 2 | **Chapman-Shaoxing + Ningbo** ("Large scale 12-lead ECG database for arrhythmia study") | Open download, minutes | CC BY 4.0 | 45,152 | Strong; labels by physicians, each checked by a second reader | today |
| 3 | **PhysioNet/CinC Challenge 2021** | Open download, minutes | CC BY 4.0 | >88,000 | Strong; collects 6 sources under one label scheme, quality varies by source | today |
| 4 | **SPH** (Shandong Provincial Hospital) | Open figshare download | CC BY 4.0 | 25,770 | Strong | registry record today; download terms from memory |
| 5 | **CODE-15%** (Brazil) | Open download from Zenodo | CC BY 4.0 | 345,779 | Partial: only 1st-degree AV block, noisier labels | today |
| 6 | **CODE-test** | Open download from Zenodo | CC BY 4.0 | 827 | Clean test set with cardiologist labels | today |
| 7 | **MIMIC-IV-ECG** | Open download, minutes | ODbL | ~800k | Partial: the open labels are machine reports | today |

## Details
1. **PTB-XL**: https://physionet.org/content/ptb-xl/1.0.3/
   - 10-second, 12-lead recordings at 500 or 100 Hz from 18,869 patients.
   - The page says the recordings were "annotated by up to two cardiologists." Labels follow the SCP-ECG scheme and include AFIB, CRBBB, CLBBB, IRBBB and 1/2/3AVB.
   - It comes with recommended 10-fold splits that keep each patient in one fold.
   - Download: `physionet download ptb-xl --version 1.0.3`, or `aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ .`
   - Few records have 2nd- or 3rd-degree AV block.
   - This is your best starting point.
2. **Chapman-Shaoxing + Ningbo**: https://physionet.org/content/ecg-arrhythmia/1.0.0/
   - 10-second recordings at 500 Hz with SNOMED-CT labels.
   - Per the page: "a licensed physician labeled the rhythm… Another licensed physician performed a secondary validation," and a senior physician settled disagreements. It doesn't say whether these physicians were cardiologists.
   - Download: `physionet download ecg-arrhythmia --version 1.0.0`
   - It contains the 2019 Chapman figshare release (10,646 patients), so use this version rather than both.
3. **Challenge 2021**: https://physionet.org/content/challenge-2021/1.0.3/
   - Collects CPSC2018, CPSC-Extra, Georgia, PTB/PTB-XL, INCART and Chapman-Ningbo under shared SNOMED labels.
   - It's the most useful set for testing on hospitals your model wasn't trained on. Training on some sources and testing on Georgia is common.
   - Two caveats are on the page itself: "some of the databases have human-overread machine labels… quality of the labels varies." CPSC recordings are 6 to 60 seconds and INCART recordings are 30 minutes.
   - It includes PTB-XL and Chapman-Ningbo, so remove duplicates if you also use #1 or #2.
4. **SPH**: https://doi.org/10.6084/m9.figshare.c.5779802
   - The Scientific Data paper describes 25,770 ECGs from 24,666 patients, labelled with AHA-standard statements. Two of the authors "reviewed the diagnostic statements."
   - Recordings are 10 to 60 seconds long and stored as HDF5, with code for splitting by patient.
   - Figshare refused the automated check, so open the link in a browser to download.
5. **CODE-15%**: https://zenodo.org/records/4916206
   - Six labels: 1dAVb, RBBB, LBBB, SB, AF and ST. It has no 2nd- or 3rd-degree AV block.
   - From memory: the labels come from telehealth cardiologist reports combined with automatic analysis, so they are noisier than PTB-XL's.
   - It's very good for pretraining.
6. **CODE-test**: https://zenodo.org/records/3765780
   - 827 ECGs. Two specialists labelled each one, and "a third senior specialist… decided the diagnosis" when they disagreed.
   - Too small to train on, but a strong independent test set.
7. **MIMIC-IV-ECG**: https://physionet.org/content/mimic-iv-ecg/1.0/
   - The waveforms and machine-generated report text are open. The page says the **cardiologist reports** are available only to "members who are part of our consortium."
   - Use it for self-supervised or weakly supervised pretraining. ODbL requires that databases you build from it and share are released under the same licence.

## Known, not confirmed
- **SPH and the 2019 Chapman figshare collection**: both DOIs resolve and the registry lists them as CC BY 4.0, but figshare blocked the automated check. From memory, both are direct downloads with no login. Open them in a browser to confirm.

## Not recommended, and why
- **MIT-BIH AF, Long-Term AF, Icentia11k and Challenge 2017**: one- or two-lead long-term or ambulatory recordings, not 12-lead resting ECGs.
- **Full CODE (about 2 million ECGs) and MIMIC-IV clinical data**: both need an application or credentialing.
- **PTB-XL+**: extra features and labels for PTB-XL rather than new recordings. It's a useful companion to #1.
- **LUDB**: only 200 records.
- **Hugging Face copies** (several came up in the search): unofficial. Use the original sources.

## What I could not find
No open source has many 2nd- or 3rd-degree AV block cases. To get enough examples, combine PTB-XL, Chapman-Ningbo, SPH and Challenge 2021.

## Next step
Download PTB-XL and Chapman-Ningbo today (both a few GB). Map their labels to a shared set (Challenge 2021 already uses SNOMED codes for this), train on them, and test on Georgia and CODE-test.

The interactive shortlist is at `/private/tmp/e-yh0NTT/home/cwd/dataset-shortlist.html`.