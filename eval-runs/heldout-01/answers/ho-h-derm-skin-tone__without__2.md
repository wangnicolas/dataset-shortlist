Three public datasets meet your requirements, and I'd combine them. I'm working from memory and didn't check the live pages, so verify the counts and licenses before you commit to a protocol.

## Best fits

| Dataset | Images | Skin tone label | Diagnosis | Darker-skin coverage |
|---|---|---|---|---|
| **DDI** (Diverse Dermatology Images, Stanford AIMI) | 656 images, 570 patients | Fitzpatrick, grouped as I–II, III–IV, V–VI | Biopsy-proven, benign and malignant | About a third of images are V–VI, by design |
| **Fitzpatrick 17k** | About 16.5k clinical images, 114 conditions | Fitzpatrick I–VI | Condition label from the source atlases | V and VI are a minority but number in the high hundreds to low thousands |
| **SCIN** (Google, Skin Condition Image Network) | About 10k images from about 5k contributors | Self-reported Fitzpatrick, plus dermatologist-estimated Fitzpatrick and **Monk Skin Tone** | Dermatologist differential diagnoses, with weighted confidence and no biopsy | Substantial. Collected from US volunteers with an explicit aim of broad skin tone coverage |

- **DDI** is the best choice for the audit itself. It is small, but the skin tone groups are balanced and the diagnoses are pathology-confirmed. Skin tone was labeled by clinicians. Access requires agreeing to Stanford's terms, which are for research use.
- **Fitzpatrick 17k** is the largest and covers the widest range of conditions. Its tone labels were annotated from the images, not assessed on the patient, so they are noisy. The repo (`mattgroh/fitzpatrick17k`) ships a CSV with image URLs, and you scrape the images yourself. Some links have died. It's also not skin cancer only. Diagnoses come from the source atlases and are not all biopsy-confirmed.
- **SCIN** is the only one of the three with Monk labels. Its diagnoses are probabilistic dermatologist differentials, not ground truth. Its images are patient-taken, so they differ from clinic photos or dermoscopy. This is also a distribution-shift confound when you compare it with the other two.

## Datasets that look relevant but aren't
- **HAM10000, ISIC 2019/2020, BCN20000, Derm7pt:** No usable skin tone labels, and they are overwhelmingly light-skinned. Some papers estimate tone from pixels (ITA), but that is a proxy, not a label.
- **PAD-UFES-20:** It has Fitzpatrick metadata, but almost all patients are type I–III, so V and VI are too thin for subgroup testing.

## Cautions for the audit
- **Fitzpatrick is a tanning and burning scale, not a measure of skin color.** Labels from different datasets also aren't calibrated against each other. Pooling datasets adds label noise, so I'd report results per dataset first.
- **Condition mix differs by tone.** In Fitzpatrick 17k and SCIN, the conditions photographed for dark skin differ from those for light skin. A drop in dark-skin performance can come from the condition mix or the image source, not skin tone. Stratify by condition, or use DDI's matched benign/malignant design to control for it.
- **Subgroups can be small.** DDI's V–VI group has only about 200 images, so report confidence intervals.
- **SkinCon** adds clinician concept annotations (such as erythema and scale) to Fitzpatrick 17k and DDI. It can help explain why errors differ by tone.

I'd run DDI as the primary audit, Fitzpatrick 17k for statistical power, and SCIN as a Monk-scale cross-check. I can look up the current access pages and licenses for these, or draft a script that downloads and joins the metadata.