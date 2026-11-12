The datasets below pair images with the radiologist's actual report text. I wrote this from memory and didn't look anything up for this answer, so check sizes, licences and access steps on each dataset's page before you rely on them.

## English free-text reports

| Dataset | Scale | Source | Access |
|---|---|---|---|
| **MIMIC-CXR** (PhysioNet) | ~377K images, ~228K studies, ~65K patients | Beth Israel Deaconess (Boston), ER/inpatient | Credentialed |
| **CheXpert Plus** (Stanford AIMI, 2024) | ~223K image–report pairs, ~65K patients | Stanford Hospital | Research-use agreement |
| **ReXGradient-160K** (2025) | ~160K studies, ~109K patients | 3 US health systems, ~79 sites | Gated Hugging Face |
| **IU X-Ray / Open-i** | ~7.5K images, ~3.9K reports | Indiana University | Open download |
| **CANDID-PTX** | ~19K images with reports | Dunedin, New Zealand (focus on pneumothorax) | DUA with Univ. of Otago |

**MIMIC-CXR**
- **Getting it:** create a PhysioNet account, get credentialed (identity check plus a reference), finish the CITI "Data or Specimens Only Research" course, then sign the DUA for the dataset. This usually takes a few days to a couple of weeks.
- **Images vs. reports:** the reports are in `mimic-cxr-reports.zip` in the main MIMIC-CXR project, which also holds the DICOMs (~4.7 TB). Most people use **MIMIC-CXR-JPG** (~570 GB) for the images. It also has the standard train/val/test split and CheXpert labels, but no report text. So you sign two DUAs and join the two on study ID.
- **LLM restriction:** PhysioNet's rules don't allow sending the data to third-party chat services like the consumer ChatGPT site. Hosted APIs with no data retention (e.g. Azure OpenAI, Bedrock, Vertex) are allowed under their responsible-use guidance. This matters if you plan to use LLMs for preprocessing or evaluation.
- **Standing:** it's the de facto benchmark, so you'll need it for comparisons with published work.

**CheXpert Plus**
- The original CheXpert only shipped labels. Plus adds the de-identified reports, parsed into sections, along with RadGraph annotations and demographics.
- **Getting it:** register on Stanford AIMI, accept the Stanford research-use agreement, then download from Azure. It's large; DICOM and PNG versions are both offered.

**ReXGradient-160K**
- **Getting it:** accept the terms on the gated Hugging Face repo (from the Rajpurkar lab).
- It ships train/val/public-test splits plus a held-out private test set.
- Because the images come from many sites, it's useful for testing generalization beyond a single hospital.

**IU X-Ray (Open-i)**
- **Getting it:** no credentialing; download directly from NLM's Open-i. It's licensed for non-commercial use, so check the exact terms.
- Reports come as XML with Findings and Impression sections. De-identification replaced some content with "XXXX".
- It's small and has no official split, so papers' numbers aren't directly comparable. Use it for quick prototyping or as a second test set.

**CANDID-PTX**
- **Getting it:** a data use agreement plus proof of human-subjects training.
- It's skewed toward pneumothorax, chest tubes and rib fractures, so it's better as an extra evaluation set than as general training data.

## Non-English (for your secondary experiment)

- **PadChest** (Spain, BIMCV/Alicante): ~160K images and ~110K studies with **Spanish** reports. I believe the report text is somewhat preprocessed rather than fully raw, so look at a sample before committing. **Getting it:** fill out the BIMCV request form; it's free for research. About 1 TB.
- **PadChest-GR** (2024–25): a few thousand PadChest studies with grounded report sentences in **both Spanish and English**, plus bounding boxes. **Getting it:** through BIMCV under an agreement. It works well for a cross-lingual or grounded-generation experiment.
- **BIMCV-COVID19+** (Spain): I think it includes some Spanish reports, but I'm not certain. Check before relying on it.

## Common datasets that don't have report text
NIH ChestX-ray14, the original CheXpert, VinDr-CXR, and BRAX (as far as I know) only release labels or annotations. Datasets built on top of MIMIC-CXR, such as Chest ImaGenome, MS-CXR and RadGraph, add annotations but still need MIMIC-CXR access to get the reports.

## Practical notes
- **Which section to generate:** most papers generate the **Findings** section, sometimes Impression, so decide this early. A sizeable share of MIMIC studies have no Findings section.
- **References to prior exams:** reports often say things like "unchanged from prior". Consider CXR-PRO (MIMIC with those references removed) or using the prior study as an input.
- **Suggested plan:** start with IU X-Ray (instant download) while the MIMIC-CXR credentialing goes through. Then use MIMIC-CXR as the main benchmark, with CheXpert Plus and ReXGradient for training scale and testing on other hospitals' data.