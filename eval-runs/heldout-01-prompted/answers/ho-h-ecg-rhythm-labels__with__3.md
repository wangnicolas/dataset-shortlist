Three datasets fit: PTB-XL, the Chapman-Shaoxing/Ningbo database, and PhysioNet Challenge 2021. All three are on PhysioNet under CC BY 4.0, open access, with no application or credentialing. I confirmed this from each project page.

## Recommended

**1. PTB-XL** ([physionet.org/content/ptb-xl/1.0.3](https://physionet.org/content/ptb-xl/1.0.3/))
- It has 21,799 ECGs from 18,869 patients, each 10 seconds and 12-lead, at 500 Hz with a 100 Hz copy.
- Up to two cardiologists annotated each record, and a large share was checked by a second cardiologist. This is the best match for your "cardiologist-assigned" requirement.
- It uses 71 SCP-ECG statements, and a record can have several labels. The conduction-disturbance superclass (CD) has 4,898 records.
- I did not confirm per-statement counts for AF, LBBB, RBBB or AV block on the page. From memory, 2nd- and 3rd-degree AV block are very rare in this set. Check `scp_statements.csv` and `ptbxl_database.csv` before you commit.
- Download options: ZIP (about 1.7 GB), `wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/`, or `aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ .`

**2. Chapman-Shaoxing/Ningbo ("ecg-arrhythmia")** ([physionet.org/content/ecg-arrhythmia/1.0.0](https://physionet.org/content/ecg-arrhythmia/1.0.0/), paper: [Zheng et al. 2020](https://www.nature.com/articles/s41597-020-0386-x))
- It has 45,152 ECGs, each about 10 seconds and 12-lead, at 500 Hz, in WFDB format (about 2.3 GB zipped).
- A licensed physician labeled each record, a second physician validated it, and a senior physician resolved disagreements.
- About 3,889 subjects have AFIB, according to the search summary.
- The page names RBBB and LBBB as labels. I could not confirm the full label list, and AV block coverage looks weak. A 2026 [arXiv paper](https://arxiv.org/pdf/2602.17531) reports that in the CSN set some labels have no positives, including 2AVB2, LBBB and LBBBB. It also reports fewer than three positives for 3AVB. Treat that as a second-hand claim and check the headers yourself.
- Download options: `wget -r -N -c -np https://physionet.org/files/ecg-arrhythmia/1.0.0/`, the `physionet download` package, or `aws s3 sync --no-sign-request s3://physionet-open/ecg-arrhythmia/1.0.0/ .`

**3. PhysioNet/CinC Challenge 2021 training data** ([physionet.org/content/challenge-2021/1.0.3](https://physionet.org/content/challenge-2021/1.0.3/))
- It holds about 88,000 public training ECGs pooled from several databases. Those include CPSC 2018, PTB-XL, Georgia, Chapman-Shaoxing/Ningbo and others. It is 12.6 GB uncompressed.
- Labels are SNOMED-CT codes. The page cites AF (164889003) and first-degree AV block (270492004). I did not confirm the bundle branch block codes. They are in the scored-class CSV on the challenge GitHub.
- Label quality is mixed. Some sources use human-overread machine labels, and the page warns that some labels are likely wrong.
- It is the largest pool, and it probably has the most AV block examples. Be careful with it. PTB-XL and Chapman are already inside it, so training on this and evaluating on those would leak data.

## Worth knowing: CPSC 2018

The [CPSC 2018 training set](http://2018.icbeb.org/Challenge.html) has 6,877 12-lead records. By the search summary, its classes are AF (1,098), I-AVB (704), LBBB (207) and RBBB (1,695). That covers your targets directly. However, records run 6–60 seconds, not 10, and the training data comes as several separate downloads. I did not check its license or access terms. A copy of it is already in Challenge 2021.

## Suggested plan

- **Start with PTB-XL.** It has the clearest cardiologist provenance and a standard train/validation/test split.
- **Add Chapman-Shaoxing for AF and bundle branch block volume.** Use a different dataset as your external test set, so the evaluation is honest.
- **Use Challenge 2021 if AV block counts are too low.** If you do, split by source database to avoid the leakage above.
- **Count labels before you design the study.** Second- and third-degree AV block are likely too rare in all of these for a reliable classifier. First-degree AV block is probably workable.

I did not download any files. I only read the project pages and search summaries, so the label counts need checking against the actual headers.

Sources:
- [PTB-XL on PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/)
- [Chapman-Shaoxing/Ningbo on PhysioNet](https://physionet.org/content/ecg-arrhythmia/1.0.0/)
- [Zheng et al., Scientific Data 2020](https://www.nature.com/articles/s41597-020-0386-x)
- [PhysioNet Challenge 2021](https://physionet.org/content/challenge-2021/1.0.3/)
- [CPSC 2018](http://2018.icbeb.org/Challenge.html)
- [Position: Evaluation of ECG Representations Must Be Fixed (arXiv)](https://arxiv.org/pdf/2602.17531)