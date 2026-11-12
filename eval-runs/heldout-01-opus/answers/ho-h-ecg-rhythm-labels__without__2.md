Several good datasets fit your constraints. All of the ones below can be downloaded directly with no credentialing or data use agreement, and most are 12-lead with labels from cardiologists or physicians. I'm going from memory here rather than live pages, so check the license and terms on each download page before you commit.

## Top picks

**1. PTB-XL (PhysioNet), my first choice**
- 21,799 recordings, 10 s, 12-lead, 500 Hz (100 Hz copy included), from 18,869 patients.
- Labeled with SCP-ECG statements by up to two cardiologists, with a likelihood score per statement. The labels include `AFIB`, `AFLT`, `CLBBB`, `CRBBB`, `ILBBB`, `IRBBB`, `1AVB`, `2AVB` and `3AVB`.
- It comes with recommended stratified folds (use fold 9 for validation and fold 10 for test, which have the highest label quality). That makes your results comparable to published work.
- License: CC BY 4.0. You can get it with `wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/` or download the zip.

**2. Chapman-Shaoxing + Ningbo ("A large scale 12-lead ECG database for arrhythmia study", PhysioNet)**
- About 45,000 recordings, 10 s, 12-lead, 500 Hz. Labels were assigned by physicians and reviewed by cardiologists.
- It has plenty of AF and atrial flutter, plus AV block and bundle branch block labels.
- Some records have known quality problems, such as flat-line leads and a few mislabeled files. Screen the signals before training.

**3. CODE-15% (Zenodo)**
- About 345,000 exams from about 233,000 Brazilian patients. Recordings are roughly 7–10 s, 12-lead, 400 Hz.
- Its 6 labels line up closely with your targets: **1st-degree AV block, RBBB, LBBB, AF**, sinus bradycardia and sinus tachycardia.
- The training labels come from cardiologist text reports combined with automated analysis, so they're somewhat noisier. A separate **CODE test set** of 827 exams is annotated by 2–3 cardiologists, which makes it a good external test set.
- License: CC BY 4.0. The full CODE dataset requires an application, but the 15% subset doesn't.

**4. PhysioNet/CinC Challenge 2020/2021 training data**
- About 88,000 recordings from several sources (CPSC 2018, CPSC-Extra, Georgia, PTB-XL, Chapman, Ningbo, and others), all mapped to SNOMED-CT codes. It's useful when you want one harmonized label space.
- **CPSC 2018** (about 6,900 recordings) is an especially good fit: its 9 classes include Normal, AF, I-AVB, LBBB and RBBB. Its recordings run 6–60 s, though, not a fixed 10 s.
- **Georgia** (about 10,000 recordings, 10 s) comes from a different population (US Southeast), so it's useful as an external validation site.
- Watch for overlaps: PTB-XL and Chapman/Ningbo are included inside the Challenge set. Don't count them twice or let them leak across your splits.

## Things to plan for
- **High-grade AV block is rare everywhere.** PTB-XL has only around a dozen or so records each of 2nd- and 3rd-degree AVB, and CODE and CPSC only label 1st-degree. You'll probably need to pool several sources, or merge 2nd- and 3rd-degree into a single "high-grade AVB" class.
- **Harmonize the labels early.** Map everything to SNOMED-CT, as the Challenge did, and decide whether incomplete RBBB/LBBB count as bundle branch block.
- **Validate across sites.** For example, train on PTB-XL + Chapman, then test on Georgia and the CODE test set. Models often look much worse on data from a new site.
- **Split by patient.** PTB-XL and CODE have patient IDs, so keep each patient's recordings in one split.
- **Check with your institution about ethics.** Even with public, de-identified data, many institutions want a quick "not human subjects research" determination. It's usually fast, and it's worth asking now so it doesn't hold up publication later.

**Avoid for now:** MIMIC-IV-ECG. Its waveforms are openly downloadable, but its free-text statements are machine-generated, and the cardiologist reports sit in credentialed MIMIC-IV-Note.

My suggestion: start with PTB-XL this week, since it's clean, well documented and has a standard benchmark. Then add Chapman/Ningbo and CODE-15% for more training data, and keep Georgia and the CODE test set for external testing.