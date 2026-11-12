**Short answer:** you can start today on the PhysioNet/CinC Challenge 2019 data, which has a time-stamped sepsis label and needs no application. The larger datasets (MIMIC-IV, eICU, HiRID and others) need PhysioNet credentialing, which PhysioNet's FAQ puts at about 1–2 weeks. That is tight for a one-week deadline, so start the application today.

## What I assumed you need
- **R1 (must):** a time-stamped sepsis onset label, or data from which you can derive Sepsis-3 onset (suspected infection plus a SOFA rise).
- **R2:** adult ICU vitals and labs.
- **R3 (nice to have):** access fast enough for a baseline within a week.
- I assumed an academic, non-commercial project.

## Shortlist
| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | [PhysioNet/CinC Challenge 2019](https://physionet.org/content/challenge-2019/1.0.0/) | Open download, minutes | CC-BY-4.0 | Strong: label already provided | Registry today; label details from memory |
| 2 | [MIMIC-IV](https://physionet.org/content/mimiciv/) (v3.1) | Credentialed, ~1–2 weeks | PhysioNet Credentialed Health Data License | Strong: derive onset yourself | Today |
| 3 | [eICU-CRD](https://physionet.org/content/eicu-crd/) | Credentialed, same approval as MIMIC | Credentialed license | Strong for multi-centre validation; derive onset | Today |
| 4 | [HiRID](https://physionet.org/content/hirid/1.1.1/) | Credentialed plus approval from the data contributors | Contributor Review license | Strong for temporal models; derive onset | Today |
| 5 | [SICdb](https://physionet.org/content/sicdb/1.0.8/) | Credentialed plus contributor approval | Contributor Review license | Partial: external validation | Today |
| 6 | [NWICU](https://doi.org/10.13026/4je9-db46) | Credentialed | Credentialed license | Unknown: I didn't check whether it has enough infection data | Today (access only) |
| 7 | [MIMIC-III](https://physionet.org/content/mimiciii/1.4/) | Credentialed | Credentialed license | Partial: superseded by MIMIC-IV | Today |
| 8 | [MIMIC-IV Demo](https://physionet.org/content/mimic-iv-demo/2.2/) | Open | ODbL-1.0 | Weak: too small to train on | Today |

## Details
**1. Challenge 2019** is your week-one baseline.
- The page confirms 40,336 subjects, open access and CC-BY-4.0.
- From memory, not confirmed today: it has hourly records from two hospital systems, a per-hour `SepsisLabel` based on Sepsis-3, and about 40 vitals, lab and demographic columns.
- The limit is that the label is fixed. You can't change the onset definition, and the variable set is narrow.

**2–3. MIMIC-IV and eICU** share one access route.
1. Create a PhysioNet account.
2. Complete the CITI "Data or Specimens Only Research" course. Per PhysioNet's instructions, affiliate with "Massachusetts Institute of Technology Affiliates" and avoid registering as an independent learner, to skip fees.
3. Submit the credentialing application with your CITI completion report. It asks about you and your research. I didn't confirm the reference details, so check `physionet.org/settings/profile/`.
4. Once approved, sign the data use agreement on each dataset page. Sharing data within a team is not permitted, so each of your collaborators needs their own approval.
- Neither dataset ships a Sepsis-3 onset label. Both contain the antibiotic, culture, lab and vitals data you need to derive it. The MIT-LCP `mimic-code` repository has Sepsis-3 derivations for MIMIC. That is from memory and I did not check it this session.
- Check the agreement before using any online AI service on this data. PhysioNet's terms restrict that.

**4–5. HiRID and SICdb** need credentialing and a separate request to the data contributors.
- HiRID's page says you must "submit a request to the authors to use the data for your project" and "provide a specific research question".
- SICdb's page says contributors' approval is required.
- Plan for extra time on top of credentialing, and I can't give you an estimate for it. They're best used as external validation sets.

**AmsterdamUMCdb** is worth a mention. A web search says access is free but needs a CITI-type course, a signed agreement and a named reference, and the licence is non-commercial. It is credible but unconfirmed. See the next section.

## Known, not confirmed
- **AmsterdamUMCdb.** I couldn't verify a record page. My guessed URL returned 404 and I did not use it. The site that the search returned is [amsterdammedicaldatascience.nl](https://amsterdammedicaldatascience.nl/). The search result also said the current version is 1.5.0 (OMOP format), and that you request access there and get the data via DANS. Check that site for the current form and whether it has what you need for onset.

## Not recommended
- **WiDS Datathon 2020:** the label is mortality, so there are no onset times.
- **Zenodo/Dryad sepsis records** from the registry search: these are small biomarker or study datasets, not ICU time series.

## What I could not find
- No other open dataset with sepsis onset labels beyond Challenge 2019.
- The literature search mostly timed out or returned irrelevant results, so I can't point you to confirmed papers that used these datasets. You'll find plenty by searching the Challenge 2019 and MIMIC-IV Sepsis-3 literature yourself.
- Registry search covered PhysioNet, Zenodo, OpenAIRE and DataCite. Lesser-known sources may be missing.

## Next step
1. Today: download Challenge 2019 and build the baseline.
2. Today: start the CITI course, create your PhysioNet account and submit the credentialing application. Request MIMIC-IV and eICU, and HiRID if you want it.
3. While you wait: develop your Sepsis-3 derivation on the open MIMIC-IV demo, so it's ready when the full data arrives.

Access terms were checked on 2026-11-11/12, and they can change. The interactive page is at `/private/tmp/e-kOXwcR/home/cwd/dataset-shortlist.html`. Some of its per-requirement evidence text is my own summary, so treat the reply above as authoritative.

Sources: [PhysioNet FAQs](https://physionet.org/about/faqs/), [PhysioNet CITI instructions](https://physionet.org/about/citi-course/), [AmsterdamUMCdb on GitHub](https://github.com/AmsterdamUMC/AmsterdamUMCdb)