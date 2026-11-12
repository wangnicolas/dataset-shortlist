**Start with PTB-XL.** It's the closest match to what you describe, and you can download it today with no account, application or credentialing.

## Best options (all open download)

| Dataset | Size | Labels | Notes |
|---|---|---|---|
| **PTB-XL** (PhysioNet) | ~21.8k records, ~18.9k patients, 10 s, 12-lead, 500 Hz and 100 Hz | Up to two cardiologists annotated each record. Labels are SCP-ECG statements, including AFIB, AFLT, CLBBB, CRBBB, ILBBB, IRBBB, LAFB/LPFB, 1AVB, 2AVB, 3AVB and IVCD. | CC BY 4.0. It ships with patient-stratified 10-fold splits. Folds 9 and 10 were human-validated, so they work well as val/test. Conduction classes are reasonably represented, but AV block II/III is rare. |
| **Chapman-Shaoxing / Ningbo** (PhysioNet) | ~45k records, 10 s, 500 Hz | Rhythm labels (AF, flutter, SVT, sinus rhythms, etc.) plus other condition labels, assigned by physicians | Open access. It's strong for AF, with more variable coverage of conduction classes. Check the label list for the BBB and AV block counts. |
| **CODE-15%** (Zenodo) | ~345k exams, ~233k patients, ~7–10 s, 400 Hz | 1dAVb, RBBB, LBBB, AF, sinus bradycardia and sinus tachycardia | By far the largest. The training labels are mostly derived from clinical reports and automated processing rather than individually confirmed by cardiologists. Use it for pretraining or scale, not as ground truth. |
| **Shandong Provincial Hospital (SPH)** (Figshare) | ~25k records, 10 s, 500 Hz | 44 AHA/ACC/HRS-coded statements, cardiologist-assigned | Open, but check the license on the record page. |
| **PhysioNet/CinC Challenge 2021 training set** | ~88k records pooled from several sources | SNOMED-CT labels. Scored classes include AF, I-AVB, LBBB and RBBB. | It pools PTB-XL, Chapman, Ningbo, Georgia, CPSC and others. Recording lengths vary (CPSC runs 6–60 s, and INCART is 30-minute recordings), so filter to 10 s. It's useful for testing generalization across sites. |

## Practical suggestions
- **Core set:** use PTB-XL for training and evaluation. It has ~22k records with cardiologist labels, which is well past "a few thousand".
- **Rhythm labels:** add Chapman-Shaoxing/Ningbo for more AF.
- **Generalization:** hold out one source (e.g. Chapman-Shaoxing or SPH) as an external test set, since single-site results often overstate performance.
- **Splits:** split by patient, not by record, when you build your own splits. PTB-XL's folds already do this.
- **Label mapping:** the label vocabularies differ (SCP-ECG, SNOMED, AHA codes). Map them to one scheme early.
- **Skip for now:** MIMIC-IV-ECG is large, but it requires PhysioNet credentialing and a training course. It's an option later if the lab sets that up.

## Caveat on ethics
"Open access" removes the application step. It doesn't necessarily remove your institution's requirements. Many ethics offices want a short exemption or "not human subjects research" determination, even for de-identified public data. It's usually a quick form, but confirm before you publish.

I'm working from memory here, and I haven't checked these against the live pages. Record counts and licenses can change between versions, so check each dataset's landing page. I can fetch them and pull the exact per-class counts for AF, LBBB, RBBB and AV block if you'd like.