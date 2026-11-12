Four public datasets meet your bar, each with a different weakness, and none gives you large, clinician-verified type VI numbers. I checked the counts below against the papers and repos today, except where marked.

| Dataset | Size and type | Skin tone label | Diagnosis label | V/VI representation |
|---|---|---|---|---|
| **Fitzpatrick17k** | 16,577 clinical photos from two online atlases | Fitzpatrick I–VI per image, assigned by non-expert annotators from the photo | 114 conditions, taken from atlas captions (noisy) | 1,533 type V and 635 type VI, about 13% |
| **DDI** (Stanford) | 656 clinical images | Fitzpatrick per image, released in three groups (I–II, III–IV, V–VI) | Pathologically confirmed | 207 V–VI images (159 benign, 48 malignant) |
| **PASSION** | 4,901 clinical images, 1,653 patients, sub-Saharan Africa, mostly paediatric | Fitzpatrick; cohort is IV–VI only | Eczema, fungal infections, scabies, impetigo | Essentially the whole dataset; I could not confirm per-type counts |
| **SCIN** (Google) | 10,000+ images, 5,033 crowdsourced US cases | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick and layperson-estimated Monk | Weighted dermatologist differential over 419 conditions, on 2,835 cases | Self-reported: 9.8% V, 6.6% VI, but only 2,500 cases self-reported |

- **Fitzpatrick17k**: This is the largest dark-skin pool with broad disease coverage. A cleaned version, Fitzpatrick17k-C, keeps 11,394 images after removing duplicates and bad labels.
- **DDI**: It has the best label quality and was built for exactly this audit. It is small, though, so per-disease comparisons are underpowered, and one study noted it has no basal cell carcinoma in V–VI.
- **PASSION**: With no light-skin images, you would have to pair it with another dataset for the comparison, which confounds skin tone with site, camera and disease mix. The licence is CC BY-NC 4.0.
- **SCIN**: It is the only one with both scales. The dark-skin share depends heavily on which label you use: dermatologist-estimated Fitzpatrick gives only 5.3% V and 0.6% VI, and Monk 7–10 is under 2% by US labellers.

**DermaCon-IN** is a borderline fifth: 5,450 clinical images from about 3,000 patients in South India, with expert-assigned Fitzpatrick and Monk labels and 245 diagnoses. It skews to types IV and V, and I could not confirm how many type VI images it has. It is on Harvard Dataverse under CC BY-NC-SA 4.0.

These carry skin tone labels but fail your representation requirement:

- **MRA-MIDAS**: About 83% of its 796 patients are types I–II, and one preprint found zero V–VI cancers.
- **MILK10k**: It uses its own 0–5 tone scale, and only six cases carry the darkest label.
- **ISIC archive**: One group filtering by Fitzpatrick found 10 type V images and one type VI.
- **PAD-UFES-20**: From memory, not checked today, it has Fitzpatrick metadata but almost no V–VI.

For the audit itself, I would use DDI as the primary test set, since tone and diagnosis are both trustworthy. Fitzpatrick17k (cleaned) and SCIN then add breadth across non-cancer conditions, with results reported separately per dataset rather than pooled.

Sources:
- [Fitzpatrick17k paper (arXiv 2104.09957)](https://arxiv.org/pdf/2104.09957)
- [CleanPatrick / Fitzpatrick17k-C (arXiv 2505.11034)](https://arxiv.org/pdf/2505.11034)
- [Pipsqueak paper, with Fitzpatrick17k per-type counts and ISIC filtering](https://www.sciencedirect.com/science/article/pii/S1877750326000761)
- [DDI paper (Science Advances)](https://www.science.org/doi/10.1126/sciadv.abq6147)
- [PASSION paper (arXiv 2411.04584)](https://arxiv.org/abs/2411.04584)
- [PASSION project repo](https://github.com/Digital-Dermatology/PASSION_project)
- [SCIN paper (arXiv 2402.18545)](https://arxiv.org/html/2402.18545)
- [SCIN repo](https://github.com/google-research-datasets/scin)
- [DermaCon-IN paper (arXiv 2506.06099)](https://arxiv.org/html/2506.06099)
- [MIDAS paper (NEJM AI)](https://ai.nejm.org/doi/full/10.1056/AIdbp2400732)
- [MILK10k paper (JID)](https://www.jidonline.org/article/S0022-202X(25)02270-5/fulltext?rss=yes)
- [Colorimeter-supervised skin tone audit (arXiv 2602.10265)](https://arxiv.org/html/2602.10265v1)
- [Global Atlas of Digital Dermatology (arXiv 2601.00840)](https://arxiv.org/pdf/2601.00840)