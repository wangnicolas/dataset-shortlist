You can download enough data this week with no application. Start with **PTB-XL**. It has 21,799 ten-second 12-lead ECGs labelled by cardiologists, and it's a direct download under CC BY 4.0. You can scale up with the other free downloads below. I checked everything on 2026-11-12 using the PhysioNet, Zenodo, DataCite, OpenAIRE and Hugging Face registries plus a literature search.

## What I assumed you need
- **R1 (must):** raw standard 12-lead resting ECG waveforms, about 10 seconds each
- **R2 (must):** labels for atrial fibrillation (AF), right and left bundle branch block (RBBB, LBBB) and AV block
- **R3 (must):** at least a few thousand recordings
- **R4 (must):** a free download this week, with no application, data use agreement (DUA) or credentialing
- **R5 (nice to have):** labels assigned or confirmed by cardiologists
- I assumed research use with no commercial restriction needed. All the top sets are CC BY 4.0 anyway.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PTB-XL | open download, minutes | CC BY 4.0 | 21,799 ECGs, 3.2 GB | strong; cardiologist labels | today |
| 2 | Chapman-Shaoxing + Ningbo (large-scale 12-lead arrhythmia DB) | open download, minutes | CC BY 4.0 | 45,152 ECGs, 5.5 GB | strong; labelled by physicians, second physician checked | today |
| 3 | PhysioNet/CinC Challenge 2021 | open download, minutes | CC BY 4.0 | ~88k ECGs, 13.6 GB | strong; adds CPSC 2018 and Georgia | today (contents from memory) |
| 4 | SPH (Shandong Provincial Hospital) | open download from figshare | CC BY 4.0 | 25,770 ECGs | strong | licence today; download page from memory |
| 5 | CODE-15% | open download, minutes | CC BY 4.0 | 345,779 exams, 46 GB | partial; noisier labels | today |
| 6 | CODE-test | open download, minutes | CC BY 4.0 | 827 ECGs | test set only; cardiologist consensus | today |
| 7 | MIMIC-IV-ECG | open download | ODbL | ~800k ECGs, 97 GB | partial; machine labels | today |
| 8 | PTB-XL+ | open download | CC BY 4.0 | same records as PTB-XL | add-on | today |

## Details
1. **PTB-XL** — https://physionet.org/content/ptb-xl/1.0.3/
   - **Contents:** 10-second ECGs at 500 Hz and 100 Hz, labelled with SCP-ECG codes. The codes include AFIB, CRBBB, CLBBB, IRBBB, LAFB and first-, second- and third-degree AV block.
   - **Who labelled them:** the page says the waveforms were "annotated by up to two cardiologists" and "a large fraction … validated by a second cardiologist".
   - **Caveat:** some labels started as automatic device interpretations, so filter on the `validated_by_human` flag.
   - **Split:** it comes with patient-wise folds (folds 1–8 to train, 9 to validate, 10 to test). Use them.
   - **Limits:** recorded in Germany in 1989–96.
2. **Chapman-Shaoxing + Ningbo** — https://physionet.org/content/ecg-arrhythmia/1.0.0/
   - **Contents:** 45,152 ten-second ECGs with SNOMED CT labels.
   - **Who labelled them:** "a licensed physician labeled… another licensed physician performed a secondary validation… a senior physician" settled disagreements. The page doesn't say they were cardiologists.
   - It replaces the original 10,646-record figshare release from 2020.
   - From memory, people have reported some label noise, so inspect the rare classes.
3. **Challenge 2021** — https://physionet.org/content/challenge-2021/1.0.3/
   - The useful extra parts are CPSC 2018 (6,877 records labelled for AF, first-degree AV block, LBBB and RBBB, 6–60 s long) and Georgia (10,344 ten-second records). The labels are already mapped to a common code set, and scoring code is included.
   - **Overlap warning:** it also contains PTB-XL and Chapman/Ningbo. Remove the duplicates before combining it with #1 or #2, or records will leak between training and test.
4. **SPH** — DOI 10.6084/m9.figshare.c.5779802. The paper is Liu et al. 2022, *Scientific Data*, doi:10.1038/s41597-022-01403-5.
   - **Contents:** 25,770 ECGs, 10–60 seconds long (crop them to 10 s), with standardised AHA diagnostic statements.
   - figshare blocked my automated check, so the open download is from memory. Who wrote the labels is also unconfirmed; check the paper.
5. **CODE-15%** — https://zenodo.org/records/4916206
   - **Contents:** Brazilian telehealth ECGs labelled for first-degree AV block, RBBB, LBBB, sinus bradycardia, AF and sinus tachycardia.
   - From memory, the labels come semi-automatically from cardiologist reports, and there is no label for second- or third-degree block.
   - Best used for pretraining. It was used in Ribeiro et al. 2020, *Nature Communications*, doi:10.1038/s41467-020-15432-4.
6. **CODE-test** — https://zenodo.org/records/3765780
   - Two cardiologists labelled every ECG and "a third senior specialist" settled disagreements.
   - Use it as an independent gold-standard test set.
7. **MIMIC-IV-ECG** — https://physionet.org/content/mimic-iv-ecg/1.0/
   - The open release has only machine-generated report text, which you'd have to parse into labels.
   - The labels derived from clinical records (MIMIC-IV-ECG-Ext-ICD) need credentialing.
8. **PTB-XL+** — https://physionet.org/content/ptb-xl-plus/1.0.1/
   - Adds ECG features and labels from two commercial interpretation algorithms to every PTB-XL record. Useful as a comparison baseline, not as new recordings.

## Known, not confirmed
- **SPH:** the access terms and who labelled it (see #4).
- **Challenge sets:** the exact record counts and which classes are scored are from memory.

## Not recommended, and why
- **KURIAS-ECG** (Korean): a good clinical fit, but the page says "only registered users who sign the specified data use agreement can access the files". It's a personal click-through agreement, not one your institution signs. Use it only if your no-DUA rule allows that.
- **MIT-BIH AF Database and PhysioNet Challenge 2017:** these are 2-lead Holter and single-lead recordings, not 12-lead resting ECGs.
- **PTB Diagnostic** (only 549 records, mostly heart attacks), **Leipzig** (children and congenital heart disease) and **MedalCare-XL** (simulated ECGs).
- **Full CODE and UK Biobank:** need an application (from memory).
- **Hugging Face copies of these datasets:** unofficial copies. Download from the official sources.

## What I could not find
Apart from PTB-XL and CODE-test, I found no large open set where every label was confirmed by a cardiologist. Second- and third-degree AV block are rare in every dataset, so expect a few hundred examples at most once you pool them.

## Next step
1. Today, download PTB-XL and CODE-test.
2. Add Chapman/Ningbo and CPSC/Georgia from Challenge 2021, removing records that appear in more than one set.
3. Map everything to the SNOMED codes the Challenge uses.
4. Even though this data is open and de-identified, ask your institution's ethics board whether it needs a short "not human subjects research" decision before you publish.

The interactive version of this list, where you can filter and export an access plan, is at `/private/tmp/e-F4cWzl/home/cwd/dataset-shortlist.html`.