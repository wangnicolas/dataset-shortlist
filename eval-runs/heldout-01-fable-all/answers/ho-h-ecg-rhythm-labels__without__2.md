Four datasets fit: all are open access, need no application or credentialing, and are released under CC BY 4.0. I checked the access terms and sizes on each landing page today; the label-count figures marked "from memory" are from the dataset papers and not re-checked.

| Dataset | Size | Format | Labels | Fit for AF / BBB / AV block |
|---|---|---|---|---|
| **[PTB-XL](https://physionet.org/content/ptb-xl/)** v1.0.3 | 21,799 records, 18,869 patients | 10 s, 500 Hz (and 100 Hz) | Annotated by up to two cardiologists | Best label quality. From memory: about 1,500 AF, 500 each complete LBBB and RBBB, 800 first-degree AV block, only a few dozen second- and third-degree. |
| **[Chapman-Shaoxing + Ningbo](https://physionet.org/content/ecg-arrhythmia/)** v1.0.0 | 45,152 patient ECGs | 10 s, 500 Hz | Physician-labelled, second physician validated, senior physician resolved disagreements | Strong for AF and other rhythms; includes LBBB and RBBB. I did not confirm the AV block labels. |
| **[PhysioNet/CinC Challenge 2021](https://physionet.org/content/challenge-2021/)** v1.0.3 | 88,253 public training records | Mostly 10 s, 500 Hz | Varies by source; some are machine labels overread by humans | Largest pool, with all labels mapped to SNOMED-CT codes. |
| **[CODE-15%](https://zenodo.org/records/4916206)** | 345,779 exams, 233,770 patients | 7–10 s, 400 Hz, zero-padded | Semi-automatic (from memory: cardiologist report text combined with automatic analysis) | Label set is almost exactly your targets: AF, RBBB, LBBB and first-degree AV block, plus sinus bradycardia and tachycardia. |

- **Start with PTB-XL.** It has the cleanest cardiologist labels and ships recommended patient-level folds (`strat_fold`), so you can have a baseline quickly.
- **Add Chapman-Shaoxing-Ningbo for volume.** It gives you more AF and bundle branch block cases from a different population and device, which also makes it useful as an external test set.
- **Use Challenge 2021 only if you want one harmonised download.** It already contains PTB-XL and Chapman-Ningbo, so don't count those twice. What it adds is CPSC 2018 (10,330 training records including CPSC-Extra) and Georgia (10,344). The organisers warn that some labels are wrong.
- **Use CODE-15% for scale or pretraining.** Its labels are noisier, so treat it as training data rather than a benchmark. From memory, the companion CODE test set on Zenodo (827 ECGs with cardiologist-consensus labels on the same six classes) is a good held-out benchmark.

Two limits apply whichever you choose:

- **High-grade AV block is rare everywhere.** First-degree is well covered, but second- and third-degree cases number in the tens per dataset. If you need them, plan to pool sources or scope the task to first-degree block.
- **Open access does not settle your own ethics position.** These are de-identified public datasets, which many institutions treat as exempt, but your institution may still want a formal determination before you publish.

I left out MIMIC-IV-ECG: its labels are machine-generated statements, and linking it to clinical data requires credentialing.