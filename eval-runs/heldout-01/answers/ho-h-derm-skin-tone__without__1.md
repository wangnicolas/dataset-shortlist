Three public datasets fit, and I'd use them together. These are from memory, so check the counts and license terms on each dataset's page before you commit.

| Dataset | Size | Skin tone label | Diagnosis label | Types V/VI |
|---|---|---|---|---|
| **DDI (Diverse Dermatology Images, Stanford)** | ~656 images, ~570 patients | Fitzpatrick, grouped as I–II, III–IV, V–VI | Biopsy-confirmed | Roughly a third of the images, about 200 |
| **SCIN (Google)** | ~10k+ images, thousands of contributors | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick, and Monk Skin Tone estimates | Dermatologist differential diagnoses, not biopsy | A few hundred to low thousands, depending on which label you use |
| **Fitzpatrick 17k** | ~16.5k images, 114 conditions | Fitzpatrick I–VI per image (crowd-annotated) | Taken from the source atlases (DermaAmin, Atlas Dermatológico) | A couple thousand combined, but V and VI are much rarer than I–III |

**How I'd use them**
- **DDI** is the best ground truth. Its diagnoses are biopsy-confirmed, and the dark-skin subset was built for exactly this kind of audit. It's small, so subgroup confidence intervals will be wide, and the skin tone label is a V–VI group rather than a single type. Access goes through a Stanford AIMI data use agreement.
- **SCIN** is the only one with Monk labels. It's a good large-scale complement. Its diagnoses are probabilistic differentials, so decide up front how to turn them into a single label, such as the top-weighted condition or only cases above a confidence threshold. It's also self-submitted, mostly smartphone-quality, and covers common inflammatory conditions more than cancers.
- **Fitzpatrick 17k** has the most dark-skin volume. Its labels are noisy: skin tone was annotated by non-dermatologists from web images, diagnoses come from the source sites rather than pathology, and there are duplicates and unlabeled entries (coded -1) to filter out. Use it for stress-testing, and don't treat its labels as ground truth.

**Datasets to skip for this audit**
- **PAD-UFES-20** has per-patient Fitzpatrick labels, but almost all patients are type I–III, so V and VI barely appear.
- **HAM10000, BCN20000, and most of the ISIC archive** have no skin tone labels and are heavily skewed toward light skin. Estimating tone with ITA (individual typology angle) is possible but unreliable, and I wouldn't use it as your label.

**Caveats for the audit**
- Use patient-level splits where patient IDs exist (DDI, SCIN). Fitzpatrick 17k has no patient IDs, so check for near-duplicates.
- Condition mix differs across skin tones in all three datasets. A gap by tone can partly reflect which diseases were photographed, so stratify by condition or restrict to conditions present in both light and dark groups.
- Fitzpatrick and Monk labels are estimated from photos, and they disagree with each other. SCIN lets you check how much your result changes depending on which label you use.

I can pull the current download links and exact Fitzpatrick V/VI counts for each dataset if you'd like.