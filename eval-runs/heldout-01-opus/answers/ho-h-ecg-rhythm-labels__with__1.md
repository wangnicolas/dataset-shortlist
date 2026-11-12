You have several good options. All of the ones below are open downloads with no account, no data use agreement and no credentialing, so you can start today. I checked them on 2026-11-12 through the PhysioNet and Zenodo registry records and their landing pages.

## What I assumed you need
- **R1 (must):** standard 10-second, 12-lead resting ECG waveforms
- **R2 (must):** labels for atrial fibrillation, left/right bundle branch block and AV block
- **R3 (preferred):** labels assigned or confirmed by cardiologists or physicians
- **R4 (must):** a few thousand recordings or more, downloadable this week with nothing to sign. I assumed CC BY licences are fine (they allow academic and commercial use with attribution).

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PTB-XL v1.0.3 | Open download, minutes | CC BY 4.0 | 21,799 ECGs | Strong | today |
| 2 | Large-scale 12-lead arrhythmia DB (Chapman–Shaoxing–Ningbo) | Open download, minutes | CC BY 4.0 | 45,152 ECGs | Strong | today |
| 3 | PhysioNet/CinC Challenge 2021 | Open download, minutes | CC BY 4.0 | ~88k recordings (pooled) | Strong | today |
| 4 | SPH (Shandong Provincial Hospital) | Open on figshare, minutes | CC BY 4.0 | ~25,770 ECGs | Strong | DOI today; contents from memory |
| 5 | CODE-15% | Open download, minutes | CC BY 4.0 | 345,779 exams | Partial (noisier labels) | today |
| 6 | CODE-test | Open download, minutes | CC BY 4.0 | 827 exams | Test set only | today |
| 7 | MIMIC-IV-ECG | Open download (~90 GB) | ODbL | ~800k ECGs | Partial (machine labels only) | today |

