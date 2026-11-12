Here are the main options, from memory. Check each access page before you plan around it, because terms and versions change.

## English, with free-text reports

| Dataset | Size | Access |
|---|---|---|
| **MIMIC-CXR** (and MIMIC-CXR-JPG) | ~377k images, ~227k studies, ~65k patients (BIDMC) | Credentialed (PhysioNet) |
| **CheXpert Plus** | ~223k image-report pairs, ~187k studies (Stanford) | Registration and research agreement |
| **IU X-ray (Open-I)** | ~3.9k reports, ~7.4k images | Open download |
| **ReXGradient-160K** | ~160k studies from several US health systems | Gated on Hugging Face |

**MIMIC-CXR** is the standard benchmark for this task.
- **Access:**
  1. Create a PhysioNet account.
  2. Complete the CITI "Data or Specimens Only Research" course.
  3. Submit the credentialing application, which needs a reference. Approval can take days to weeks.
  4. Sign the data use agreement for the project.
- **Download:** Use `wget` with your PhysioNet login, or pull from the GCP/AWS buckets. The DICOMs are several TB. MIMIC-CXR-JPG is far smaller (~570 GB) and includes the official train/val/test split plus CheXpert/NegBio labels.
- **Reports:** The reports are a small separate zip of plain text. The repo's `create_sections_files.py` splits out the findings and impression sections.
- **LLM policy:** PhysioNet restricts sending credentialed data to third-party LLM APIs. Read that policy first if you plan to use an API model for evaluation or augmentation.
- **Derived resources:** Some build on MIMIC-CXR and need the same access. Examples are Chest ImaGenome (scene graphs) and CXR-PRO (impressions with references to prior studies removed).

**CheXpert Plus** extends the original CheXpert, which had labels only. This release adds the radiology reports. You register with Stanford AIMI and agree to a research-use license. Access is quicker than PhysioNet credentialing.

**IU X-ray (Open-I)** needs no credentialing. You download images and XML reports from NLM Open-i, and mirrors exist on Kaggle and elsewhere.
- It's small, so it's good for debugging and for a second benchmark.
- Reports are findings plus impression, with de-identification placeholders (`XXXX`).
- Some studies have empty sections.
- Papers generally use the split from Li et al. (2018), so use that to stay comparable.

**ReXGradient-160K** is a 2025 release and the one I'm least sure of. Check the Hugging Face page for the current license and gating process.

## Non-English

**PadChest** (Hospital San Juan, Alicante) has ~160k images and ~67k patients, with the reports in **Spanish**.
- **Access:** You fill out a request form with BIMCV, and they approve by email. It's usually free for research.
- **Labels:** Only about a quarter of the labels are manually reviewed. The rest come from an automatic labeler, so don't treat the labels as ground truth.
- **Related:** BIMCV-COVID19 also has Spanish reports, but it's COVID-specific.

## Often suggested, but not usable here
- **NIH ChestX-ray14, VinDr-CXR, original CheXpert, BRAX:** These release labels or boxes, not the radiologists' reports.
- **Chinese or other-language report sets:** Several papers use them, but the ones I know of are private hospital data. I can't point you to a public one with confidence.

## Suggested plan
1. Start the **MIMIC-CXR** credentialing now, since it's the slowest step.
2. Prototype on **IU X-ray** while you wait.
3. Add **CheXpert Plus** as a second large English set for cross-dataset checks.
4. Use **PadChest** for the non-English experiment.

I can also write the download and preprocessing scripts, such as section extraction and split handling, once you have access.