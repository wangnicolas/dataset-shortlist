## What I assumed you need
- **R1 (must):** adult ICU time series of routine vitals and labs.
- **R2 (must):** a time-stamped sepsis onset label (Sepsis-3 or close), or data you can derive one from.
- **R3 (must):** thousands of patients in a clear setting.
- **R4 (nice to have):** data you can get within about a week.

I checked everything against PhysioNet's registry and pages on 2026-11-11/12. I marked anything I didn't re-read today as "memory".

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PhysioNet/CinC Challenge 2019, sepsis | **Open download, minutes** | CC-BY-4.0 | 40,336 ICU stays | Strong; label included | Today |
| 2 | MIMIC-IV v3.1 | Credentialed, days to weeks | PhysioNet Credentialed Health Data License | Large (single centre) | Strong; you derive the label | Today |
| 3 | eICU-CRD v2.0 | Credentialed, same route as MIMIC-IV | PhysioNet Credentialed Health Data License | Multi-centre US | Strong; you derive the label | Today |
| 4 | HiRID v1.1.1 | Credentialed plus author approval, weeks | PhysioNet Contributor Review Health Data License | ~34k admissions | Strong; you derive the label | Today |
| 5 | SICdb v1.0.8 | Credentialed plus contributor approval, weeks | PhysioNet Contributor Review Health Data License | Not checked | Partial; label unclear | Today |
| 6 | AmsterdamUMCdb | Application, DANS licence | DANS Licence | ~23k admissions (memory) | Strong if the Sepsis-3 code works | Registry record only; access terms from memory |

## Details
**1. Challenge 2019 (start here).** Link: https://physionet.org/content/challenge-2019/1.0.0/
- It has hourly vitals and labs plus an hourly sepsis label, so you can run a baseline this week.
- The label is a challenge convention, not a charted event. From memory, onset is set 6 hours before clinical suspicion of infection, using Sepsis-3 criteria.
- It has only about 40 variables, with shifted times. You can't re-derive onset from source tables, and the hidden test set was never released.
- Don't use the Hugging Face copies. They are unofficial.

**2–5. PhysioNet credentialed datasets.** All four share one route:
1. Create a PhysioNet account.
2. Complete the CITI "Data or Specimens Only Research" course. Per PhysioNet's instructions, affiliate with "Massachusetts Institute of Technology Affiliates" and upload the training report, not the certificate.
3. Submit the credentialing application.
4. Sign the data use agreement for each dataset.

- PhysioNet's registry text says only credentialed users who sign the agreement can access the files.
- Access is personal, so each person on your team applies separately.
- One credentialing covers all of these datasets, but each needs its own agreement.
- HiRID and SICdb add a step. You submit a specific research question and the authors or contributors approve it. The pages say this, so budget extra time for it.
- None of these has a Sepsis-3 column. You derive onset from SOFA plus suspected infection (antibiotic and culture timing). MIMIC-IV is the easiest for this, because it has well-documented antibiotic and culture tables and open community code (from memory).
- eICU has a demo (100 stays, open, ODbL licence) at https://physionet.org/content/eicu-crd-demo/2.0.1/. MIMIC-IV has one too at https://physionet.org/content/mimic-iv-demo/2.2/. You can build your pipeline on these while you wait.
- Don't paste restricted records into hosted AI tools. PhysioNet's 24 Sept 2025 policy prohibits it unless zero retention and no training are verified.

**6. AmsterdamUMCdb.** Link: https://doi.org/10.17026/dans-22u-f8vd
- The registry lists it as application-based under the DANS Licence.
- A GigaDB record titled "Sepsis-3 criteria in AmsterdamUMCdb: open-source code implementation" exists (https://doi.org/10.5524/102204).
- The landing and access pages wouldn't load, so the process is from memory: a request plus a signed licence agreement. Confirm it before planning around it.

## Known, not confirmed
- **AmsterdamUMCdb access steps and timing.** I know the registry says "application". I tried the DOI, the DataCite API and GitHub, and all failed with connection errors. Check the DOI page.
- **SICdb sepsis fit.** The page lists sepsis detection as an application area. I didn't verify antibiotic or culture data, which you'd need to derive onset. Check https://www.sicdb.com/Documentation/.
- **Challenge 2019 label definition.** The 6-hour rule is from memory. Check it against the challenge paper.

## Not recommended, and why
- **PhysioNet/CinC Challenge 2012.** It predicts mortality only.
- **GOSSIS-1 / WiDS 2020.** These are severity-score summaries, not time series with onset.
- **Zigong infection ICU database.** It is a single-hospital infection cohort. I didn't check it for onset labels or time series, and it needs credentialing.
- **Zenodo sepsis records.** These are small clinical-study supplements or unrelated records, not ICU time series.

## What I could not find
- **Literature evidence of use.** The paper search returned almost nothing, so I have no verified papers to cite for any dataset. Search for the 2019 challenge's official results paper and for HiRID benchmark papers yourself.
- **Newer derived datasets.** I saw MIMIC-IV-Ext-CLIF in the results but didn't evaluate it. I also didn't look for pre-built Sepsis-3 tables.

## Next step
1. Today, download Challenge 2019 and build the baseline.
2. Today, start the CITI course and the PhysioNet credentialing application. Ask your supervisor for the reference or sign-off the form needs.
3. In parallel, develop your Sepsis-3 derivation on the MIMIC-IV demo, then run it on full MIMIC-IV once approved.
4. Use eICU or HiRID later for external validation.

I can't say how long credentialing will take from this check. Confirm the current review times on PhysioNet.

Interactive page: `/private/tmp/e-HIuBPH/home/cwd/dataset-shortlist.html`