## Details
**1. PTB-XL**: https://physionet.org/content/ptb-xl/1.0.3/
- **Contents:** 10-second 12-lead recordings at 500 Hz and 100 Hz, with SCP-ECG codes. The codes include AFIB, CLBBB, CRBBB, IRBBB, 1AVB, 2AVB and 3AVB (the code names are from memory). It comes with recommended train/test splits, so your results will be comparable with published work.
- **Labels:** the page says the records were "annotated by up to two cardiologists". Some report strings came from the ECG device instead, so use the `validated_by_human` column to filter.
- **Weak spot:** there are only a few dozen 2nd- and 3rd-degree AV block cases.
- **Used by:** Wagner et al. 2023 (JBHI, 10.1109/jbhi.2023.3271858), with CPSC2018 + PTB-XL, and a 2021 Entropy paper (10.3390/e23091121). An OSF pre-registration (10.17605/osf.io/m9ur2) targets almost exactly your label set (1AVB, CRBBB, CLBBB, AF) on PTB-XL.
- **PTB-XL+** (https://physionet.org/content/ptb-xl-plus/1.0.1/, open) adds ECG features and labels from automatic interpretation software for the same recordings.

**2. Chapman–Shaoxing–Ningbo database**: https://physionet.org/content/ecg-arrhythmia/1.0.0/
- **Contents:** 10-second 12-lead recordings at 500 Hz, labeled with SNOMED CT codes. The codes include AF, atrial flutter, LBBB, RBBB and 1st/2nd-degree AV block (from memory).
- **Labels:** the page says one licensed physician labeled each recording, a second physician validated it, and a senior physician decided disagreements. That is the strongest labeling process on this list at this size.
- **Caveat:** all patients are from China.
- Use this PhysioNet release, not the 2025 Zenodo or Hugging Face re-uploads. It replaces the original 10,646-patient Chapman release on figshare.

**3. PhysioNet/CinC Challenge 2021**: https://physionet.org/content/challenge-2021/1.0.3/
- **Contents:** about 88k recordings pooled from CPSC2018, CPSC-Extra, Georgia (~10k, US), PTB-XL, Chapman, Ningbo, INCART and PTB, all mapped to shared SNOMED codes. The main reason to use it is the Georgia and CPSC data, which give you populations outside China and Germany.
- **Cautions:**
  - CPSC recordings run 6–60 seconds, and INCART is 30-minute recordings, so filter or crop them.
  - PTB-XL and Chapman appear here as well. Remove the duplicates before you split your data, or the same recordings can end up in both training and test sets.
  - The hidden test sets were never released.
  - The source makeup and the ~88k count are from memory.

**4. SPH**: https://doi.org/10.6084/m9.figshare.c.5779802
- I confirmed the DOI, its registered title ("A large-scale multi-label 12-lead electrocardiogram database with standardized diagnostic statements") and the CC BY 4.0 licence.
- figshare blocked my automated check of the page, so the rest is from memory: 25,770 ECGs of 10–60 seconds, AHA-standard diagnostic statements covering AF, bundle branch blocks and AV blocks, published in Sci Data 2022.
- Open it in a browser to confirm, then download the HDF5 files.

**5. CODE-15%**: https://zenodo.org/records/4916206
- **Contents:** 345k Brazilian telehealth exams with yes/no columns for 1dAVb, RBBB, LBBB and AF (confirmed on the page), plus sinus bradycardia and sinus tachycardia. Data is HDF5 in 18 parts.
- **Labels:** these come from automatic analysis software plus text from the cardiologists' reports (from memory, Ribeiro et al. 2020). They are not individually cardiologist-confirmed. The page itself describes `normal_ecg` as coming from the "automatic annotation system".
- **Gap:** there is no label for 2nd/3rd-degree AV block.
- **Use it for:** pre-training or scale.
- **Paper:** Ribeiro 2020, Nat Commun (10.1038/s41467-020-15432-4).

**6. CODE-test**: https://zenodo.org/records/3765780
- 827 exams with the same classes as CODE-15%. The page says two cardiologists annotated each one, with a third senior specialist resolving disagreements.
- That makes it a good external gold-standard test set.

**7. MIMIC-IV-ECG**: https://physionet.org/content/mimic-iv-ecg/1.0/
- **Contents:** about 800k 10-second 12-lead ECGs at 500 Hz, open access. The open release only has machine measurements and machine-generated interpretation statements (the statements are from memory).
- **The catch:** the page says the cardiologist reports are part of MIMIC-IV-Note, and that "only members who are part of our consortium can access the cardiologist reports / notes". Getting them means credentialing, which is not possible for you this week.
- **Use it for:** self-supervised pre-training only.

## Known, not confirmed
- **Exact label counts per class**, especially for high-grade AV block. I did not tally them. Count them from `ptbxl_database.csv` and the SNOMED headers before you design your classes.
- **SPH contents**: see #4 above.

## Not recommended, and why
- **Harvard-Emory ECG Database:** the page says "Only credentialed users who sign the DUA can access the files."
- **Challenge 2020:** the 2021 release contains all of it.
- **INCART:** only 75 records, each 30 minutes long.
- **MIT-BIH AF and CinC 2017:** 2-lead or single-lead recordings, not 12-lead.
- **PTB Diagnostic:** 549 records, mostly heart attack cases.
- **Sami-Trop:** its labels are age and mortality only.
- **Hugging Face and Zenodo re-uploads** of PTB-XL, Chapman or MIMIC: unofficial copies. Use the originals.

## What I could not find
No open dataset has many 2nd- or 3rd-degree AV block cases; expect tens to low hundreds per source. You will probably have to merge sources (PTB-XL + Chapman + Georgia/CPSC + SPH) or treat high-grade AV block as a single combined class. I searched PhysioNet, Zenodo, DataCite, OpenAIRE, Hugging Face and the literature (193 candidates). I did not separately check Chinese competition portals such as Tianchi.

## Next step
Download PTB-XL and the Chapman–Ningbo database today. They total about 67k ECGs with physician-validated labels for all your target classes. Map both to SNOMED codes, as the 2021 Challenge did. Then add Georgia and CPSC from the Challenge release for populations from more places, and keep CODE-test as an external test set. All of these are CC BY 4.0, so you only need to cite the datasets. Access rules can change, so recheck before publishing.

The interactive shortlist, where you can filter datasets and export an access plan, is at `/private/tmp/e-JkFyeE/home/cwd/dataset-shortlist.html`.