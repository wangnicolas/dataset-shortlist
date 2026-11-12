## What I assumed you need

- **R1 (must):** adult ICU time series of vitals and labs.
- **R2 (must):** time-stamped sepsis onset, or enough data to derive Sepsis-3 onset yourself. That means SOFA inputs plus antibiotic and culture timestamps.
- **R3 (nice):** enough patients, ideally from more than one site.
- **R4 (nice):** obtainable within a week.

I checked these on 2026-11-11 against PhysioNet's registry and pages. Items marked "from memory" were not confirmed today.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PhysioNet/CinC Challenge 2019 (early sepsis prediction) | **Open download, minutes** | CC-BY-4.0 | 40,336 patients, 42 MB | Strong | today |
| 2 | MIMIC-IV v3.1 | Credentialed: CITI training and DUA, about 1–2 weeks | PhysioNet Credentialed Health Data License | tens of thousands of ICU stays | Strong (derive onset) | access today, contents from memory |
| 3 | eICU-CRD | Credentialed, same application as MIMIC-IV | PhysioNet Credentialed | about 200k stays | Strong (derive onset) | access today, contents from memory |
| 4 | HiRID (Bern) | Credentialed plus authors' approval of your research question, weeks | PhysioNet Contributor Review | about 34k admissions | Strong (derive onset) | today |
| 5 | AmsterdamUMCdb v1.0.2 | Signed access and licence form via DANS, weeks | DANS Licence | tens of thousands of admissions | Strong (derive onset) | access today |
| 6 | SICdb (Salzburg) | Credentialed plus contributor approval, weeks | PhysioNet Contributor Review | not checked | Partial | today |
| 7 | MIMIC-IV demo / eICU demo | Open, minutes | ODbL-1.0 | about 100 / about 2,500 stays (from memory) | Pipeline testing only | today |

## Details

**1. Challenge 2019: start here today.**
- Link: https://physionet.org/content/challenge-2019/
- The page states there is one hourly file per subject. It has two hospital systems (sets A and B, 20,336 and 20,000 subjects).
- Labels come from Sepsis-3, and the page says they are "shifted… ahead by six hours", so the task is already 6-hour-early prediction.
- Download needs no credentials.
- Caveats:
  - It has a fixed set of about 40 variables, from memory.
  - You can't re-derive the label.
  - The challenge's hidden test set isn't included.
- Official scoring code and a utility function that rewards early predictions are provided.

**2–3. MIMIC-IV and eICU: the main research data.**
- Links: https://physionet.org/content/mimiciv/ and https://physionet.org/content/eicu-crd/
- Neither has an onset column. You derive Sepsis-3 from SOFA plus suspected infection (antibiotics and cultures). Community derivation code exists, from memory.
- Access steps, confirmed on the pages:
  1. Create a PhysioNet account.
  2. Complete CITI's "Data or Specimens Only Research" course. PhysioNet says to affiliate with "Massachusetts Institute of Technology Affiliates" and not register as an independent learner, which avoids extra fees.
  3. Upload the CITI training report, not the certificate.
  4. Apply for credentialing. A reference may be requested, from memory.
  5. Sign the data use agreement.
- Access is personal, so your supervisor and lab mates each apply separately.
- Don't send this data to hosted LLM services. PhysioNet's rule is at https://physionet.org/news/post/llm-responsible-use/.
- MIMIC-IV is single-centre. eICU is multi-centre and is the natural external-validation set.

**4. HiRID.**
- Link: https://physionet.org/content/hirid/
- It has roughly 2-minute resolution from a Swiss ICU, which suits time-series modelling.
- The page says you must be credentialed, sign the DUA "and provide a specific research question". The data authors approve the request, so timing is less predictable.

**5. AmsterdamUMCdb.**
- Link: https://doi.org/10.17026/dans-22u-f8vd
- The record is restricted and points to a signed access request and end-use licence form (details at github.com/AmsterdamUMC/AmsterdamUMCdb). Whether the form needs an institutional signature is from memory, so check it.
- A DataCite record titled "Sepsis-3 criteria in AmsterdamUMCdb: open-source code implementation" exists, which could save you derivation work.

**6. SICdb.** The page says contributor approval is required, along with PhysioNet credentialing and a research question. It is a possible later validation site.

**7. Demos.** The open MIMIC-IV and eICU samples are too small to model. Use them to write and test your Sepsis-3 pipeline while credentialing is pending.

## Known, not confirmed

- **Paper citations:** the literature APIs returned almost nothing, so I'm citing no papers. Check the Challenge 2019 paper (Reyna et al., *Critical Care Medicine*), which the page says is the official one.
- **Contents of MIMIC-IV, eICU and AmsterdamUMCdb:** I didn't read the variable lists today. Sizes and derivation code availability are from memory.
- **Credentialing timing:** "about 1–2 weeks" is from memory.

## Not recommended, and why

- **Hugging Face copies of the Challenge data:** unofficial mirrors. Use PhysioNet.
- **Zenodo and OpenAIRE sepsis supplements:** these have mortality, biomarker or single-study tables, with no hourly vitals or onset times.
- **MIMIC-style datasets with only discharge codes:** ICD-coded sepsis gives no onset time.

## What I could not find

- An open, multi-centre dataset with raw Sepsis-3 inputs and no application.
- Working literature search results this session.
- The old Amsterdam URL (amsterdammedicaldatascience.nl/amsterdamumcdb/) returned 404, so use the DOI link.

## Next step

1. Today: download Challenge 2019 and run a baseline against its utility score.
2. Today: start the CITI course and the PhysioNet credentialing application. That is the slow part.
3. While you wait: build your Sepsis-3 derivation on the MIMIC-IV demo.
4. After approval: train on MIMIC-IV and validate externally on eICU. Ask the HiRID authors in parallel.

Interactive page (filter, compare, export an access plan): `/private/tmp/e-upQ7Yk/home/cwd/dataset-shortlist.html`