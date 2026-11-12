The best fit is **DermaCon-IN**, **Fitzpatrick17k**, **SCIN** and **DDI**, and each has a gap you should know about. I checked access and licence for most of them on 2026-11-11. I did not check the per-type image counts, so every count below is from memory unless I say otherwise.

I didn't build the interactive HTML page, so there is no `dataset-shortlist.html`. The registry search covered Hugging Face, Zenodo, DataCite, OpenAIRE and PhysioNet.

## What I assumed you need
- **R1 (must):** skin images with a diagnosis label.
- **R2 (must):** a Fitzpatrick or Monk label per image or patient.
- **R3 (must):** Fitzpatrick V–VI present in numbers large enough to give stable subgroup metrics.
- **R4 (nice):** patient IDs, so you can split by patient.
- **R5 (nice):** downloadable now.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | DermaCon-IN | Open download (Harvard Dataverse) | CC BY-NC-SA 4.0 | 5,450+ images, ~3,000 patients, 240+ diagnoses | Skin tone scores per image, South Indian patients, so likely V–VI-heavy. The scale and distribution are unchecked. | Record today; skin tone scale not verified |
| 2 | Fitzpatrick17k | Open: GitHub CSV, images fetched from the source atlases | CC BY-NC-SA 3.0 | 16,577 images, 114 conditions | Fitzpatrick label on every image. V–VI is a minority, and I recall roughly a tenth. | Page today; counts from memory |
| 3 | SCIN (Google) | Open download, under the SCIN Data Use License | SCIN Data Use License | 10,000+ images | Dermatologist-estimated Fitzpatrick, layperson Monk and self-reported Fitzpatrick. Diagnoses are dermatologist differentials. V–VI is a minority. | Page today; counts from memory |
| 4 | DDI (Stanford Diverse Dermatology Images) | Free registration and research use agreement | Non-commercial research use | ~656 images, ~570 patients (memory) | Biopsy-proven diagnoses. Built to compare I–II against V–VI. I recall about 200 V–VI images. | Page today; counts from memory |
| 5 | "Black skin lesions" (Zenodo 10570316) | Request form; files restricted | CC BY-NC-SA 4.0 | Unknown | Acral lesions, assessed against the Fitzpatrick scale. | Access page today; contents not read |
| 6 | MRA-MIDAS (Stanford AIMI) | Registration or data agreement; I couldn't read the terms | Not stated | Not checked | Fitzpatrick type per lesion and biopsy-based labels. I don't know the V–VI share. | Page today; V–VI share unknown |

## Details
- **DermaCon-IN** (https://doi.org/10.7910/dvn/w7ouzm). It is prospective clinical photos with hierarchical diagnoses and body location. The record says "skin tone scores" without naming the scale, so check whether it is Fitzpatrick before you rely on it. Harvard Dataverse blocked my automated check, so open the page in a browser.
- **Fitzpatrick17k** (https://github.com/mattgroh/fitzpatrick17k). The page says it holds "16,577 clinical images sourced from two dermatology atlases" labelled by Scale AI and Centaur Labs. Two caveats:
  - The skin tone labels are crowd-annotated and noisy.
  - There are no patient IDs, and I recall near-duplicates, so a patient-level split isn't possible. The Zenodo record "Investigating the Quality of DermaMNIST and Fitzpatrick17k" (https://zenodo.org/records/12739457) covers its quality problems.
- **SCIN** (https://github.com/google-research-datasets/scin). The page states "estimated Fitzpatrick skin type (eFST) and layperson estimated Monk Skin tone (eMST)". It is the only one here with Monk labels. The images are US crowd-donated, not clinical, and the diagnoses are differentials rather than biopsy-proven. A JAMA Network Open paper describes it (https://doi.org/10.1001/jamanetworkopen.2024.46615).
- **DDI** (https://ddi-dataset.github.io/). The page says it was designed to compare I–II with V–VI, matched on diagnostic category, age, gender and photo date. It also says "personal, non-commercial research purposes only". A Stanford group used it to test LLM accuracy by skin tone (https://doi.org/10.1111/ijd.70452).
- **Black skin lesions** (https://zenodo.org/records/10570316). The page says "The record is publicly accessible, but files are restricted" and asks you to fill in a form. It may be useful for acral lesions. I haven't seen its contents or label scheme.
- **MRA-MIDAS** (https://doi.org/10.71718/15nz-jv40). Pages say Fitzpatrick type was recorded per lesion. Stanford AIMI datasets usually need registration, but I couldn't read the terms. If V–VI is thin, it fails R3.

## Known, not confirmed
- **PASSION** (Digital-Dermatology group): from memory, about 4,900 pediatric images from several Sub-Saharan African countries, mostly Fitzpatrick IV–VI, with a handful of common conditions. This could be the strongest source of V–VI images. The registry search didn't find it. Check its Hugging Face page and the paper, and confirm the licence and access terms.
- **DDI-2** (https://doi.org/10.57761/pgwn-6b62). The record describes 665 images from 550 self-identified Asian patients with biopsy-proven diagnoses and Fitzpatrick type. The access tier is unknown, and the page is rendered by JavaScript so I couldn't read it. I expect mostly types III–IV, so it adds little for V–VI.

## Not recommended, and why
- **HAM10000, ISIC archives:** no skin tone labels, and the population is predominantly light-skinned.
- **PAD-UFES-20** (https://data.mendeley.com/datasets/zr7vgbcyr2/1): open and CC BY 4.0. The metadata includes Fitzpatrick type, but from memory it has many missing values and almost no V–VI.
- **SOS-ALL** (Zenodo 21064520): an amaXhosa dermatitis cohort, but a 123 KB tabular file with no images.
- **FitzDerm-CF** (https://doi.org/10.7910/dvn/ozks1l): synthetic text notes layered on Fitzpatrick17k and DDI images. It is derivative, so use the originals.
- **Other registry hits:** the Hugging Face copies, "DermaMNIST" and the Fitzpatrick-prompting LLM papers' supplements are re-uploads or unrelated.

## What I could not find
- Verified V and VI counts for any dataset. Count them yourself from the metadata files before committing.
- A clinical dataset with Monk labels other than SCIN.
- PASSION in the registries, as noted above.

## Next step
1. Download the Fitzpatrick17k CSV and the SCIN tables (a few minutes each) and tabulate V–VI by diagnosis.
2. Open DermaCon-IN in a browser and confirm the scale.
3. Register for DDI.

Together these should give you a workable V–VI subgroup. Fitzpatrick17k has the largest, noisiest set. DDI has the cleanest, biopsy-proven set. DermaCon-IN and PASSION may give you the deepest V–VI coverage.