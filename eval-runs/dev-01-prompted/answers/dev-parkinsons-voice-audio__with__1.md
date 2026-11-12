I searched the web and opened the pages I could. Items marked *not verified* are ones where I couldn't read the page myself.

## Raw-audio datasets with Parkinson's and healthy controls

| Dataset | Language and task | Size | Access |
|---|---|---|---|
| **[MDVR-KCL](https://zenodo.org/records/2867216)** (Zenodo) | Smartphone recordings of early and advanced PD plus healthy controls | One 606 MB zip, WAV, 44.1 kHz, 16-bit | **Open**, CC BY 4.0, direct download with no login. The page doesn't give the PD/HC split, so check the paper. |
| **[Italian Parkinson's Voice and Speech](https://ieee-dataport.org/open-access/italian-parkinsons-voice-and-speech)** (IEEE DataPort) | Italian: sustained vowels and read phrases | About 565 MB zip of WAVs plus Excel metadata. Per search results, 831 files from 65 speakers (28 PD, 37 HC), 16 kHz. | CC BY 4.0. You need a **free IEEE account**. The page contradicts itself about whether a paid subscription is required, so check when you log in. |
| **[NeuroVoz](https://zenodo.org/records/13647600)** (Zenodo; [paper](https://arxiv.org/html/2403.02371)) | Castilian Spanish: vowels, 16 listen-and-repeat sentences, /pa-ta-ka/ and a free monologue | About 1 GB and about 2,977 WAV files, 44.1 kHz. 54 PD and 58 HC per the paper. | **Restricted.** You request access on Zenodo and paste the Data Usage Agreement text into the message box. |
| **[mPower](https://www.synapse.org/Synapse:syn4993293)** (Sage Bionetworks, Synapse) | Smartphone sustained /a/ recordings in m4a | Large, about 80 GB in one study. Tens of thousands of recordings. | Free Synapse account plus the data-use terms and a qualification step. Convert m4a to WAV yourself. *Not verified: I didn't open the Synapse page.* The controls are self-reported, so labels are noisier. |
| **PC-GITA** (Colombian Spanish) | Read speech, spontaneous speech and sustained vowels. 50 PD and 50 HC, 44.1 kHz. | — | **On request only.** Email Juan Rafael Orozco-Arroyave at Universidad de Antioquia (rafael.orozco@udea.edu.co). I found no public form or download link. |
| **[Figshare voice samples](https://figshare.com/articles/dataset/Voice_Samples_for_Patients_with_Parkinson_s_Disease_and_Healthy_Controls/23849127)** | Sustained /a/ recorded over the phone | Tiny, about 4 MB (`PD_AH.zip`, `HC_AH.zip`) | Described as direct download. *Not verified: the page returned 403 to me.* Sources disagree on the count (50 + 50 described, 81 recordings in one study). |

## Datasets that look relevant but aren't
- **[UCI "Parkinson's Speech with Multiple Types of Sound Recordings"](https://archive.ics.uci.edu/dataset/301/parkinson+speech+dataset+with+multiple+types+of+Audio+recordings):** The search summary implied audio, but the page says it holds 26 extracted features per sample. The download is a 92 KB archive, so it has no audio.
- **Oxford Parkinson's dataset:** Features only.
- **[Mendeley DDK dataset](https://data.mendeley.com/datasets/zdp72s54cd/1):** The description says acoustic features extracted after adding noise, so it probably has no raw WAVs. I didn't confirm the file list.
- **Older NeuroVoz Zenodo record ([3557758](https://zenodo.org/records/3557758)):** Rasta-PLP features only.

## Suggestions for deep learning
- **Sample size:** All of these are small, at about 30 to 110 speakers each. Split train and test **by speaker**, not by file, or your accuracy will be inflated. Leave-one-dataset-out testing is better still.
- **Where to start:** MDVR-KCL and the Italian set are the easiest to get today. Request NeuroVoz and PC-GITA early, since approval can take days or weeks.
- **Pooling:** Combining datasets gives you more data. But the language, microphone and task differ between them, and the model can learn to identify the dataset instead of the disease. Check for that.
- **Versions:** The NeuroVoz versions differ. The paper and Zenodo record say 112 speakers, while the GitHub README says 108 speakers and 2,903 files. Use the latest Zenodo record and cite the Scientific Data paper (Mendes-Laureano et al., 2024).

I can write download scripts for the open ones or draft the access-request emails. A broader catalog is at [talhanai/speech-nlp-datasets](https://github.com/talhanai/speech-nlp-datasets).

Sources:
- [Zenodo MDVR-KCL](https://zenodo.org/records/2867216)
- [IEEE DataPort Italian PVS](https://ieee-dataport.org/open-access/italian-parkinsons-voice-and-speech)
- [NeuroVoz Zenodo](https://zenodo.org/records/13647600)
- [NeuroVoz paper (arXiv)](https://arxiv.org/html/2403.02371)
- [UCI 301](https://archive.ics.uci.edu/dataset/301/parkinson+speech+dataset+with+multiple+types+of+Audio+recordings)
- [Figshare](https://figshare.com/articles/dataset/Voice_Samples_for_Patients_with_Parkinson_s_Disease_and_Healthy_Controls/23849127)
- [Mendeley DDK](https://data.mendeley.com/datasets/zdp72s54cd/1)
- [mPower on Synapse](https://www.synapse.org/Synapse:syn4993293)
- [talhanai/speech-nlp-datasets](https://github.com/talhanai/speech-nlp-datasets)