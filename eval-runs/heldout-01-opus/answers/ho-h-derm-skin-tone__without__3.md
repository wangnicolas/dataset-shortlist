Four public datasets meet all your requirements: every image has a skin tone label and a diagnosis, and types V–VI appear in real numbers. There are two other datasets you'll probably come across that don't meet them.

## Datasets that qualify

**1. Fitzpatrick17k** (Groh et al., CVPR-W 2021)
- 16,577 clinical photos covering 114 conditions, taken from online atlases.
- Each image has a Fitzpatrick label. From my memory of the paper (worth re-checking against the CSV), the counts are about 1,533 type V and 635 type VI.
- The labels were assigned by crowd annotators looking at the image, not reported by the patient. Later audits found duplicate images and some wrong diagnosis labels. Use the cleaned version (Abhishek et al., 2024) so the duplicates don't leak across your splits.
- It's freely downloadable and the most widely used benchmark for this kind of audit.

**2. DDI – Diverse Dermatology Images** (Daneshjou et al., *Science Advances* 2022, Stanford)
- 656 images from 570 patients. Every diagnosis is confirmed by biopsy, which none of the other datasets offer. It includes malignant vs. benign labels and about 78 specific diagnoses.
- Skin tone was assigned by reviewing the patient's clinical record, not just the image, so it's stronger than Fitzpatrick17k's labels. The groups are roughly balanced: about 207 images in V–VI and about 208 and 241 in the other two groups (my recollection, so check the metadata).
- Limitations: tone comes only in three groups (I–II, III–IV, V–VI), so you can't separate V from VI, and the dataset is small, so your confidence intervals will be wide.
- Access is through the Stanford AIMI portal and requires accepting a research-use agreement.

**3. SCIN** (Google and Stanford, 2024)
- 10,408 images from 5,033 people, crowdsourced from US internet users. Diagnoses were labeled by dermatologists as a weighted list of possible conditions, not confirmed by biopsy.
- It has three tone labels per case: Fitzpatrick type reported by the person, Fitzpatrick type estimated by a dermatologist, and Monk scale estimated by laypeople (separate rater pools in the US and India). That makes it the strongest option if you need Monk scale.
- The authors describe the Fitzpatrick distribution as weighted more toward types 3–6 than clinical datasets. The JAMA Netw Open paper notes "relatively few contributors with MST greater than 8", so the darkest Monk tones are sparse. The self-reported and dermatologist-estimated Fitzpatrick types also often disagree. The repo's demo notebook prints the distributions, so check counts before committing.
- Freely available on GitHub.

**4. DermaCon-IN** (NeurIPS 2025 Datasets track)
- 5,450 clinical images from 3,002 outpatients in South India, with 245 diagnoses assigned by board-certified dermatologists.
- Every image has both Fitzpatrick and Monk labels, scored on unaffected skin. It focuses on types IV–VI. I couldn't find per-type counts.
- It's hosted on Harvard Dataverse. When I looked, the README still said "will be hosted," so confirm the data is actually downloadable.

**5. PASSION** (MICCAI 2024)
- 4,901 images from 1,653 children and teenagers, collected in Madagascar, Guinea, Malawi and Tanzania. Labels were checked by dermatologists.
- The images are almost all type IV–VI, mostly VI.
- It covers only a few common conditions: eczema, fungal infections, scabies and impetigo.
- Available through passionderm.github.io after a request or agreement.

## Datasets that don't qualify
- **ISIC archive / HAM10000 / BCN20000:** most images have no skin tone labels, and the population is overwhelmingly light-skinned.
- **PAD-UFES-20:** has Fitzpatrick labels for some images, but almost none are V–VI.

## Suggestions for the audit
- **Main approach:** train or evaluate on Fitzpatrick17k, then use DDI as the external test set. DDI is the only one with biopsy-confirmed diagnoses and roughly equal-sized tone groups, and it's the standard design in this literature (Daneshjou et al. found performance drops on V–VI this way).
- **For Monk scale or self-reported tone:** add SCIN.
- **PASSION and DermaCon-IN:** both are excellent for dark-skin coverage, but they have few light-skin images. Comparing light vs. dark within either one is weak, and comparing across datasets mixes up skin tone with differences in camera, location and disease mix. Use them as extra test sets on dark skin, ideally limited to diagnoses that also appear in your other data.
- **Check how each tone label was made:** image-estimated, chart-derived and self-reported labels disagree a lot. It's worth running your analysis under more than one labeling source as a robustness check.

Sources:
- [PASSION paper (arXiv 2411.04584)](https://arxiv.org/html/2411.04584v1) · [MICCAI page](https://papers.miccai.org/miccai-2024/590-Paper3722.html)
- [DermaCon-IN (arXiv 2506.06099)](https://arxiv.org/html/2506.06099) · [code repo](https://github.com/shan4035/DermaCon-IN-code)
- [SCIN GitHub](https://github.com/google-research-datasets/scin) · [SCIN blog](https://research.google/blog/scin-a-new-resource-for-representative-dermatology-images/) · [SCIN JAMA Netw Open paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11579799/)
- [Global Atlas of Digital Dermatology (arXiv 2601.00840)](https://arxiv.org/html/2601.00840): a recent survey of the field, useful for finding anything I missed
- Fitzpatrick17k and DDI details are from memory of the original papers (Groh et al. 2021; Daneshjou et al. 2022), so verify exact counts against their metadata.