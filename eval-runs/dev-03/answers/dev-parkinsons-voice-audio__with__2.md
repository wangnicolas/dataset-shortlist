## What I assumed you need
- **R1 (must):** real audio files, not feature tables.
- **R2 (must):** labelled PD and healthy-control speakers.
- **R3 (nice):** a licence that allows model training.
- **R4 (nice):** enough speakers for deep learning, ideally 100 or more.
- I assumed you can wait weeks for an application if the data is worth it, and that the language doesn't matter.

I checked on 2026-11-12. "Confirmed" means a registry record or page I read this session. "Memory" or "web search" means not confirmed on the source itself.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | MDVR-KCL (smartphone, English) | Open download | CC BY 4.0 | About 37 speakers (memory) | Strong, small | Confirmed |
| 2 | VOC-PD (Mandarin) | Open download | CC BY 4.0 | 1,551 WAV files, 811 PD and 740 HC | Strong | Registry record confirmed; page not fully read |
| 3 | Arabic PD Speech | Open download | CC BY 4.0 | 17 PD, 23 HC (MP3) | Strong, small | Confirmed |
| 4 | Italian Parkinson's Voice and Speech | Hugging Face mirror open; original needs a free IEEE account (memory) | CC BY 4.0 on the mirror | 28 PD, 37 HC | Strong | Mirror confirmed; original from web search |
| 5 | NeuroVoz (Castilian Spanish) | Request access on Zenodo, about weeks | CC BY-NC-ND 4.0 | 54 PD, 58 HC | Strong, the best size | Confirmed |
| 6 | PC-GITA (Colombian Spanish) | Email request and signed agreement | Agreement terms | 50 PD, 50 HC | Strong | Web search only |
| 7 | mPower (smartphone voice) | Synapse qualified-researcher access | Synapse terms | Thousands of participants | Partial | Web search only |
| 8 | Bridge2AI-Voice | PhysioNet credentialing, plus committee sign-off for raw audio | Bridge2AI Registered Access Licence | 253 participants in one PD analysis | Partial | Confirmed |
| 9 | HeyJay! (ICPSR 39448) | Restricted data use agreement, about 3 weeks | Not confirmed | Not confirmed | Weak | Web search only |

## Details

**1. MDVR-KCL** ([record](https://zenodo.org/records/2867216))
- It holds 44.1 kHz, 16-bit WAV files from early and advanced PD patients and healthy controls.
- File names encode the label and clinical scores (for example `ID02_pd_1_2_1.wav`).
- Access: open the record and download. No account is needed.

**2. VOC-PD** ([DOI](https://doi.org/10.5281/zenodo.21775027))
- It has 1,551 WAV recordings (numbers, phrases, sentences, vowels), about 367 MB in 4 zip files.
- The Zenodo page timed out when I read it, so the counts come from the registry description.
- Check whether the recordings carry speaker IDs, so you can split train and test by speaker.

**3. Arabic PD Speech** ([record](https://zenodo.org/records/22036480))
- It has vowels, a read passage and spontaneous speech, as 44.1 kHz MP3 (lossy), about 39 MB.
- Download directly. The page states CC BY 4.0.

**4. Italian Parkinson's Voice and Speech**
- The original is by Dimauro and Girardi on IEEE DataPort, DOI 10.21227/aw6b-tg17 ([search result](https://commons.datacite.org/doi.org/10.21227/kv93-ak67)).
- It has 28 PD patients, 15 young healthy controls and 22 elderly healthy controls. Many papers use only the 22 elderly controls to avoid an age confound.
- A copy sits on [Hugging Face](https://huggingface.co/datasets/birgermoell/Italian_Parkinsons_Voice_and_Speech) (1,662 clips, CC BY 4.0). Its card doesn't show the PD/HC labels, so check them before training.
- Cite the original authors, not the mirror.

**5. NeuroVoz** ([record](https://zenodo.org/records/13647600))
- It has 112 participants, with PD patients recorded on medication.
- Access: log in to Zenodo, request access, and accept the Data Agreement Usage. The authors approve requests.
- The page shows **CC BY-NC-ND 4.0**. The no-derivatives clause may matter for model training, so read the agreement.

**6. PC-GITA** (web search, not a registry record)
- It has 50 PD and 50 HC speakers with vowels, DDK tasks, sentences and monologues. An extended version adds 20 PD and 20 HC recorded in uncontrolled conditions.
- Access: request it from the GITA Lab, University of Antioquia (rafael.orozco@udea.edu.co) and sign a user agreement. The standard citation is Orozco-Arroyave et al., LREC 2014.
- It is the most widely used PD speech benchmark, so it is useful for comparing results.

**7. mPower** (web search; Synapse ID syn4993293)
- It has real-world smartphone voice recordings (sustained /a/, m4a) from a very large app cohort.
- Access: a Synapse account validated by the Access and Compliance Team, a Certified User quiz, and a public Intended Data Use statement. Only participants who opted into broad sharing are included.
- Labels are self-reported, and the "controls" are app users who didn't report PD. That is noisy for detection work.

**8. Bridge2AI-Voice** ([PhysioNet](https://physionet.org/content/b2ai-voice/4.0.0/))
- The PhysioNet release contains no raw audio. Raw audio needs institutional sign-off from the access committee (DACO@b2ai-voice.org, per a web search result).
- One published analysis built a cohort of 106 PD cases and 147 controls from it.

**9. HeyJay!** ([ICPSR](https://www.icpsr.umich.edu/web/ICPSR/studies/39448/versions/V6))
- It is a corpus of atypical English speech that includes PD speakers, built for speech recognition rather than detection.
- I could not confirm that it has healthy controls. Only consider it if you can confirm a control group.

## Known, not confirmed
- **PC-GITA, mPower and the original Italian record** have no registry record. Their access terms come from web search and the Italian licence from the mirror, so confirm each at the source before planning around it.
- **Hugging Face MDVR-KCL copy** (`saeedzou/kcl-parkinson-voice-dataset`): it is gated behind a click-through. Use the Zenodo original instead.
- **Dataset-in-paper "ParkMultiNet"** ([Zenodo](https://zenodo.org/records/22082939)): it is open (CC BY 4.0) with 502 processed speech clips (266 PD, 236 non-PD). The clips are re-processed from other public sets, so using it risks duplicating data you already have.

## Not recommended, and why
- **Figshare "Parkinson-Disease-voice-Dataset", Mendeley DDK set, Zenodo plosive set, Hugging Face `TabBioMed` and `BenchmarkDatasets` Parkinson_Speech:** these hold extracted features or tables, so they fail R1.
- **PADS smartwatch, gait, tremor and keystroke sets on PhysioNet:** they have no speech audio.

## What I could not find
- **Large open datasets:** no open dataset with 100 or more speakers turned up. The largest open sets are the Mandarin one (speaker count unknown) and the Italian one (65 speakers).
- **Registry coverage:** DataCite and Hugging Face dropped out on some queries. The figshare and ICPSR pages blocked automated reading.
- **Reuse caveat:** most sets use different languages and recording setups. A model trained on one often drops sharply on another, so plan for cross-corpus testing.

## Next step
Download MDVR-KCL, VOC-PD, Arabic and Italian today. Send the NeuroVoz request and the PC-GITA email now, since both take time. Together they give you several languages for cross-corpus testing.

Interactive page: `/private/tmp/e-LXXiUX/home/cwd/dataset-shortlist.html`