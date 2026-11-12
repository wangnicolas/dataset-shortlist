Here's what I know from memory. I haven't checked any of these links live, so confirm current access terms on each landing page.

## Open or easy to get

| Dataset | Contents | Access |
|---|---|---|
| **Italian Parkinson's Voice and Speech** (Dimauro & Girardi) | About 65 subjects: 28 PD, 15 elderly controls, 22 young controls. Sustained vowels, words and sentences as WAV files. | Free on IEEE DataPort. You need an account, and open access is available. It's also mirrored on Kaggle. |
| **MDVR-KCL** (King's College London) | 16 PD and 21 controls (the PD group includes people with REM sleep behavior disorder). Smartphone recordings of reading and spontaneous speech. | Open on Zenodo, CC BY 4.0. Search for "Mobile Device Voice Recordings at King's College London." |

## Free, but you must apply

| Dataset | Contents | Access |
|---|---|---|
| **mPower** (Sage Bionetworks) | Thousands of smartphone recordings of a 10-second "aaah", with self-reported PD and control labels. It's by far the largest, but the recordings are noisy and the labels are self-reported. | Synapse account, a short certification quiz, then a data use application. |
| **Neurovoz** (Spanish, Castilian) | About 50 PD and 50 controls, with vowels, DDK tasks and sentences. | Hosted on Zenodo with restricted access. You request it with a data use agreement. |
| **PC-GITA** (Colombian Spanish, GITA Lab, Universidad de Antioquia) | 50 PD and 50 age/sex-matched controls, with vowels, DDK, words, sentences and a monologue. It's the most widely cited benchmark. | Email the GITA group and sign a license agreement, usually for academic use. |

## Possible, but check first
- **Bridge2AI-Voice** (PhysioNet) includes a PD category. As I recall, the public release has features and spectrograms rather than raw audio because of privacy, so check whether it fits your need.
- **Czech and German PD speech corpora** (for example, from Rusz's group in Prague) exist in the literature. They're generally available only through collaboration.

## Common traps
- The **UCI Parkinson's datasets** (Little, Sakar, telemonitoring) have precomputed features only, so they don't meet your requirement. Most Kaggle "Parkinson's voice" datasets are copies of these.
- Most of these are small, with fewer than 100 subjects. For deep learning, split by speaker, never by recording. Otherwise the same speaker lands in both train and test, and your accuracy will be inflated.
- Recording conditions, language and device differ between datasets. A model can learn to identify the dataset or microphone instead of the disease, so avoid training on PD from one source and controls from another.
- Pretrained audio encoders (wav2vec 2.0, HuBERT, Whisper) fine-tuned or used as feature extractors tend to work better than training from scratch at this scale.

I can search the web to confirm the current links and access requirements for any of these. I can also help set up a speaker-independent split once you've picked a dataset.