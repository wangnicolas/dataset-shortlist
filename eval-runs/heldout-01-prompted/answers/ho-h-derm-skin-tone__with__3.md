Four public datasets fit. I fetched the access page for each one, except where noted.

| Dataset | Skin tone label | Diagnosis | Dark-skin representation | Access |
|---|---|---|---|---|
| **DDI** (Stanford) | Fitzpatrick, grouped I–II, III–IV, V–VI | Biopsy-confirmed, with benign/malignant and disease labels | 207 of 656 images are V–VI (208 I–II, 241 III–IV). Images come from 570 patients. | Free registration and a research-use agreement through the Stanford AIMI portal. Non-commercial, no redistribution. |
| **SCIN** (Google) | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick, and layperson-estimated Monk | Dermatologist condition labels for 2,835 of 5,033 contributions | V–VI is 16.4% by self-report but only 5.8% by dermatologist estimate. Monk 8–10 is under 1.5%. | Google Cloud Storage bucket `dx-scin-public-data` under the SCIN Data Use License. The repo has a demo notebook. |
| **Fitzpatrick17k** | Fitzpatrick I–VI | 114 conditions, with a 3-class label | V–VI is 467 of the 3,230 images in the SkinCon-annotated subset. I couldn't find counts for the full 16,577. | The CSV is on GitHub under CC BY-NC-SA 3.0. The images are not included. |
| **DermaCon-IN** | Fitzpatrick and Monk, per image | 88 main classes, 19 subclasses, 245 fine-grained labels | Mostly darker skin (Fitzpatrick IV–VI, Monk 4–9). I found no per-type counts. | Harvard Dataverse, DOI [10.7910/DVN/W7OUZM](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/W7OUZM), CC BY-NC-SA 4.0, about 4 GB. |

**Which to use**
- **DDI is the cleanest for your question.** It has reliable diagnoses, it's roughly balanced across tones, and it was built to compare I–II with V–VI. Its limit is size, so confidence intervals on V–VI will be wide.
- **SCIN has Monk labels.** Its Fitzpatrick V–VI share depends heavily on which label you use. Its diagnoses are mostly inflammatory or allergic conditions (89% of the 2,835 with a differential), not cancer. Only about half the contributions have a self-reported skin type. The paper's two Monk labeler groups also disagree on the same images.
- **Fitzpatrick17k is the largest.** Its diagnoses come from online atlases rather than biopsy, with more than 30% label noise reported. It has about 3.6 times more light than dark samples. Many image links are broken, and the authors ask you to fill out a form for a full set of links.
- **DermaCon-IN adds a different population** (South India). Its Fitzpatrick breakdown is only in a figure, and its text is inconsistent about whether the annotations centre on type 3–4 or IV–VI. Check the actual label counts before relying on it.

**Not recommended yet**
- A 2024 MSKCC skin-tone labeling set has 4,879 dermoscopic images from 64 patients, with Fitzpatrick, Monk and colorimeter labels (CC BY). The listing didn't say whether it has diagnosis labels, and I didn't open the dataset page, so I can't confirm it fits.
- None of these is dermoscopy-only. If you need dermoscopy with tone labels, I didn't find a verified one.

Per-type counts for SCIN and DermaCon-IN need to be computed from the data itself.

Sources:
- [SCIN on GitHub](https://github.com/google-research-datasets/scin)
- [SCIN paper (arXiv 2402.18545)](https://arxiv.org/html/2402.18545v1)
- [Fitzpatrick17k on GitHub](https://github.com/mattgroh/fitzpatrick17k)
- [DDI dataset page](https://ddi-dataset.github.io/)
- [DDI paper (Science Advances)](https://www.science.org/doi/10.1126/sciadv.abq6147)
- [SkinCon (arXiv 2302.00785)](https://arxiv.org/pdf/2302.00785)
- [DermaCon-IN (arXiv 2506.06099)](https://arxiv.org/html/2506.06099)
- [Skin lesion dataset catalog](https://github.com/AxDante/skin-lesion-dataset-analysis)