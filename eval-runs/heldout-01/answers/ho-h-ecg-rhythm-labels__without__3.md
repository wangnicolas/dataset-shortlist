All of these are open downloads, with no application, DUA or credentialing. I'm going from memory and didn't check the sites, so confirm the license and file details on each landing page and treat the counts as approximate.

## Best options

**1. PTB-XL (PhysioNet), the best starting point**
- It has about 21.8k records from about 18.9k patients. Each is a 10 s, 12-lead recording, at 500 Hz with a 100 Hz copy.
- Labels are SCP-ECG statements. Up to two cardiologists annotated them, and there's a flag for human-validated labels.
- It covers AF and flutter, complete and incomplete LBBB and RBBB, fascicular blocks, and first-degree AV block.
- It's CC BY 4.0, and it ships with suggested patient-wise stratified folds, so use those.
- Weakness: 2nd- and 3rd-degree AV block are very rare (tens of records), so a model for "AV block" will effectively be first-degree AV block.

**2. Chapman-Shaoxing and Ningbo (PhysioNet)**
- It has about 45k patients, 10 s, 12-lead, at 500 Hz.
- It has standardized rhythm and conduction labels, including AF, first-degree AV block, and LBBB/RBBB. Physicians assigned the labels.
- It's open under CC BY 4.0.
- It's a good complement to PTB-XL because it comes from a different population and different hardware, which helps with external validation.

**3. PhysioNet/CinC Challenge 2021 training data**
- It's roughly 88k 12-lead recordings pooled from several sources: PTB-XL, Chapman, Ningbo, Georgia, CPSC and others. Labels are mapped to SNOMED-CT, and the pool includes AF, LBBB, RBBB and first-degree AV block.
- Use it as a convenient pre-harmonized bundle, and don't count it as additional data on top of #1 and #2.
- Recording lengths and label quality vary by source. Some CPSC records run 6–60 s, so you'd need to crop or filter to get true 10 s.

**4. CODE-15% (Zenodo)**
- It's about 345k exams from Brazil's Telehealth Network of Minas Gerais. Recordings are about 7–10 s.
- It has labels for 1st-degree AV block, LBBB, RBBB and AF, among others.
- Most of the training labels come from clinical reports or automated processing, not from a per-exam cardiologist review. Only the small separate CODE-test set was cardiologist-annotated. That may not meet your "assigned or confirmed by cardiologists" requirement, so use it for pretraining or scale, not as ground truth.

## Practical notes
- **Data volume:** PTB-XL plus Chapman/Ningbo gives well over your "few thousand" for AF, bundle branch blocks and first-degree AV block. For high-grade AV block you'll likely have too few examples from any open set. Plan around that, or treat it as a limitation in your write-up.
- **Leakage:** Split by patient, and don't mix Challenge 2021 with its constituent datasets without deduplicating.
- **Label harmonization:** Label vocabularies differ across sources (SCP-ECG codes, SNOMED, free text). Build one mapping table early.
- **Ethics and compliance:** These sets are de-identified and openly licensed, so you can download them now. Many institutions still want a short exempt or not-human-subjects determination before publishing, so a quick email to your IRB or ethics office is worth sending this week.
- **Excluded:** MIMIC-IV-ECG and similar sets need credentialing, so they don't fit your timeline.

I can write a download-and-label-mapping script for PTB-XL and Chapman/Ningbo that produces a unified 10 s, 12-lead set with AF, LBBB, RBBB and AV-block targets. Say if you want it.