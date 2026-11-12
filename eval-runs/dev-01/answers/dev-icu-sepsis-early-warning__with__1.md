## What I assumed you need

- **R1 (must):** A time-stamped sepsis onset, either given (Sepsis-3 or close) or derivable.
- **R2 (must):** Routinely charted vitals and labs over time.
- **R3 (must):** Adult ICU patients, thousands or more.
- **R4 (nice to have):** A first baseline possible within a week.

I assumed you have a supervisor or colleague who can vouch for you and a university email address. I also assumed you can't run restricted data through hosted AI services (see the PhysioNet note under MIMIC-IV).

I checked the registries on 2026-11-11 and 2026-11-12. Access rules change, so check each page again before you apply.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit |
|---|---|---|---|---|---|
| 1 | PhysioNet/CinC Challenge 2019 | **Open download, minutes** | CC-BY-4.0 | 40,336 ICU patients (two public hospital systems), hourly | Strong. Onset label is given. |
| 2 | MIMIC-IV 3.1 | Credentialed, days to weeks | PhysioNet Credentialed DUA | 94,458 ICU stays, 65,366 patients (Boston, 2008–2022) | Strong. You derive the label. |
| 3 | eICU-CRD | Credentialed (same application as #2) | PhysioNet Credentialed DUA | 200k+ unit stays, 208 US hospitals, 2014–2015 | Strong for external validation. You derive the label. |
| 4 | HiRID 1.1.1 | Credentialed plus per-study review by the authors, weeks | PhysioNet Contributor Review DUA | ~34k admissions (Bern, 2008–2016), 681 variables | Strong. You derive the label. |
| 5 | AmsterdamUMCdb | Application at amsterdammedicaldatascience.nl; steps not confirmed | DANS licence | 23,106 admissions (2003–2016) | Partial. You derive the label. |
| 6 | SICdb 1.0.8 | Credentialed plus per-study review by the authors, weeks | PhysioNet Contributor Review DUA | 27k+ admissions (Salzburg, 2013–2021) | Partial. You derive the label. |
| 7 | MIMIC-IV Demo | Open | ODbL-1.0 | Demo subset | Pipeline development only |

## Details

**Start today: Challenge 2019** ([link](https://physionet.org/content/challenge-2019/1.0.0/))
- **Contents:** 40 variables per hour: 8 vitals, 26 labs and 6 demographic or unit fields, plus a `SepsisLabel`. The label follows Sepsis-3: a 2-point SOFA change plus suspected infection (cultures or IV antibiotics). Onset is the earlier of the two times.
- **Third hospital:** A third hospital system is hidden and used for scoring.
- **Caveat on the label:** The page says the training labels are shifted 6 hours earlier. Check how that fits your target definition.
- **Limits:** There are no raw medications or cultures, so you can't rederive onset with a different Sepsis-3 variant. It is also heavily used, so novelty has to come from your method or evaluation.
- **Access:** None needed. Download it.

**Apply now: MIMIC-IV** ([link](https://physionet.org/content/mimiciv/3.1/))
- **Contents:** Charted vitals, labs, inputs, cultures and prescriptions, so you can derive Sepsis-3 onset yourself. The page has no sepsis label.
- **Access steps:**
  1. Create a PhysioNet account.
  2. Complete CITI "Data or Specimens Only Research" training.
  3. Submit the credentialing application, which includes references.
  4. Sign the Credentialed DUA on the dataset page.
- **Time:** I couldn't confirm a typical approval time from the pages. The CITI course takes a few hours.
- **Personal access:** Access is per person. Your teammates apply separately.
- **AI services:** The agreement bars sending the data through APIs or online platforms. PhysioNet recommends locally run models ([their post](https://physionet.org/news/post/llm-responsible-use/)). Don't paste records into hosted tools.
- **Related paper:** MIMIC-Sepsis ([doi](https://doi.org/10.1109/bhi67747.2025.11269536)) is a curated cohort of 35,239 ICU patients from MIMIC-IV. I only read its abstract and didn't confirm where its code is released.

**eICU-CRD** ([link](https://physionet.org/content/eicu-crd/2.0/))
- It uses the same credentialing as MIMIC-IV, so one application covers both.
- It has no sepsis label, and charting varies by hospital.
- It is mainly useful for external validation.

**HiRID and SICdb**
- Both need credentialing, plus a specific research question submitted to the dataset authors.
- Neither page states a turnaround time.
- Neither has a sepsis label.
- HiRID is ~18 GB.

**AmsterdamUMCdb** ([DOI](https://doi.org/10.17026/dans-22u-f8vd))
- The README sends you to amsterdammedicaldatascience.nl.
- I couldn't load that site, so steps, eligibility, cost and timing are unconfirmed.
- A Sepsis-3 implementation for this dataset exists ([supporting data](https://doi.org/10.5524/102204)).

**Multi-dataset benchmark**
- The YAIB framework supports MIMIC-III/IV, eICU, HiRID and AmsterdamUMCdb, and sepsis is one of its five predefined tasks ([paper](https://arxiv.org/abs/2306.05109), [code](https://github.com/rvandewater/YAIB)).
- I didn't confirm how it defines sepsis. It may save you from writing your own cohort code.
- A related paper pooled four public ICU datasets (334,812 stays) to test how well models transfer to new hospitals ([doi](https://doi.org/10.1097/ccm.0000000000006359)). I read only its abstract and didn't confirm that sepsis is one of its tasks.

## Not recommended, and why

- **WiDS Datathon 2020:** It predicts mortality, not timed sepsis onset.
- **Health Gym synthetic sepsis data:** It is synthetic, derived from MIMIC-III, and credentialed anyway.
- **Hugging Face copies of the Challenge 2019 data:** They are unofficial mirrors. Use the PhysioNet original.
- **Neonatal and omics sepsis sets on Zenodo:** They are the wrong population or modality.

## What I could not find

- I couldn't confirm real-world approval times for PhysioNet credentialing or the HiRID and SICdb author reviews. Ask people in your lab who applied recently.
- I couldn't load the AmsterdamUMCdb application page.
- I didn't confirm where MIMIC-Sepsis releases its code or cohort.
- Some registry queries failed (DataCite, Zenodo, Hugging Face), so coverage may be incomplete.
- I didn't assess non-Western ICU databases, such as the Zhejiang critical care EHR set that showed up in results.

## Next step

1. **Today:** Download Challenge 2019 and build your baseline on it. Start the CITI training and the PhysioNet credentialing application, and ask your supervisor to confirm the reference. Also ask your institution whether this work needs an ethics exemption.
2. **While waiting:** Use the MIMIC-IV demo to write your Sepsis-3 derivation pipeline. Then apply for HiRID once you have a concrete research question.
3. **After approval:** Train on MIMIC-IV and validate externally on eICU or HiRID.

Interactive page: `/private/tmp/e-b61852/home/cwd/dataset-shortlist.html`