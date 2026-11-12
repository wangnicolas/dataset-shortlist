I haven't checked any of these links or access terms live, so confirm them on each landing page. Everything below is from memory.

## Open download (audio included)

| Dataset | Contents | Access |
|---|---|---|
| **Italian Parkinson's Voice and Speech** (Dimauro & Girardi, Bari) | About 65 speakers (roughly 28 PD and 37 HC). It has sustained vowels, words and phrases, in about 830 recordings. | Hosted on IEEE DataPort. Make a free account and download. It's CC-BY, and there are Kaggle mirrors. |
| **MDVR-KCL** (King's College London mobile voice recordings) | About 37 speakers (16 PD and 21 HC). It has smartphone recordings of reading and spontaneous speech. | Zenodo, open, CC-BY. Search for "MDVR-KCL". |

## Registration or a request required

| Dataset | Contents | Access |
|---|---|---|
| **mPower** (Sage Bionetworks) | Thousands of smartphone participants, each doing a 10-second "aaah". PD status is self-reported. It's the largest set by far. | On Synapse. Make an account, complete the qualified-researcher/data-use steps, and accept the conditions. Approval can take a while. |
| **PC-GITA** (Universidad de Antioquia, Colombian Spanish) | 50 PD and 50 HC, age- and sex-balanced. It has vowels, DDK tasks, sentences and a monologue. | Not a public download. Email the GITA group and sign a license, usually academic-only. |
| **Neurovoz** (Castilian Spanish) | About 100+ speakers (PD and HC), with several speech tasks. | Distributed on request, with a data agreement. Check the Zenodo and paper listing for the current process. |
| **Bridge2AI-Voice** (NIH) | Multi-disorder voice and speech data that includes Parkinson's. | On PhysioNet, with credentialed access (CITI training and a data use agreement). Check whether the release you want includes raw audio or only derived features, since parts are restricted. |

## Features only (skip these)

- **UCI Parkinson's (Little et al., 195 phonations)** is features only.
- **UCI Parkinson Speech Dataset with Multiple Types of Sound Recordings** (Sakar) is mostly features. Check the page in case raw files have been added.

## Cautions for deep learning

- **Size:** Most open sets have only 30–100 speakers. Split by speaker, never by recording, or you'll get leakage and inflated accuracy. Cross-validate by speaker.
- **Recording confounds:** In some sets, PD and HC were recorded with different devices, rooms or sessions, so a model can learn the channel instead of the disease. Test cross-corpus (train on one dataset, test on another) to check for this.
- **Language and task mismatch:** The sets differ in language (Italian, Spanish, English) and task (vowels, read speech, free speech). Pooling them takes care.
- **Age and sex:** Match these between PD and HC, or at least report them.
- **Pretrained models:** With so little data, fine-tuning something like wav2vec 2.0, HuBERT or Whisper embeddings usually beats training from scratch.

I can fetch the current landing pages, confirm the licenses and file formats, or write download scripts for the open ones. Which would help most?