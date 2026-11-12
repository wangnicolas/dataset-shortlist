Here are the main chest X-ray datasets that include the actual report text, starting with the most useful. Numbers and access terms are from memory, not checked live, so confirm the current license and version on each dataset's page before you apply.

## English, with full report text

**1. MIMIC-CXR (PhysioNet, Beth Israel Deaconess, Boston)**: the standard benchmark
- **Size:** about 377K images, 228K studies, 65K patients. Each study has one de-identified report with FINDINGS and IMPRESSION sections.
- **Access:** you need a PhysioNet credentialed account (ID check plus a reference), the CITI "Data or Specimens Only Research" course, and a signed data use agreement. Approval usually takes days to a few weeks.
- **Files:** the reports come as `mimic-cxr-reports.zip` in the DICOM release. MIMIC-CXR-JPG (about 570 GB) is the practical image source. The full DICOM set is about 4.7 TB. Official train/validate/test splits exist.
- **Restrictions:** the agreement forbids sending the data to third-party APIs, including hosted LLMs, unless the deployment is compliant. That matters if you plan LLM-based evaluation or augmentation.
- **Extras:** derived datasets like Chest ImaGenome, MS-CXR (phrase grounding) and CXR-PRO (reports with prior-study references removed) use the same credentials.

**2. CheXpert Plus (Stanford AIMI, 2024)**
- **Size:** about 223K image–report pairs, 188K studies, 65K patients. Reports are split into sections (findings, impression, history and so on), with patient metadata and RadGraph annotations.
- **Access:** register on the Stanford AIMI shared datasets portal and accept the research use agreement. It's non-commercial only, and there's no credentialing step like PhysioNet's.
- **Files:** downloads are hosted on Azure. The full image set is several TB, so plan storage and bandwidth.
- **Note:** this is the only CheXpert release with report text; the original CheXpert has labels only.

**3. ReXGradient-160K (Harvard Rajpurkar lab and Gradient Health, 2025)**
- **Size:** about 160K studies from about 109K patients across many US sites, with findings and impression text. Its multi-site data is good for testing whether a model generalizes beyond one hospital.
- **Access:** gated download on Hugging Face (accept the terms). Part of the test set is held back for the ReXrank leaderboard. Check the card for current license and split details.

**4. IU X-Ray / Open-i (Indiana University, via NLM)**
- **Size:** about 3,955 reports and 7,470 frontal and lateral images. Small, but the report format is clean.
- **Access:** fully public. Download from NLM's Open-i site, or use Kaggle mirrors.
- **Caveats:** too small to train on alone, and commonly used as an external test set. De-identification replaced some words with "XXXX", which you'll need to handle. Many papers use their own splits, so results across papers aren't directly comparable.

**5. CANDID-PTX (Dunedin, New Zealand)**
- **Size:** about 19K radiographs with free-text reports, plus pneumothorax, rib fracture and chest tube labels. A useful non-US English source.
- **Access:** request through Figshare. You complete ethics or human-subjects training and sign a data use agreement.

## Non-English

**6. PadChest (Spanish; BIMCV, Hospital San Juan, Alicante)**: the best option for your secondary experiment
- **Size:** about 160K images, 110K studies, 67K patients, with a Spanish report field.
- **Caveat:** the released "report" is preprocessed (normalized, lowercased, lightly cleaned), not the radiologist's raw prose. Whether that's acceptable depends on your experiment.
- **Access:** fill in the request form on the BIMCV site. It's free for research. The download is about 1 TB.
- **PadChest-GR (2024–25):** a smaller (about 4.5K studies) companion with grounded findings sentences in both Spanish and English, plus bounding boxes. It's handy for bilingual or grounded report generation.

**7. BIMCV-COVID19+ (Spanish)**: COVID-era chest X-rays and CTs with Spanish reports, distributed through BIMCV. Narrower in what it covers, but real report text.

## Datasets that look relevant but have labels only
NIH ChestX-ray14, original CheXpert, VinDr-CXR and BRAX (Brazil) ship labels extracted from reports, not the reports themselves. ROCO, MedPix and similar sets have figure captions or teaching-case text, not clinical reports.

## Suggested plan
- **Main training:** MIMIC-CXR. Start the PhysioNet credentialing now, since it's the slowest step.
- **More training data and external tests:** CheXpert Plus and ReXGradient-160K, with IU X-Ray as a quick public sanity check you can run on day one.
- **Secondary experiment:** PadChest, or PadChest-GR if you want parallel English text.
- **Data agreements:** check each one's terms on cloud compute and LLM APIs before you build your evaluation pipeline. MIMIC's terms in particular affect GPT- or Claude-based scoring like GREEN.

I can check current versions and access pages for any of these, or sketch a data loader that puts their report formats into one common shape.