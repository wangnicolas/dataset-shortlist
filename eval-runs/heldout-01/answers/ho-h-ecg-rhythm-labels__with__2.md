Four open datasets cover your needs, and two of them hold most of the labels: PTB-XL and the Chapman-Shaoxing/Ningbo database. All of them can be downloaded today with no application, credentialing or data use agreement. I confirmed the access and licence records on 2026-11-11. I did not build the interactive shortlist page, so there is no `dataset-shortlist.html`.

## What I assumed you need
- **R1 (must):** standard 12-lead resting ECGs of about 10 s.
- **R2 (must):** diagnostic labels for AF, LBBB, RBBB and AV block, ideally from or checked by cardiologists.
- **R3 (must):** at least a few thousand recordings.
- **R4 (must):** direct download with no application or credentialing.
- **R5 (nice):** a standard train/test split and papers to benchmark against.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PTB-XL | Direct download | CC-BY-4.0 | ~21.8k ECGs, 10 s | Cardiologist-annotated. AF, LBBB, RBBB and AV block codes are in the statement list. | Access and licence confirmed today; code names from memory |
| 2 | Chapman-Shaoxing/Ningbo ("large scale 12-lead ECG database for arrhythmia study") | Direct download | CC-BY-4.0 | 45,152 ECGs | Physician-labelled, with a second physician validating. It has AF and bundle-branch and AV-block labels. | Access, licence, size and labelling confirmed today; label list from memory |
| 3 | CODE-15% | Direct download from Zenodo | CC-BY-4.0 | 345,779 exams | Has AF, LBBB, RBBB and 1st-degree AV block labels (from memory). Labels are weaker, and recordings may be 7–10 s. | Access and licence confirmed today; label details from memory |
| 4 | CODE-test | Direct download from Zenodo | CC-BY-4.0 | ~800 ECGs (from memory) | Cardiologist-annotated, same label set as CODE-15%. Too small to train on, but good as a gold test set. | Access and licence confirmed today; size from memory |
| 5 | PhysioNet/CinC Challenge 2021 (and 2020) | Direct download | CC-BY-4.0 | >88k public ECGs | A pooled collection with one SNOMED-CT label scheme, so it is convenient. | Confirmed today |

## Details
- **PTB-XL:** [physionet.org/content/ptb-xl/1.0.3](https://physionet.org/content/ptb-xl/1.0.3/)
  - **Labels:** The page says "annotated by up to two cardiologists" and "a large fraction of the records was validated by a second cardiologist". It also says some report strings came from the ECG device's automatic interpretation. So the labels are not all purely human.
  - **Splits:** It ships 10-fold splits split by patient, which suits your benchmark need.
  - **Papers:** Strodthoff et al., [10.1109/jbhi.2020.3022989](https://doi.org/10.1109/jbhi.2020.3022989), is a benchmark paper. The dataset paper is [10.1038/s41597-020-0495-6](https://doi.org/10.1038/s41597-020-0495-6).
  - **Access:** "Anyone can access the files", under CC-BY-4.0.
- **Chapman-Shaoxing/Ningbo:** [physionet.org/content/ecg-arrhythmia/1.0.0](https://physionet.org/content/ecg-arrhythmia/1.0.0/)
  - **Labels:** The page says "a licensed physician labeled the rhythm", "another licensed physician performed a secondary validation", and a senior physician settled disagreements. This is your best match for rhythm labels such as AF and for conduction labels.
  - **Format:** From memory, the ECGs are 10 s at 500 Hz. Check the header files.
  - **Access:** Download with `physionet download ecg-arrhythmia --version 1.0.0` or with a terminal command. The page says the IRB allowed public sharing after de-identification.
- **CODE-15%:** [zenodo.org/records/4916206](https://zenodo.org/records/4916206)
  - **Why it's different:** It is the largest set here, with 233,770 patients from Minas Gerais, Brazil, 2010–2016.
  - **Labels (from memory):** They were derived from clinical reports and automatic analysis, then partly checked by cardiologists. That is weaker than PTB-XL or Chapman. Read the label section of the paper before relying on them as ground truth.
  - **CODE-test pairing:** If you need cardiologist-verified evaluation, use CODE-test as your test set.
- **Challenge 2021:** [physionet.org/content/challenge-2021/1.0.3](https://physionet.org/content/challenge-2021/1.0.3/)
  - **Contents:** The page says there are over 88,000 public training ECGs from several sources. They include CPSC 2018 (10,330 ECGs), INCART (74 ECGs), PTB-XL, Georgia (10,344 ECGs) and Chapman-Ningbo (45,152 ECGs). The reading above showed these sources; I did not check the others.
  - **Pooled labels:** It is the quickest route to multi-source data with consistent labels. It also gives you external validation across hospitals and countries.
  - **Overlap:** It contains PTB-XL and Chapman, so do not count them twice or let them leak between your train and test sets.
  - **Recording length:** The CPSC subset has variable recording lengths (from memory), so you may need to crop to 10 s.
  - **Access:** The registration text on that page is for the competition. The data records are open under CC-BY-4.0.

## Known, not confirmed
- **SPH (Shandong Provincial Hospital) database:**
  - **What it is:** It is titled "A large-scale multi-label 12-lead electrocardiogram database with standardized diagnostic statements", with the DOI [10.6084/m9.figshare.c.5779802.v1](https://doi.org/10.6084/m9.figshare.c.5779802.v1).
  - **What I confirmed:** The DOI exists. The landing page blocked my automated check.
  - **From memory:** It has about 25k ECGs of 10–60 s, with cardiologist-reviewed labels. I believe it is open on figshare, but I don't know the licence.
  - **What to check:** Open the page in a browser to confirm the licence and whether recordings are all 10 s.
- **Georgia (Emory) and CPSC 2018:** I did not open them separately. The Challenge page confirms they are included in the Challenge data.

## Not recommended, and why
- **MIMIC-IV-ECG and MIMIC-IV-Ext-ECG-Glucose:** They need PhysioNet credentialing, which you ruled out. I confirmed the credentialed licence on the Glucose one. The MIMIC-IV-ECG label situation is from memory and I did not look it up.
- **KURIAS-ECG:** It needs a free account plus a restricted-data licence, so it isn't a plain download.
- **Hugging Face copies (for example `tirandazdylan/ptb-xl-ecg`):** Use the official PhysioNet source instead. The copies are unofficial, and some have no stated licence.
- **Small or off-target sets:** The Brugada, Leipzig paediatric and ventricular-arrhythmia sets, the 100-record SPH-Mini, and MIT-BIH-style single-lead sets don't match your labels or scale.

## What I could not find
I did not find a single dataset with large numbers of **cardiologist-verified** AV-block (2nd and 3rd degree) labels. Those classes are rare in all of these sets, so check the per-class counts before you commit. I also haven't confirmed the exact label names in PTB-XL or Chapman. I searched five registries and the literature. I did not search country-specific portals.

## Next step
1. Download PTB-XL and Chapman first. Together they give about 67k labelled 10 s ECGs, enough for AF, LBBB and RBBB.
2. Count the AV-block examples per class in each set.
3. Add CODE-15% if you need more AV-block or LBBB volume. Use CODE-test to check that its label noise is acceptable.
4. Treat Challenge 2021 as a pooled, pre-harmonised source or for external validation. Don't also train on PTB-XL and Chapman separately without deduplicating.
5. Confirm the licence terms for your intended use. CC-BY needs attribution, and these sets are de-identified.