Your best starting point is **PTB-XL**, plus the **PhysioNet/CinC Challenge 2021** collection if you want more data. Both are open access, need no application or credentialing, and match your recording format. I haven't re-checked the dataset pages today, so confirm each one is still listed as "Open Access" before you plan around it.

## Top recommendations

**1. PTB-XL (PhysioNet), the best match**
- 21,799 recordings from 18,869 patients. All are 10 s, 12-lead, at 500 Hz (a 100 Hz version is included).
- Labels are SCP-ECG statements made by up to two cardiologists, with a flag showing whether a human validated each one. That matches your "assigned or confirmed by cardiologists" requirement.
- Relevant labels: AFIB, AFLT, CLBBB, CRBBB, ILBBB/IRBBB, 1AVB, 2AVB, 3AVB, LAFB/LPFB.
- It comes with 10 recommended patient-level folds (folds 9 and 10 have the highest label quality), so your results stay comparable with published benchmarks.
- License is CC BY 4.0. You can download it with `wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/`, about 3 GB. Check the page for the latest version number.

**2. PhysioNet/CinC Challenge 2020/2021 training data, for more volume**
- About 88,000 12-lead ECGs from several sources, all mapped to one shared SNOMED-CT label set covering AF, AFL, LBBB, RBBB, IRBBB, 1st-degree AV block, and more.
- The sources are PTB-XL, Chapman-Shaoxing, Ningbo, CPSC 2018, the Georgia 12-lead database (about 10,000 US recordings) and the older PTB/INCART sets.
- Data from several hospitals lets you test how well a model trained at one site works at another, which reviewers care about.
- Caveats: CPSC recordings run 6–60 s, so you'll need to crop or pad them; INCART is 30-minute Holter-style data, so leave it out. Label quality also varies by source.

**3. Chapman-Shaoxing / Ningbo (PhysioNet: "A large scale 12-lead electrocardiogram database for arrhythmia study")**
- About 45,000 recordings, 10 s, 500 Hz, labeled by licensed physicians with SNOMED codes, including AV blocks and bundle branch blocks. It's heavy on rhythm labels, which suits AF.
- License is CC BY 4.0. Note that it overlaps with the Challenge collection above.

**4. CODE-15% (Zenodo), for large-scale pretraining**
- About 345,000 exams from 233,000 Brazilian patients, CC BY 4.0, no application needed.
- It has 6 labels, including AF, 1st-degree AV block, RBBB and LBBB.
- The labels come from automated analysis combined with text reports, not careful cardiologist review, so they're noisier. Recording length also varies (7–10 s).
- The separate CODE-test set (827 exams annotated by several cardiologists) makes a good external test set for these labels.

**Possible addition: MIMIC-IV-ECG.** It has about 800,000 10-s 12-lead ECGs and, as far as I know, the waveforms and machine-generated reports are open access. The labels are machine reports, though, and linking them to clinical data requires credentialing. Treat it as optional.

## Things to plan for

- **2nd- and 3rd-degree AV block are rare everywhere.** PTB-XL has only about a dozen examples of each. If high-grade AV block matters to you, pool data across sources, consider grouping the AV block classes, and report how much your confidence intervals widen with so few cases.
- **Split by patient, not by recording.** PTB-XL and CODE have repeat recordings from the same patients.
- **"Open access" still has terms.** CC BY means you must credit the dataset and cite its paper. More importantly, many institutions still want a short determination that secondary use of public, de-identified data is "not human subjects research." That's usually a quick form, not a full ethics review, but check with your IRB or ethics office before you publish.

**Suggested setup:** start with PTB-XL for development and benchmarking. Add the Challenge 2021 sources for training volume and testing on unseen hospitals, and use CODE-test as an external check for AF, bundle branch blocks and 1st-degree AV block.