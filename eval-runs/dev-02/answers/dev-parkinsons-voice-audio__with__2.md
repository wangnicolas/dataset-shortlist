I found three PD-vs-control speech datasets with real audio that you can download today. A fourth, IPVS (Italian Parkinson's Voice and Speech), needs a free login. Two more are well known but gated. I did not build the interactive shortlist page, so everything is in this message.

I searched Zenodo, DataCite, OpenAIRE, PhysioNet, Hugging Face and the literature. I checked records and access flags on 2026-11-11, and the checks were partial. Figshare and IEEE sites blocked automated page reads, and the Zenodo search failed on one query. Treat the list as good but not exhaustive.

## What I assumed you need
- **R1 (must):** raw audio, not feature tables.
- **R2 (must):** PD and healthy-control labels.
- **R3 (nice):** several speakers and several tasks (vowels, reading, spontaneous speech), so you can split by speaker.
- **R4 (nice):** open or fast access, and a licence that allows research use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | **MDVR-KCL** (UK, phone-recorded) | Direct download from Zenodo | CC-BY-4.0 | 606 MB zip | Audio, PD and HC | Today |
| 2 | **VOC-PD** (Mandarin) | Direct download from Zenodo | CC-BY-4.0 | 1,551 .wav files (811 PD, 740 HC) | Audio, PD and HC, 5 tasks | Today (record only, files not opened) |
| 3 | **Arabic PD Speech Dataset** | Direct download from Zenodo | CC-BY-4.0 | 39 MB, 17 PD and 23 HC | Audio, PD and HC, 3 task types | Today (record only) |
| 4 | **Italian Parkinson's Voice and Speech (IPVS)** | Free IEEE DataPort login (my reading of the page, below) | Not stated on the page I could read | ~565 MB | Audio, PD and HC | Today (page), contents from memory |
| 5 | **Bridge2AI-Voice** | Registered access for features; raw audio needs institutional sign-off and a committee decision | Custom "Registered Access" licence | 48,226 recordings, 263 control participants | Mixed-condition cohort with a PD diagnosis table | Today |
| 6 | **PC-GITA** (Colombian Spanish) | Agreement with the owning group | Unknown | 50 PD and 50 HC | Audio, PD and HC | From memory |

## Details

**1. MDVR-KCL.** https://zenodo.org/records/2867216 (the DOI 10.5281/zenodo.2867215 also resolves).
- **What it is:** recordings made on a mobile phone at King's College London Hospital in September 2017. Zenodo's description says it covers early and advanced PD patients and healthy controls.
- **Access:** open on Zenodo, one zip file, no account needed.
- **Licence:** CC-BY-4.0, so attribution is the only requirement.
- **From memory (not confirmed today):** about 37 speakers, with reading and spontaneous tasks. The set is small, so split by speaker and be careful about overfitting.
- **Use in papers:** one 2021 arXiv comparison paper used it together with IPVS (https://doi.org/10.48550/arxiv.2111.10207).
- **Hugging Face copy:** the Hugging Face copy `saeedzou/kcl-parkinson-voice-dataset` is a re-upload. Use Zenodo.

**2. VOC-PD.** https://doi.org/10.5281/zenodo.21775027
- **What it is:** Mandarin audio in .wav format, in 5 task folders (numbers, phrases, sentences, vowels and one more).
- **Why it fits:** it is the largest clean-labelled open audio set I found, and the PD and HC counts are well balanced.
- **Caveats:** it is brand new (October 2026) and has no citations yet. The record doesn't give a speaker count, so check that recordings can be grouped by speaker before you split train and test.
- **Access and licence:** open on Zenodo under CC-BY-4.0.

**3. Arabic PD Speech Dataset.** https://zenodo.org/records/22036480
- **What it is:** 40 speakers. Tasks are sustained /a/, /i/ and /u/, a read passage and spontaneous speech.
- **Caveat:** the small speaker count makes it better for external validation than for training.
- **Access and licence:** open on Zenodo under CC-BY-4.0 (version 1.0.0, August 2026).

**4. IPVS.** https://www.ieee-dataport.org/open-access/italian-parkinsons-voice-and-speech (DOI 10.21227/aw6b-tg17)
- **Access:** the page says "LOGIN TO ACCESS DATASET FILES", and another passage mentions an IEEE DataPort subscription. I could not fully read the page, so confirm whether a free account is enough before planning around it.
- **Licence:** not stated on the page I could read. Check it on DataPort.
- **From memory:** about 65 speakers. The healthy controls include young adults as well as elderly ones, which creates an age confound you should control for.
- **Mirrors:** several Hugging Face copies exist (for example `birgermoell/Italian_Parkinsons_Voice_and_Speech`, ungated, with a 1.66k-row audio table). They are third-party re-uploads, and the CC-BY-4.0 tag was set by the uploader. For citations and licence certainty, use DataPort.
- **Use in papers:** a 2024 Journal of Voice paper on audio spectrogram transformers (https://doi.org/10.1016/j.jvoice.2024.11.008) is in the literature results, but I did not confirm which dataset it used.

**5. Bridge2AI-Voice.** https://physionet.org/content/b2ai-voice/4.0.0/
- **What it is:** a large, multi-condition voice collection with a Parkinson's diagnosis table (`parkinsons_disease.tsv`) and 263 controls.
- **Access, quoted from the page:** "Raw Audio Data Access for Bridge2AI Voice Adult Cohort is via Synapse" and "Accessing raw audio is a more involved process and requires institutional sign-off." Contact: DACO@b2ai-voice.org.
- **What I did not get:** the number of PD participants, and whether the PhysioNet release includes audio or only derived features.
- **Timeline:** plan on weeks, not days.

**6. PC-GITA.** From memory, not confirmed today.
- **What it is:** Colombian Spanish from the GITA group at Universidad de Antioquia, with about 50 PD and 50 HC speakers. A 2026 conference paper in the literature results uses it (https://doi.org/10.1109/icsadl67539.2026.11451863).
- **Access (my recollection):** a data-use agreement with the owning group. I couldn't open the IEEE page to confirm, so email the group.

## Known, not confirmed
- **Neurovoz** (Castilian Spanish PD corpus). I recall it as audio, with access by request to the authors (possibly via Zenodo). I did not verify this. Search "Neurovoz" and read the access statement.
- **Czech PD speech** (Rusz and colleagues). I recall access by request to the authors. Unverified, and "on request" is not an open dataset.
- **Figshare "Parkinson-Disease-voice-Dataset"** (https://doi.org/10.6084/m9.figshare.32588973.v2). It is open under CC-BY-4.0 and about 697 MB. But the description talks about "acoustic speech features", so it may be features only. The landing page was blocked, so open it and check whether it contains .wav files.
- **University of Rochester dataset** (https://doi.org/10.60593/ur.d.29410703.v2). The title says "Parkinson's Disease Screening", and it carries a CC-BY-4.0 licence. The page was blocked and the registry gave no access flag, so check the contents yourself.

## Not recommended
- **UCI Parkinson's voice sets** (Little et al. and the Sakar multi-type set). I recall these as precomputed measures, which is what you ruled out. This is from memory.
- **Mendeley "voice features from diadochokinesis test"** (https://doi.org/10.17632/zdp72s54cd.1). The title says features, and I didn't open it.
- **Figshare "Dataset for Parkinson Disease"** (https://doi.org/10.6084/m9.figshare.33212514.v1). "Biomedical voice measurements" sounds like a feature table, and I didn't open it.
- **"Synthetic Voice Dataset for Parkinson's…"** (https://doi.org/10.5281/zenodo.17753641). It is synthetic, and probably not audio.
- **PhysioNet PADS** (smartwatch motion data) and **Hugging Face `Parkinson_Speech` variants** (`BenchmarkDatasets`, `TabBioMed`). They don't fit: PADS is motion data, and the Hugging Face ones look like tabular copies of the UCI data.

## What I could not find
- A large, multi-site open corpus with hundreds of PD speakers and matched controls. The open sets are all small to medium (tens of speakers, or a few thousand clips).
- I did not search the Synapse portal directly (mPower, which I recall as app-collected voice with PD and control labels). From memory, it needs a free account plus an approved qualified-researcher application. Check it if you need scale.

## Next step
1. **Today:** download MDVR-KCL, VOC-PD and the Arabic set from Zenodo. They use three languages and three recording setups, which suits cross-corpus testing.
2. **This week:** create an IEEE DataPort account for IPVS, and email the PC-GITA and Neurovoz groups.
3. **For the model:** split by speaker, not by clip, because every dataset here has multiple clips per person. Train on one corpus and test on another to see whether your detector learns PD or just the recording setup.

If you want the interactive shortlist page, I can build it.