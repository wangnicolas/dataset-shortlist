Four public datasets fit your criteria. I checked each one's access page, except where I say otherwise. I haven't downloaded any of them or counted any images myself. Every V/VI figure below is from papers or secondary sources.

## Best fits

**1. Diverse Dermatology Images (DDI), Stanford**
- **What it is:** 656 clinical images from 570 patients. Diagnoses are pathology-confirmed, and each image has a malignant/non-malignant label.
- **Skin tone labels:** Fitzpatrick I–VI. Two board-certified dermatologists assigned them, using the in-person clinic evaluation and the demographic photos.
- **V/VI representation:** This is the most balanced set. One secondary source reports 207 images of types V–VI (159 benign, 48 malignant). Another reports 81 with 16 malignant. I couldn't reconcile the two, so check the counts in the metadata yourself.
- **Access:** Register on the [DDI site](https://ddi-dataset.github.io/) through the Stanford AIMI portal. Each user registers individually.
- **Terms:** Non-commercial research use only. No redistribution, and no derivative works.
- **Fit for your audit:** The set is small, so confidence intervals will be wide. It was built to be matched across tone groups (diagnostic category, age, gender, photo date), which suits an audit.

**2. SCIN (Google)**
- **What it is:** 10,000+ crowdsourced clinical photos from US users, with self-reported demographics and dermatologist condition labels.
- **Skin tone labels:** It is the only dataset here with both scales. It has self-reported Fitzpatrick, estimated Fitzpatrick and estimated Monk Skin Tone. The Monk labels come from laypeople, not dermatologists.
- **Access:** The `dx-scin-public-data` Google Cloud Storage bucket. The [GitHub repo](https://github.com/google-research-datasets/scin) has a demo notebook and a schema file. It is released under the SCIN Data Use License.
- **Caveats:** About 89% of the diagnosable cases are allergic, infectious or inflammatory conditions, so it has little skin cancer. Labels are differential diagnoses, not biopsy-confirmed. The repo lists known issues: duplicate images, 48 gradable cases with no condition label, and one missing file. I couldn't find V/VI counts on the page, so count them from the metadata.

**3. Fitzpatrick 17k**
- **What it is:** 16,577 clinical images across 114 conditions, with Fitzpatrick I–VI labels from Scale AI annotators. This is by far the largest set.
- **V/VI representation:** About 13% of images are V+VI. A review puts type VI alone at 635 images.
- **Access:** The [GitHub repo](https://github.com/mattgroh/fitzpatrick17k) has `fitzpatrick17k.csv` with labels and URLs. You download the images from the original atlas sites, and some links are broken. The authors offer a form to request a link to all the images.
- **Terms:** CC BY-NC-SA 3.0.
- **Caveats:** Diagnoses come from atlas metadata, not histopathology. Near-duplicate pairs exist, some with conflicting labels. Skin tone labels are subjective. Deduplicate and consider the label noise before drawing fairness conclusions.

**4. DermaCon-IN**
- **What it is:** 5,450 images of Indian patients with 245 disease labels, annotated for both Fitzpatrick and Monk.
- **Access:** [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/W7OUZM), about 4 GB, CC BY-NC-SA 4.0. The [paper](https://arxiv.org/html/2506.06099) says the code is on GitHub. I confirmed the access details from the paper, not by opening the Dataverse page.
- **Caveats:** I couldn't read the per-tone counts. The paper says the intro covers Fitzpatrick IV–VI but the text also says Fitzpatrick 3–4, so V/VI coverage is unclear. It is a single-country population.

## Ruled out or weak
- **PAD-UFES-20:** Fitzpatrick labels exist for only 579 of 1,373 patients, and one source counts just 11 images of type V–VI. It doesn't meet your "not a handful" requirement.
- **HAM10000, ISIC 2020, MILK10k:** These have no reliable skin tone labels, and fewer than 1% of subjects are V/VI. One paper trained models to estimate tone for them. That gives you estimated labels, not ground truth.
- **Monk Skin Tone Examples and Skin Tone in the Wild:** These carry Monk labels but aren't dermatology data.

## Suggested approach
Use DDI as the main audit set because its labels are the cleanest. Use Fitzpatrick 17k for statistical power, and SCIN if you want Monk labels or inflammatory conditions. All of these have non-commercial terms, so check that they cover your audit's use.

Sources:
- [Fitzpatrick17k overview](https://www.emergentmind.com/topics/fitzpatrick-17k-dataset)
- [Skin Type Diversity in Skin Lesion Datasets: A Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11343783/)
- [SCIN GitHub](https://github.com/google-research-datasets/scin)
- [DDI dataset page](https://ddi-dataset.github.io/)
- [Fitzpatrick17k GitHub](https://github.com/mattgroh/fitzpatrick17k)
- [DermaCon-IN paper](https://arxiv.org/html/2506.06099)
- [Pipsqueak / skin tone bias in melanoma detection](https://www.sciencedirect.com/science/article/pii/S1877750326000761)
- [Skin Tone Label Granularity paper](https://arxiv.org/pdf/2509.11184)