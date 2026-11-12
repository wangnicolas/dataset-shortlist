Several large, cardiologist-labeled 12-lead datasets are open access, so you can download them now with no application, credentialing or data use agreement. I'm going from memory and haven't checked the live pages, so confirm the counts and licenses on each dataset page before you commit.

## Best options

**1. PTB-XL (PhysioNet, open access, CC BY 4.0)**
- It has about 21,800 recordings from about 18,900 patients. All are 10 s, available at 500 Hz and 100 Hz.
- Cardiologists annotated them with standardized SCP-ECG statements, and a subset has a validation flag. There is also a suggested patient-wise 10-fold split.
- It covers AF, complete and incomplete LBBB and RBBB, left anterior fascicular block, and 1st, 2nd and 3rd degree AV block.
- 2nd and 3rd degree AV block are very rare in it, with only a handful of records each. 1st degree AV block has several hundred.
- It's the best starting point because it's clean, exactly 10 s, and well documented.

**2. CPSC 2018 (China Physiological Signal Challenge)**
- It has about 6,900 12-lead recordings at 500 Hz, labeled as Normal, AF, I-AVB, LBBB, RBBB, PAC, PVC, ST depression or ST elevation.
- That label set closely matches your targets.
- Recordings are 6–60 s, not a fixed 10 s, so you'd need to crop or segment them.
- It's also included in the Challenge collections below.

**3. Chapman-Shaoxing and Ningbo (PhysioNet, open access)**
- It has about 45,000 patients with 10 s, 500 Hz recordings.
- Rhythm labels such as AF were assigned by cardiologists. Conduction coverage is thinner than in PTB-XL.
- You can get it through the PhysioNet 2021 Challenge package or the original release.

**4. PhysioNet/CinC Challenge 2020 and 2021 training data (open access)**
- This bundles PTB-XL, CPSC, CPSC-Extra, Georgia, Chapman-Shaoxing, Ningbo, PTB and St Petersburg INCART. The 2021 set is about 88,000 recordings in total.
- Labels are mapped to SNOMED-CT codes that include AF, LBBB, RBBB, 1st degree AV block and others, so it's the easiest way to get a large multi-source set.
- Recording lengths and sampling rates vary, and label quality differs by source.

**5. CODE-15% (Zenodo, open access)**
- It has about 345,000 ECGs from Brazil's Telehealth Network of Minas Gerais, labeled 1dAVb, RBBB, LBBB, sinus bradycardia, AF or sinus tachycardia.
- It's the biggest option by far.
- Most labels came from automated analysis with some review, and only a small test subset was annotated by cardiologists. Treat the labels as noisier.
- Recordings are 7–10 s at 400 Hz.

## Things to watch
- **Overlap:** The Challenge sets contain PTB-XL, CPSC and Chapman/Ningbo. If you combine sources, deduplicate and split by patient and by source, or you'll leak data between train and test.
- **Rare classes:** 2nd and 3rd degree AV block will be your scarce classes in almost every public set. Plan for class imbalance, or consider merging them with 1st degree AV block into a single AV block label.
- **Label heterogeneity:** Label vocabularies differ across datasets, so you'll need a mapping table, such as SNOMED codes or PTB-XL statements to your target classes.
- **Avoid for now:** MIMIC-IV-ECG, many other PhysioNet sets, and the full CODE dataset need credentialing or an application, so they don't fit your timeline.
- **Ethics:** These datasets are public and de-identified, and no formal approval was needed to download them. Your institution may still want a brief exempt or not-human-subjects determination before you publish. A quick email to your IRB can settle that.

I'd start with PTB-XL plus CPSC 2018, which gives you about 28,000 recordings with good conduction and AF coverage. Add Chapman/Ningbo or CODE-15% if you need more volume. I can write the download commands (`wget -r` from PhysioNet) and a label-mapping script if you'd like.