I'm working from memory and haven't checked any of these links today, so confirm access terms on each landing page. These are the ones I know of that include raw audio.

**Open download**

| Dataset | Contents | Access |
|---|---|---|
| **MDVR-KCL** (Mobile Device Voice Recordings at King's College London) | About 16 PD and 21 healthy controls. Smartphone WAVs of reading and spontaneous speech. | Zenodo (record ~2867216), open access, no approval needed. |
| **Italian Parkinson's Voice and Speech** (Dimauro & Girardi) | About 65 speakers (28 PD, rest healthy controls). Vowels, words, and phrases. | IEEE DataPort (DOI ~10.21227/aw6b-tg17). Free account required, and I believe it's open access. |

**Registration or application required**

| Dataset | Contents | Access |
|---|---|---|
| **mPower** (Sage Bionetworks) | Thousands of participants. 10-second smartphone "aaah" recordings. | Synapse. Register, complete the qualified-researcher steps, and accept the data use terms. The "controls" are self-reported, so labels are noisy. |
| **PC-GITA** (Colombian Spanish, GITA group, Univ. of Antioquia) | 50 PD and 50 age/sex-matched controls. Vowels, DDK, words, sentences, and monologue. | Request from the authors under a license agreement. It's widely used, so it's good for benchmarking. |
| **Neurovoz** (Castilian Spanish) | About 47 PD and 32 controls. Sentences, DDK, and monologues. | Request through the authors' Zenodo/paper page. I'm not sure of the current terms. |
| **Bridge2AI-Voice** (PhysioNet) | Multi-disorder voice data that includes PD. | Credentialed PhysioNet access with a data use agreement. As far as I know, the public releases contain derived features such as spectrograms and MFCCs rather than raw audio, so check whether that fits your needs. |

**Features only, so not what you need:** the Oxford Parkinson's Detection dataset (Little) and the UCI Parkinson Speech datasets (Sakar). They show up in most searches, but they're CSV tables.

**Caveats for deep learning**
- **Small speaker counts.** Most sets have tens of speakers. Split by speaker, never by recording, or you'll get leakage and inflated accuracy.
- **Recording-condition confounds.** If PD and control audio differ in device or room (as can happen in mPower), a model can learn the channel instead of the disease. Check this early.
- **Pooling for scale.** Combining corpora is common, but language and task differ across them. Hold out a whole corpus as a test set to see whether your model generalizes.

I can search the web to confirm current links and access terms, or look for more datasets such as Czech, German, or Mandarin corpora. Want me to do either?