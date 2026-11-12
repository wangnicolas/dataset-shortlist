## What I assumed you need

- **R1 (must):** Parkinson's patients and healthy controls, with a diagnosis label.
- **R2 (must):** Real audio files, not feature tables.
- **R3 (nice):** Several speech tasks (vowels, reading, spontaneous speech) and enough speakers to train a deep model.
- **R4 (must):** Data you can obtain, with a licence that allows research use. I assumed non-commercial research. Say if that's wrong, because it affects NeuroVoz.

I checked on 2026-11-11 and 2026-11-12. I searched Hugging Face, OpenAIRE, PhysioNet and Zenodo. The Zenodo and DataCite APIs failed intermittently, so the sweep may have gaps.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit |
|---|---|---|---|---|---|
| 1 | MDVR-KCL (UK English, phone recordings) | Direct download, minutes | CC BY 4.0 | 606 MB | Strong |
| 2 | VOC-PD (Mandarin) | Direct download, minutes | CC BY 4.0 | 367 MB, 1,551 files (811 PD, 740 HC) | Strong |
| 3 | Italian Parkinson's Voice and Speech | Free IEEE account, minutes | CC BY 4.0 | 565 MB | Strong |
| 4 | NeuroVoz (Castilian Spanish) | Request on Zenodo, timing unknown | CC BY-NC-ND 4.0 | 692 GB | Strong |
| 5 | Arabic PD Speech Dataset | Direct download, minutes | CC BY 4.0 | 39 MB, 17 PD / 23 HC | Partial |
| 6 | ParkMultiNet speech and MRI sets | Direct download, minutes | CC BY 4.0 | 1.3 GB | Partial |

## Details

**1. MDVR-KCL** ([Zenodo](https://doi.org/10.5281/zenodo.2867215))
- It has uncompressed WAV at 44.1 kHz, with PD patients and healthy controls rated on H&Y and UPDRS.
- Tasks are reading and spontaneous dialogue, though not every participant has the same tasks.
- The page doesn't state group sizes, so check the paper.
- Access: download the zip.
- Used in [Comparative Study of Speech Analysis Methods to Predict PD](https://doi.org/10.48550/arxiv.2111.10207), alongside the Italian set.

**2. VOC-PD** ([Zenodo](https://doi.org/10.5281/zenodo.21775027))
- It has WAV files in five task folders: numbers, phrases, sentences, vowels and others.
- It's from 2026 and has no citations yet, so nobody else has validated it.
- The counts are recordings, not speakers. Split by speaker to avoid leakage.
- Access: download the zip.

**3. Italian Parkinson's Voice and Speech** ([IEEE DataPort](https://ieee-dataport.org/open-access/italian-parkinsons-voice-and-speech))
- It has WAV files with XLSX metadata. The creators are Dimauro and Girardi (2019).
- The page I read doesn't give subject counts or tasks. They're in the paper.
- Access: create a free IEEE account and download. The page also mentions a "DataPort Subscription". I read that as free for open-access sets, but I didn't test the download.
- A [Hugging Face copy](https://huggingface.co/datasets/birgermoell/Italian_Parkinsons_Voice_and_Speech) (1,662 rows, CC BY 4.0) is easier to load. It's an uploader's re-upload, so cite the original.

**4. NeuroVoz** ([Zenodo](https://zenodo.org/records/13647600))
- It has 54 PD patients (on medication) and 58 controls, with 2,977 audio files. Tasks are vowels, diadochokinetic (DDK) tests, 16 repeated sentences and monologues.
- It's the richest set here, and the best fit for deep learning.
- Access: log in to Zenodo, request access, and accept the data usage agreement. I found no stated turnaround.
- The licence is non-commercial and no-derivatives. Ask the owners whether training models and augmentation count as derivatives.
- It's large: 692 GB for the current version.

**5. Arabic PD Speech** ([Zenodo](https://doi.org/10.5281/zenodo.22036480))
- It has MP3 files at 44.1 kHz: vowels, a reading passage and spontaneous speech.
- With 40 speakers it's good as a pilot or external test set, not for training on its own.
- The page has no consent or ethics statement.

**6. ParkMultiNet sets** ([Zenodo](https://doi.org/10.5281/zenodo.22082939))
- It has 502 speech clips (266 PD, 236 non-PD) plus a clinical cohort.
- Part of the speech is recycled from other public datasets, so there's a leakage risk if you combine them.
- I didn't open the archive, so the clip format and tasks are unconfirmed.

**Two more that need an application.** I found these through web search only, not a registry record or the landing page.
- **PC-GITA** (Colombian Spanish, 50 PD / 50 HC; vowels, DDK, words, sentences, a reading text and a monologue). Email Juan Rafael Orozco-Arroyave at Universidad de Antioquia (rafael.orozco@udea.edu.co) and sign the user agreement. It's the most-cited benchmark, so it's good for comparing results. Source: [LREC 2014 paper](http://www.lrec-conf.org/proceedings/lrec2014/pdf/7_Paper.pdf).
- **mPower** (Synapse syn4993293, phone vowel /a/ recordings in m4a; only participants who chose broad sharing). Get a Synapse account, have your profile validated, pass the certified-user quiz, and submit an Intended Data Use statement. The data is large and noisy, and the control labels are self-reported.

## Not recommended, and why

- **Neurovoz Rasta-PLP sets** ([Zenodo 3401684](https://doi.org/10.5281/zenodo.3401684)): features only.
- **Parkinson_Speech sets on Hugging Face**: I treated them as tabular copies of the UCI feature data. I didn't confirm that.
- **Synthetic-voice Zenodo sets** ([17753641](https://doi.org/10.5281/zenodo.17753641)): synthetic, not real recordings.
- **PhysioNet PD sets** (smartwatch, gait, tremor, keystrokes): no speech.
- **Rochester screening set**: about 630 KB of metadata, no audio.

## What I could not find

- I didn't verify PC-GITA or mPower against a registry record.
- **EWA-DB** (Slovak, 1,649 speakers including PD and controls) is flagged application-only. I didn't read its access page.
- A single large, open, multi-site English dataset didn't turn up. The open sets are small or single-language.

## Next step

Start with MDVR-KCL, VOC-PD and the Italian set today. Send the NeuroVoz and PC-GITA requests now, since they take the longest.

Whatever you combine, split train and test by speaker, and hold out an entire dataset as a test set. Models trained on small corpora tend to learn recording conditions rather than disease.

Interactive page: `dataset-shortlist.html` (in `/private/tmp/e-JqEZNe/home/cwd`).