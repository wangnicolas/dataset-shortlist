The datasets below include actual report text. I'm working from memory rather than checking the hosting pages, so confirm sizes and licence terms before you commit.

## English

| Dataset | Size | Report text | Access |
|---|---|---|---|
| **MIMIC-CXR** (Beth Israel Deaconess, Boston) | ~377k images, ~228k studies, ~65k patients | Full de-identified reports, with findings and impression sections in most | PhysioNet credentialed access (steps below) |
| **CheXpert Plus** (Stanford) | ~223k image–report pairs, ~188k studies, ~65k patients | De-identified reports split into sections | Stanford AIMI portal: sign in, accept the research use agreement, download with azcopy |
| **ReXGradient-160K** (Rad AI / Harvard) | ~160k studies, ~273k images, ~109k patients across several US health systems | Findings and impression | Gated on Hugging Face: accept the licence on the dataset page (non-commercial, as I recall) |
| **IU X-Ray / Open-i** (Indiana University) | 7,470 images, 3,955 reports | Findings and impression, with over-aggressive de-identification (`XXXX` tokens) | Open download from NLM Open-i, no registration or agreement |
| **CANDID-PTX** (Dunedin, New Zealand) | ~19k radiographs | De-identified reports, skewed towards pneumothorax, chest tubes and rib fractures | Data use agreement plus a short online ethics course, via University of Otago |

MIMIC-CXR is the standard benchmark, and getting it involves:

1. Create a PhysioNet account and apply for credentialing, which asks for a reference such as a supervisor.
2. Complete the CITI "Data or Specimens Only Research" course.
3. Sign the data use agreement on the project page.

Approval typically takes days to a couple of weeks. The reports are in the base MIMIC-CXR project; MIMIC-CXR-JPG adds JPGs (~560 GB instead of ~4.7 TB of DICOMs) and the official train/val/test split. The agreement forbids sharing the data with third parties, which includes sending reports to ordinary hosted LLM APIs.

For CheXpert Plus, the PNG version is a few hundred GB and the DICOMs run to terabytes. The original CheXpert release has labels only, so you need the Plus version.

## Non-English

- **PadChest (Spanish):** ~160k images from ~110k studies and ~67k patients in Alicante. You submit a request form on the BIMCV site and accept the research use agreement; the full set is about 1 TB. The released report text is preprocessed (lowercased, punctuation stripped, as I recall), so it is not pristine prose.
- **PadChest-GR (Spanish and English):** ~4.5k studies with sentence-level findings and bounding boxes, through the same BIMCV request route. The sentences were rewritten by radiologists for grounding and are not the original reports.
- **BIMCV-COVID19 (Spanish):** a few thousand COVID-era studies mixing chest X-ray and CT, with reports. It is downloadable from BIMCV with lighter terms than PadChest.
- **CASIA-CXR (French):** ~11k frontal radiographs with French reports, published in 2024. I'm least sure of this one's access details, so check the paper.
- **CX-CHR (Chinese):** appears in many papers but was never publicly released; you would have to ask the authors.

## Labels only

NIH ChestX-ray14, the original CheXpert, VinDr-CXR and BRAX provide only labels, though they are often listed alongside the datasets above.

## Recommendation

Start the MIMIC-CXR credentialing now, since it is the only step with a waiting period, and build your pipeline on IU X-Ray in the meantime. Use CheXpert Plus or ReXGradient for cross-institution evaluation, and PadChest for the non-English experiment.