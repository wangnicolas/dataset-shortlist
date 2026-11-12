Only a handful of public chest X-ray datasets ship the radiologist's actual free-text report. Many popular ones (CheXpert, ChestX-ray14, VinDr-CXR, PLCO) release only labels. This is from memory, so check each access page before you plan around it. Terms and sizes change.

## English reports

| Dataset | Size | Access |
|---|---|---|
| **IU X-Ray (Open-I)** | ~7.5k images, ~3.9k studies (frontal and lateral) | Open, no application |
| **MIMIC-CXR** | ~377k images, ~227k studies, ~65k patients | PhysioNet credentialed access |
| **CheXpert Plus** | ~223k image-report pairs, ~187k studies | Stanford AIMI registration and agreement |
| **ReXGradient-160K** | ~160k studies from several US health systems | Gated release (I believe on Hugging Face), with a terms agreement |

**IU X-Ray** is the easiest to get.
- Download the images and XML reports from the NLM Open-I site. Kaggle mirrors also exist.
- Each report has indication, comparison, findings, and impression sections.
- It's small, and some studies have empty findings. Most papers use the R2Gen or Li et al. split so results are comparable.

**MIMIC-CXR** is the standard benchmark for report generation.
1. Create a PhysioNet account.
2. Complete the CITI "Data or Specimens Only Research" training.
3. Apply for credentialed status, which needs references and takes days to weeks.
4. Sign the data use agreement for MIMIC-CXR (and MIMIC-CXR-JPG if you want JPEGs).
5. Download with `wget` or from the cloud buckets.

- The DICOMs are about 4.7 TB. The JPG version is roughly 550 GB and comes with the official train/val/test split and CheXpert labels.
- The reports are a separate, small download. Use the official `create_section_files.py` to extract findings and impression.
- PhysioNet's policy restricts sending the data to third-party LLM APIs. That matters if you plan LLM-based evaluation or augmentation. Use an approved route, such as a compliant Azure OpenAI setup or a local model.
- There are known issues to handle: `___` de-identification placeholders, and references to prior studies the model can't see. CXR-PRO is a derivative on PhysioNet that removes the prior references.

**CheXpert Plus** adds reports to Stanford's CheXpert images. The original CheXpert has no reports. You register at the AIMI site and agree to a research-use license. The download is large.

**ReXGradient-160K** is newer, so check its dataset card for current terms.

## Non-English reports

- **PadChest (Spanish, Valencia/BIMCV):** ~160k images. Access is by request form and is usually fast. Its public metadata is mostly labels and UMLS-mapped findings, and I'm not sure the full report text is in the main CSV. Verify that before committing. There is also a newer grounded-report extension, PadChest-GR, with Spanish and English sentences. It may fit better.
- **BIMCV-COVID19+ (Spanish):** it has reports but is skewed toward COVID cases, so it's weaker for general report generation.

## What I'd do
1. Prototype on IU X-Ray, since it's open and small.
2. Train and benchmark on MIMIC-CXR. Start the PhysioNet credentialing now, because it's the slowest step.
3. Use CheXpert Plus or ReXGradient as a second English source for generalization.
4. Use PadChest for the non-English experiment, after confirming what text it includes.

I can check the current access pages and dataset cards to confirm sizes, licenses, and the PadChest report question if you want.