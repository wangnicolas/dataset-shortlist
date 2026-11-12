These are the datasets I know of that release the radiologist's free-text report. I'm going from memory and haven't checked the live pages. Access terms and sizes change, so confirm them before you plan around them.

## English

| Dataset | Size | Source | Access |
|---|---|---|---|
| **MIMIC-CXR** (plus MIMIC-CXR-JPG) | ~377k images, ~227k studies, ~65k patients | BIDMC, Boston | Credentialed, via PhysioNet |
| **IU X-ray (Open-i)** | ~3.9k reports, ~7.4k images | Indiana University, via NLM | Open, no registration |
| **CheXpert Plus** | ~223k image-report pairs, ~187k studies | Stanford | Registration and a research use agreement |
| **ReXGradient-160K** | ~160k studies | Multiple US health systems | Gated download, which I believe is on Hugging Face |

**MIMIC-CXR** is the standard benchmark for report generation.
- **Steps:** Create a PhysioNet account and complete the CITI training ("Data or Specimens Only Research"). Then apply for credentialed status, which needs a reference, and sign the data use agreement. Approval usually takes days to a couple of weeks.
- **Download:** The DICOM release is several TB. MIMIC-CXR-JPG is about 570 GB, and you can also pull it from the GCP or AWS buckets.
- **Reports only:** The reports are a separate small archive (`mimic-cxr-reports.zip`), so you can start on the text without the images. Use the repo's `create_sections_files.py` to split out Findings and Impression.
- **LLM restriction:** PhysioNet restricts sending MIMIC data to external LLM APIs. It only allows services with no-retention terms, such as certain Azure OpenAI or Vertex configurations. Check this if your pipeline calls a hosted model.
- **Derived resources:** Chest ImaGenome and MS-CXR build on MIMIC-CXR. They add sentence-level anatomical and grounding annotations, with the same credentialed access.

**IU X-ray** is the easiest to get, from the NLM Open-i site or mirrors. It's small and has a fairly high share of normal studies, so use it for quick experiments or as a second benchmark. Most papers use the R2Gen split, so use that to compare results.

**CheXpert Plus** is not the original CheXpert, which has labels only and no reports. The Plus release adds the full report text, section-parsed, along with other metadata. It's useful as an out-of-distribution check against MIMIC.

**ReXGradient-160K** is newer and large. Verify its license and access terms yourself, because I'm least sure of this one.

## Non-English (secondary experiment)

- **PadChest** (Spanish) has ~160k images from ~67k patients at Hospital San Juan, Valencia, and the BIMCV group hosts it.
  - **Access:** You fill out a request form on the BIMCV site and wait for approval, then download about 1 TB of images plus a CSV with the reports. Only about a quarter of the labels are manually curated. The rest come from an automatic labeler, which matters only if you use the labels.
  - **PadChest-GR:** This is a newer grounded-report extension. I believe it includes English as well as Spanish, but verify that.
- **BIMCV-COVID19+** (Spanish) has reports too, but it covers a COVID-skewed population.
- **Chinese:** I recall a large Chinese chest X-ray report corpus (CTRG-Chest-548K) from 2024. I'm not confident of its details or license, so check the paper before relying on it.

## Datasets to skip

NIH ChestX-ray14, the original CheXpert, VinDr-CXR and PLCO ship labels or boxes only, with no reports. They're often listed as report datasets by mistake.

## Practical notes

- Split by patient, not by image or study. MIMIC-CXR has an official split, and you should use it.
- Reports often refer to priors ("unchanged from prior"). Models can't see the prior image unless you give it to them, so many papers filter or handle this explicitly.
- MIMIC reports are de-identified, with `___` placeholders, and style varies a lot between institutions. Expect a drop when you transfer between datasets.

I can draft the PhysioNet application steps, or the download and preprocessing scripts for MIMIC-CXR and IU X-ray, if you'd like.