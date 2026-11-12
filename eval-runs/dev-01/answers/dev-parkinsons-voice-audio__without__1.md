This list is from memory and I haven't checked the links or access terms today. Confirm each one before you build on it. Only datasets that ship real audio are included. The UCI/Oxford and Sakar sets are features only, so skip them.

| Dataset | Language / size | Access |
|---|---|---|
| **Italian Parkinson's Voice and Speech (IPVS)** | Italian, about 65 subjects (28 PD, 37 HC), several hundred recordings of vowels, phrases and sentences | Free on IEEE DataPort, which needs a free account. Some copies are mirrored on Kaggle, but check that the license and provenance match. |
| **MDVR-KCL** (King's College London / King Abdullah University Hospital) | English/Arabic-region cohort, about 37 subjects (16 PD, 21 HC), smartphone recordings of reading and spontaneous speech | Open on Zenodo. Search "Mobile Device Voice Recordings at King's College London". |
| **mPower** (Sage Bionetworks) | Thousands of smartphone "aaah" recordings, with PD and control labels self-reported through the app | Register on Synapse, complete the qualified-researcher process, and accept the data use terms. Labels are noisy, and you'll need to convert the m4a files. |
| **PC-GITA** | Colombian Spanish, 50 PD and 50 HC, vowels, words, sentences and monologue | Not openly downloadable. Email the GITA group at Universidad de Antioquia to request it under a license agreement. It's the most widely benchmarked set, so it's worth the effort. |
| **NeuroVoz** | Castilian Spanish, about 100+ PD and about 50+ HC, with several speech tasks | Distributed on Zenodo, as I recall under a request or restricted-access arrangement. Check the paper (LREC-COLING 2024) for the current process. |
| **Bridge2AI-Voice** | Multi-condition, including Parkinson's | On PhysioNet, which needs credentialed access and a signed DUA. The public releases have been derived features and spectrograms rather than raw audio, so check whether the current version includes waveforms. |

**Practical notes**
- **Size:** All of these are small, apart from mPower. Use subject-wise splits, not recording-wise, or you'll leak speakers across train and test.
- **Confounds:** Recording device, channel and session effects can separate PD from HC in these sets. Models can pick up the microphone instead of the disease. Cross-corpus evaluation, for example training on one set and testing on another, is the honest check.
- **Combining sets:** Mixing languages and tasks is common (domain adaptation work does it), but label consistently by task type.
- **Not PD:** TORGO and UA-Speech are dysarthria corpora (cerebral palsy/ALS), not Parkinson's. They're only useful for pretraining.

I can search to verify the current links and access terms for any of these, or look for more recent releases like Mendeley/Figshare uploads. Do you want me to?