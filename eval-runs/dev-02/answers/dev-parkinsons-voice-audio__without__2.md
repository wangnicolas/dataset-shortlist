I'm working from memory and haven't checked the current pages, so confirm access terms and sizes at the source before you build on any of this.

## Openly downloadable

| Dataset | Contents | Access |
|---|---|---|
| **MDVR-KCL** (King's College London, Jaeger et al. 2019) | About 37 speakers (about 21 PD, 16 HC). Smartphone recordings of reading and spontaneous speech. | Zenodo, open download, CC-BY. Search "Mobile Device Voice Recordings at King's College London". |
| **Italian Parkinson's Voice and Speech** (Dimauro & Girardi) | About 65 speakers (28 PD, 37 HC). Sustained vowels, words, and sentences as WAV. | IEEE DataPort. You need a free account, and I believe it's open access. |
| **Neurovoz** (Castilian Spanish, Mendes-Laureano et al., 2024) | About 100 speakers, PD and HC. Vowels, DDK, sentences, and free speech. | I believe it's on Zenodo, possibly with a request step. Check the paper's data-availability statement. |

## Registration and approval required

- **mPower** (Sage Bionetworks, Synapse): This is the largest set by far, with thousands of participants. The recordings are 10-second "aaah" phonations from smartphones, in m4a.
  - **Access:** Create a Synapse account, complete the Certified User process, and submit a data access request with a statement of intended use.
  - **Caveat:** Many diagnosis labels are self-reported, and the audio quality varies a lot.

## Available only by request to the authors

- **PC-GITA** (Colombian Spanish, Orozco-Arroyave et al.): 50 PD and 50 HC, with a rich task set. It's the most-used benchmark in the literature. Contact the GITA group at Universidad de Antioquia, who usually require a data-use agreement.
- **Czech and German PD corpora** (Rusz, Prague, and Erlangen groups): These are also by request. Email the corresponding authors of the papers.

## Datasets to avoid

These come up in searches but don't contain audio:
- **UCI Oxford Parkinson's (Little)**, **UCI Parkinson's Telemonitoring**, and most **Kaggle "Parkinson's voice" sets** are precomputed features only.
- **UCI Sakar multiple-sound-types set** is mostly features, so check whether the raw WAVs are included before relying on it.
- **Bridge2AI-Voice** (PhysioNet) includes PD, but as far as I know the public release has derived features rather than raw audio. Check the current release notes.

## Caveats for deep learning

- **Size:** The open sets are small, with dozens of speakers each. Split by speaker, never by clip, or you'll get inflated accuracy from speaker leakage.
- **Recording confounds:** If PD and HC were recorded with different devices or rooms, a model can learn the channel instead of the disease. Check this per dataset, especially for mPower and MDVR-KCL.
- **Pooling:** Combining datasets helps generalization, but language and task differ across them. Hold out a whole dataset as a test set if you can.
- **Labels:** Check how each dataset defines and verifies diagnosis. Also check medication state (on or off) and severity scores (UPDRS, H&Y) where they're provided.

I can also search to verify the current links and licenses, or write download and loader scripts for the open ones.