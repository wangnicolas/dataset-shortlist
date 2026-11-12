You can do this with fully open data: several large 12-lead sets are downloadable today with no application or credentialing, all under CC BY 4.0 as far as I recall. This is from memory, not re-checked against the live pages today, so treat the counts as approximate and confirm the licence on each landing page.

| Dataset | Where | Size | Labels | Fit for your targets |
|---|---|---|---|---|
| **PTB-XL** | PhysioNet, open access | ~21,800 ECGs, ~18,900 patients, 10 s, 500 Hz | Annotated by up to two cardiologists; a `validated_by_human` flag marks the roughly three-quarters that were human-validated | ~1,500 AF, ~540 each complete LBBB and RBBB, ~1,100 incomplete RBBB, ~800 first-degree AV block, plus fascicular blocks |
| **PhysioNet/CinC Challenge 2021 training set** | PhysioNet, open access | ~88,000 ECGs from several sites | Harmonised SNOMED CT codes; label provenance varies by site | AF, LBBB, RBBB and first-degree AV block were all scored classes |
| **CODE-15%** | Zenodo, open | ~345,000 ECGs, ~233,000 patients, 7–10 s, 400 Hz | Six labels: AF, RBBB, LBBB, first-degree AV block, sinus bradycardia, sinus tachycardia | Labels match your targets, but they combine the cardiologist's report with automated analysis and are only partly hand-reviewed |
| **CODE test set** | Zenodo, open | 827 ECGs | Consensus of two to three cardiologists | Same six labels; too small to train on, but a good gold-standard external test |
| **Chapman-Shaoxing / Ningbo** | PhysioNet or figshare, open | ~45,000 patients, 10 s, 500 Hz | Physician-labelled rhythm and conduction labels | Strong on rhythm; already included in Challenge 2021 |
| **CPSC 2018** | Challenge site, open | ~6,900 ECGs, 6–60 s | Nine classes | Includes AF, first-degree AV block, LBBB and RBBB; also inside Challenge 2021 |

My recommendation:

1. **Start with PTB-XL.** It has the best-documented cardiologist labels and ships with patient-wise stratified folds, so you can have a baseline running in a day.
2. **Add the Challenge 2021 set for scale and cross-site validation.** Train on some sites and test on others, such as the Georgia subset (~10,000 ECGs from the US).
3. **Use CODE-15% if you need more volume, and the CODE test set as an external benchmark.** CODE-15% is a large multi-part download.

Things to watch for:

- **Overlap:** PTB-XL, Chapman-Shaoxing, Ningbo and CPSC are all inside Challenge 2021, so don't count them twice or let them leak across your train/test split.
- **Higher-grade AV block is rare everywhere:** PTB-XL has only a dozen or so each of second- and third-degree block, and CODE-15% labels first-degree only. A few thousand examples is realistic for AF, bundle branch blocks and first-degree block, but not for higher-grade block.
- **Label conventions differ:** some sources merge AF with flutter, and they split complete, incomplete and unspecified bundle branch block differently. You will need an explicit label mapping.
- **Not everything is 10 s:** CPSC records run 6–60 s, and the Challenge set includes a small 30-minute subset (INCART) that you should drop.

Sets that don't fit your constraints:

- **MIMIC-IV-ECG:** the waveforms are open, but the labels are machine-generated statements, and the cardiologist reports need credentialed MIMIC access.
- **Full CODE, UK Biobank, Harvard-Emory:** all require an application or a data use agreement.

Even for public de-identified data, many institutions want a quick "not human subjects research" determination from the ethics board. This is usually a short form, not a full review, and worth filing in parallel so it doesn't block publication later.