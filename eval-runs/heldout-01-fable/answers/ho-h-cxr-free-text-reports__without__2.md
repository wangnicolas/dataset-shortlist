I answered from memory without checking the current dataset pages, so confirm counts and licence terms there before you plan around them.

For English, MIMIC-CXR is the standard training set and IU X-Ray is the one you can download today. PadChest (Spanish) is the natural choice for your secondary experiment.

| Dataset | Language | Approx. size | Report text | Access |
|---|---|---|---|---|
| **MIMIC-CXR** | English | ~377k images, ~228k studies, ~65k patients | Full de-identified reports | PhysioNet credentialed access |
| **IU X-Ray (Open-i)** | English | ~7.5k images, ~4k reports | Findings, impression, indication and comparison | Open download |
| **CheXpert Plus** | English | ~223k image-report pairs, ~65k patients | De-identified reports, split into sections | Stanford AIMI research use agreement |
| **ReXGradient-160K** | English | ~160k studies, ~273k images, ~109k patients | Full reports from many US sites | Gated on Hugging Face |
| **CANDID-PTX** | English | ~19k images | Anonymised reports, as I recall | University of Otago data use agreement |
| **PadChest** | Spanish | ~161k images, ~110k studies, ~67k patients | Reports in a CSV column, normalised | BIMCV request form |
| **BIMCV-COVID19+** | Spanish | Thousands of COVID-era studies, mixed with CT | Reports included | BIMCV licence acceptance |

## What access involves

- **MIMIC-CXR:** You need a PhysioNet account, the CITI "Data or Specimens Only Research" training course, a credentialing application and a signed data use agreement. Approval typically takes days to a couple of weeks, so start this first.
  - The reports are in the main MIMIC-CXR (DICOM) project, which is several terabytes.
  - Most people take the images from MIMIC-CXR-JPG (roughly 500–600 GB) and download only the reports archive from the DICOM project.
  - The agreement prohibits sharing the data with third parties, which includes sending reports to hosted LLM APIs unless you follow PhysioNet's specific guidance.
- **IU X-Ray:** There is no registration; you download the PNG images and XML reports directly from NLM's Open-i site. It is too small to train on alone but is widely used as a second benchmark. Redacted tokens appear as "XXXX", and the licence is non-commercial as I recall.
- **CheXpert Plus:** You sign in on the Stanford AIMI Shared Datasets page, accept the non-commercial research use agreement, and download with azcopy from Azure. The original CheXpert release has labels only; you need the Plus release for reports.
- **ReXGradient-160K:** You request access on the Hugging Face dataset page (Rajpurkar lab) and accept a non-commercial licence. Its multi-site origin makes it useful for testing generalisation.
- **CANDID-PTX:** You apply through the University of Otago, which requires a data use agreement and a short online ethics course. The set is skewed toward pneumothorax, and you should confirm that reports are in the current release.
- **PadChest:** You fill in the BIMCV form, accept the research use agreement, and receive a download link; the full set is around 1 TB. The released report text is preprocessed (lowercased, with punctuation and accents stripped, as I recall), so it is not the verbatim report. Inspect a sample before committing.
- **BIMCV-COVID19+:** You accept the licence on the BIMCV site and download. It is narrower and noisier than PadChest.

## Sets that do not qualify

- **Labels only:** NIH ChestX-ray14, the original CheXpert, VinDr-CXR and BRAX release no report text.
- **Derived from MIMIC-CXR:** MS-CXR, Chest ImaGenome, RadGraph and CXR-PRO are annotations or rewrites of MIMIC-CXR reports. They need the same PhysioNet credentialing and add no new reports.
- **PadChest-GR:** This has bilingual Spanish and English finding sentences with grounding boxes, but they are restructured sentences, not the original free text.