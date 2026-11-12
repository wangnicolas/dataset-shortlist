Four public datasets fit your criteria. I checked each one's page where I could. I haven't downloaded anything or counted images myself.

## Best fits

**1. DDI (Diverse Dermatology Images, Stanford)**
- **Contents:** 656 clinical images from 570 patients. Every lesion is biopsy-proven, with 78 disease labels plus a benign/malignant flag.
- **Dark-skin coverage:** 207 images are Fitzpatrick V–VI, which is 159 benign and 48 malignant. The other bins are 208 for I–II and 241 for III–IV. This is the most balanced of the datasets.
- **Limits:**
  - Skin tone comes in three bins (I–II, III–IV, V–VI), so you can't separate V from VI.
  - It is small, so subgroup confidence intervals will be wide.
  - Those labels were validated by two dermatologists, which makes them stronger than most.
- **Access:** You download it from the Stanford AIMI portal. Registration is required, and you must accept a Research Use Agreement. The terms are non-commercial research only, no redistribution, no derivative works and no sharing the link. A Redivis mirror also exists. I couldn't open its page, so I don't know whether that route has the same terms.
- **Links:** [project page](https://ddi-dataset.github.io), [Redivis listing](https://stanford.redivis.com/datasets/3r16-5mby7gfer), [paper](https://www.science.org/doi/10.1126/sciadv.abq6147)

**2. SCIN (Google)**
- **Contents:** About 10,400 images from about 5,000 contributions. They are crowdsourced US clinical photos with dermatologist condition labels. It has estimated Fitzpatrick type (eFST), layperson-estimated Monk tone (eMST) and some self-reported Fitzpatrick type. It's the only option here with Monk labels.
- **Dark-skin coverage:** The demo notebook output shows self-reported FST5 at 214 and FST6 at 143. Those are about 8.5% and 5.7% of the roughly 2,500 contributors who self-reported. That denominator is my inference. I couldn't get the eFST or eMST tables, so I can't give counts for V–VI or Monk 8–10 on the estimated labels. Table S11 of the paper suggests Monk 10 is nearly absent.
- **Limits:**
  - Diagnoses are dermatologist opinions from photos, not biopsy results, and some images have several or uncertain labels.
  - The Monk labels come from nonclinical labelers in two geographies and differ between them. The schema has separate US and India label columns.
  - Check how many images per tone survive your gradability filters.
- **Access:** Open Google Cloud Storage bucket `dx-scin-public-data`. `scin_demo.ipynb` shows how to load it. The SCIN Data Use License applies, so read it before use.
- **Links:** [GitHub](https://github.com/google-research-datasets/scin), [paper](https://arxiv.org/pdf/2402.18545), [schema](https://github.com/google-research-datasets/scin/blob/main/dataset_schema.md)

**3. Fitzpatrick17k**
- **Contents:** 16,577 clinical images with Fitzpatrick I–VI labels and 100+ conditions, scraped from the DermaAmin and Atlas Dermatologico atlases.
- **Dark-skin coverage:** One review reports only 635 images of type VI. I didn't verify that or the type V count.
- **Limits:**
  - It has duplicates and label errors, and the Fitzpatrick labels were annotated rather than clinically assessed.
  - Diagnoses are not biopsy-confirmed.
  - Use it as a large supplement, not as your main benchmark.
- **Access:** `fitzpatrick17k.csv` is on GitHub. The images must be downloaded from the URLs in the CSV, and some links are broken. You can instead fill out the maintainers' form to get a link to all the images. The license is CC BY-NC-SA 3.0.
- **Link:** [GitHub](https://github.com/mattgroh/fitzpatrick17k)

## Worth considering, but not fully verified
- **PASSION:** 4,901 images from 1,653 patients in Sub-Saharan Africa. It is mostly pediatric (eczema, fungal infections, scabies, impetigo), so it is a narrow condition set that probably has many dark-skin images. I couldn't find the Fitzpatrick distribution, the download location or the license. Check [passionderm.github.io](https://passionderm.github.io) and the [paper](https://arxiv.org/abs/2411.04584).
- **DermaCon-IN:** A search summary says 5,450 images from India with both Fitzpatrick and Monk labels. I didn't open it, so confirm that it exists, how to access it and the tone distribution before relying on it.

## Not suitable
**PAD-UFES-20** has CC BY 4.0 licensing and clinical metadata, but only 579 of 1,373 patients have Fitzpatrick type recorded and just one image is type VI.

## Suggested setup
Use DDI as the primary benchmark because its labels are biopsy-proven and its V–VI group is large. Add SCIN for Monk-scale analysis and more conditions. Fitzpatrick17k can serve as a large, noisier robustness check. Keep in mind that Fitzpatrick and Monk labels measure different things, and that SCIN's labels are estimated from photos.

Sources:
- [Skin Type Diversity in Skin Lesion Datasets: A Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11343783/)
- [PASSION for Dermatology (arXiv)](https://arxiv.org/pdf/2411.04584)
- [SCIN GitHub](https://github.com/google-research-datasets/scin)
- [SCIN paper](https://arxiv.org/pdf/2402.18545)
- [SCIN demo notebook](https://github.com/google-research-datasets/scin/blob/main/scin_demo.ipynb)
- [DDI, Science Advances](https://www.science.org/doi/10.1126/sciadv.abq6147)
- [DDI project page](https://ddi-dataset.github.io)
- [DDI on Redivis](https://stanford.redivis.com/datasets/3r16-5mby7gfer)
- [Fitzpatrick17k GitHub](https://github.com/mattgroh/fitzpatrick17k)