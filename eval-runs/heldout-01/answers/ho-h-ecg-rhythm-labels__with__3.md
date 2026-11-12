The best option is PTB-XL, plus the Chapman-Shaoxing/Ningbo database. Both are direct downloads with no account, application or signed agreement. Together they cover AF, LBBB, RBBB and AV block in tens of thousands of cardiologist-labelled 12-lead ECGs, and you can start today.

I confirmed the records, licences and access conditions today (2026-11-12) against PhysioNet and Zenodo. I did not build the interactive shortlist page, to keep this quick. Record counts, class lists and label provenance come from my memory and the dataset papers, not from checking each file. Check the class counts before you commit.

## What I assumed you need
- **Must have:** 10-second 12-lead resting ECGs, with labels for AF and for LBBB, RBBB and AV block, assigned or confirmed by physicians or cardiologists.
- **Must have:** at least a few thousand recordings, downloadable this week with no application, credentialing or data use agreement.
- **Nice to have:** a licence that allows publication and redistribution of derived work, and prior papers to benchmark against.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [PTB-XL](https://physionet.org/content/ptb-xl/1.0.3/) | Open download, no account | CC-BY-4.0 | ~21.8k records (memory) | Strong. Has AF, LBBB, RBBB and 1st-degree AV block. Higher-degree AV block is rare. | Access and licence today; contents from memory |
| 2 | [Chapman-Shaoxing/Ningbo ("large scale 12-lead ECG database for arrhythmia study")](https://physionet.org/content/ecg-arrhythmia/1.0.0/) | Open download, no account | CC-BY-4.0 (Zenodo copy confirmed; PhysioNet licence line not read) | ~45k records (memory) | Strong for AF and bundle branch blocks; AV block coverage should be checked. | Access today; contents from memory |
| 3 | [PhysioNet/CinC Challenge 2020 training data](https://physionet.org/content/challenge-2020/1.0.2/) | Open download | CC-BY-4.0 | ~43k records from several sources (memory) | Good. Includes the CPSC 2018 set, which has AF, I-AVB, LBBB and RBBB. Labels are in one SNOMED-CT scheme. | Today |
| 4 | [CODE-15%](https://zenodo.org/records/4916206) | Open download (Zenodo) | CC-BY-4.0 | 345,779 exams (confirmed) | Partial. Has AF, LBBB, RBBB and 1st-degree AV block. | Today; label quality from memory |

## Details
- **PTB-XL.** It is the cleanest start. Recordings are 10 s, and the diagnostic statements were assigned by cardiologists. It also comes with predefined train/test folds that people use as a benchmark. From memory, its labels follow the SCP-ECG standard.
- **Chapman-Shaoxing/Ningbo.** The PhysioNet page says "a licensed physician labeled the rhythm and other cardiac conditions", "another licensed physician performed a secondary validation", and "a senior physician intervened" on disagreements. It also says "Anyone can access the files, as long as they conform to the terms of the specified license", and that the hospital IRBs "allowed the data to be shared publicly after de-identification". That addresses your ethics concern for the source data, not for your own use of it. There is also a [2025 Zenodo copy](https://zenodo.org/records/16789324). Prefer the PhysioNet version, which is the original.
- **Challenge 2020 training data.** It bundles several databases with harmonised labels. It overlaps with some of the datasets above, so don't count its recordings twice. From memory, the 2021 challenge adds Chapman-Shaoxing/Ningbo to a similar bundle.
- **CODE-15%.** It is by far the largest. Recordings are 7–10 s, not strictly 10 s. From memory, its labels come from automatic analysis followed by review by trainees, not cardiologist confirmation of every exam. Use it for scale, and use PTB-XL or Chapman for label quality.

## Known, not confirmed
- **CODE-II-open.** The 2026 [CODE-II paper](https://www.nature.com/articles/s41746-026-02704-4) says it is a "public subset of 15,000 patients". It also describes a "CODE-II-test" of 8,475 exams reviewed by multiple cardiologists, for blinded evaluation. Every exam is annotated by a certified cardiologist with 66 classes. I could not find where it is hosted or what the access terms are. Check the paper's data availability section before you plan around it.
- **Georgia (Emory) data.** From memory, this is part of the Challenge training data. I did not check it separately.

## Not recommended, and why
- **CODE-test** ([Zenodo](https://zenodo.org/records/3765780)): it is open and cardiologist-reviewed, but it has only 827 exams, which is below your "few thousand".
- **Sami-Trop** ([Zenodo](https://zenodo.org/records/4905618)): from memory, about 1,600 Chagas-cohort ECGs. It is too small and lacks the diagnostic labels you need.
- **MIMIC-IV-ECG and the full original CODE dataset:** both need credentialing or an application, so they fail your constraint.
- **Long-term AF databases (Long Term AF, IRIDIA-AF, Icentia11k):** these are Holter or single-lead recordings, not 10-second 12-lead.

## What I could not find
- A recorded 12-lead set with large numbers of confirmed 2nd- and 3rd-degree AV block. Expect few of these in any open set, so count them before you design your classes.
- I did not exhaustively search regional databases beyond the registries, so the list may be incomplete.

## Next step
1. Download PTB-XL and Chapman-Shaoxing/Ningbo from the PhysioNet pages above, using `wget -r -N -c -np` on each dataset's files URL.
2. Tabulate the AF, LBBB, RBBB and each AV block label counts in both.
3. Check each dataset's licence and citation requirements before you publish. Both are open, but they require attribution.

I didn't write a shortlist page, so there is no `dataset-shortlist.html` this time.