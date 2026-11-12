Three PhysioNet datasets fit. I fetched each one's official page this session, and all three are open access under CC BY 4.0, with no application, credentialing or data use agreement. I did not download any data.

## Best options

**1. Chapman-Shaoxing / Ningbo: "A large scale 12-lead ECG database for arrhythmia study"** (PhysioNet `ecg-arrhythmia` 1.0.0)
- **Size and format:** 45,152 resting 12-lead ECGs, each about 10 s at 500 Hz.
- **Labels:** each ECG has a rhythm label, such as atrial fibrillation, plus additional conditions including left and right bundle branch block. Labels apply to the whole recording and are mapped to SNOMED CT codes.
- **Provenance:** this is the strongest of the three. A physician labeled each ECG, a second physician validated it, and a senior physician resolved any disagreement.
- **Download:** the ZIP is 2.3 GB. You can also use `wget -r -N -c -np https://physionet.org/files/ecg-arrhythmia/1.0.0/` or `aws s3 sync --no-sign-request s3://physionet-open/ecg-arrhythmia/1.0.0/ .`.
- **Gap:** the page's examples don't mention AV block explicitly. Check the SNOMED mapping file for AV block codes before you commit to this dataset for that class.

**2. PTB-XL** (PhysioNet `ptb-xl` 1.0.3)
- **Size and format:** 21,799 10-second 12-lead records from 18,869 patients.
- **Labels:** 71 SCP-ECG statements. Up to two cardiologists annotated each record, and a large fraction were validated by a second cardiologist.
- **Caveat:** reports came from either a cardiologist or the device's automatic interpretation, so label quality is mixed.
- **Download:** the ZIP is 1.7 GB. The `wget` and S3 commands are the same pattern as above, with `ptb-xl/1.0.3`.
- **Gap:** I'm recalling from memory that the statements include AF, bundle branch blocks and AV blocks. The page I fetched didn't list them, so check the label file.

**3. PhysioNet/CinC Challenge 2021 training data** (`challenge-2021` 1.0.3)
- **Size:** about 88,000 public training ECGs from several sources: CPSC 2018 and Extra, Georgia, PTB/PTB-XL, INCART, and Chapman-Shaoxing/Ningbo.
- **Labels:** SNOMED-CT-coded and harmonized across sources. AF and first-degree AV block are given as examples on the page. Bundle branch block is not listed there, so check the evaluation repository's label lists.
- **Caveat:** the page says some sources have "human-overread machine labels with single or multiple human readers," so label quality varies by source. The test sets (about 36,000 ECGs) will never be released.
- **Overlap:** it includes Chapman-Shaoxing/Ningbo and PTB-XL, so don't combine it with options 1 and 2 without removing duplicates.
- **Value:** it gives you multi-site data for testing generalization, and Georgia is a good external test set. Per-source archives are available, so you can download just the parts you want.

## Suggested approach
- Start with Chapman-Shaoxing/Ningbo for training, since its labels are the best documented.
- Use PTB-XL as an independent evaluation set, with its recommended patient-wise folds.
- Pull Georgia and CPSC from the Challenge 2021 archives for external validation.

## What I haven't checked
- Per-class counts for AF, LBBB, RBBB and each AV block degree. Count these from the label files before you plan the study.
- Whether the Challenge 2021 per-source archives are downloadable individually in practice. The page implies it, but I didn't test it.
- Whether your institution still wants an ethics determination. These datasets are de-identified and openly licensed, but some institutions require a "not human subjects research" sign-off even for public data. A quick email to your IRB is worth sending.

Sources:
- https://physionet.org/content/ecg-arrhythmia/1.0.0/
- https://physionet.org/content/ptb-xl/1.0.3/
- https://physionet.org/content/challenge-2021/1.0.3/