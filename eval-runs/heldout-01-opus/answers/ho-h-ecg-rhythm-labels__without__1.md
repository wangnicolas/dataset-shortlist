You have several good options that need no credentialing. Your three targets (AF, bundle branch blocks and AV block) are among the best-labeled findings in public ECG data.

## Top picks

**1. PTB-XL (PhysioNet). Start here.**
- About 21,800 10-second 12-lead ECGs from about 18,900 patients, at 500 Hz and 100 Hz.
- Open access under CC BY 4.0. You can download it directly or with `wget` from physionet.org.
- Labels are SCP-ECG statements written by up to two cardiologists. A `validated_by_human` flag tells you which reports were checked by a person.
- It includes AFIB, CLBBB, CRBBB, IRBBB, LAFB/LPFB, IVCD, 1AVB, 2AVB and 3AVB.
- It comes with recommended patient-level folds (`strat_fold`), and folds 9 and 10 have the highest label quality. That makes it the standard benchmark, so your results will be comparable to published work.

**2. CODE-15% (Zenodo, Ribeiro et al.). Very close to your exact target set.**
- About 346,000 exams from about 234,000 Brazilian patients. Recordings are 7–10 seconds at 400 Hz.
- CC BY 4.0, direct download.
- The labels are exactly 1st-degree AV block, RBBB, LBBB, sinus bradycardia, AF and sinus tachycardia.
- The caveat is that training labels came from automated analysis (Glasgow and Minnesota) combined with the cardiologist's text report. They are good but not individually confirmed.
- **Pair it with the CODE test set** (also on Zenodo): 827 ECGs annotated by consensus of 2–3 cardiologists, with the same six labels. It's a clean held-out evaluation set.

**3. Chapman-Shaoxing / Ningbo (PhysioNet: "A large scale 12-lead electrocardiogram database for arrhythmia study")**
- About 45,000 10-second 12-lead ECGs at 500 Hz, open access.
- Labeled by physicians using SNOMED-CT codes, with strong rhythm coverage including AF, atrial flutter and SVT, plus AV blocks and BBBs.
- Early versions had some known label errors, so use the latest version.

## Also worth knowing
- **PhysioNet/CinC Challenge 2021 data:** open access, about 88,000 recordings combining PTB-XL, Chapman, Ningbo, Georgia (about 10,000 10-second ECGs) and CPSC 2018. Everything is already mapped to SNOMED-CT, which saves harmonization work. Watch out for two things: PTB-XL and Chapman are included in it, so don't count them twice, and CPSC and INCART recordings aren't 10 seconds long.
- **SPH / Shandong Provincial Hospital (figshare, CC BY 4.0):** about 25,800 ECGs with AHA-standard statements from physicians.
- **MIMIC-IV-ECG:** about 800,000 ECGs, and the waveforms are openly downloadable. However, the open part only has machine-generated reports. The cardiologist reports are in the credentialed part of MIMIC, so it's useful for pretraining but not for your labels.

## Practical cautions
- **Rare classes:** 2nd- and 3rd-degree AV block have only tens of examples per dataset. Plan to combine datasets or treat "high-grade AV block" as one class.
- **Split by patient**, not by recording, to avoid leakage.
- **Harmonize across datasets:** sampling rate (400 vs 500 Hz), units and lead order. Map labels to SNOMED-CT, using the Challenge 2021 mapping tables.
- **Ethics:** "open access" removes the data use agreement, but your institution may still want an IRB "not human subjects research" determination for de-identified public data. It's usually quick, so it's worth a short email now.

**My recommendation:** train and validate on PTB-XL, add Chapman/Ningbo for more AF and conduction cases, and use the CODE test set as a cardiologist-confirmed external test.

I gave these sizes and license terms from memory and didn't check the live pages, so confirm them on each download page before you rely on them.