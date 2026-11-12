I found six public Parkinson's speech datasets with real audio and healthy controls. Five of them you can download today; NeuroVoz needs an access request. I checked each against its registry record on 2026-11-11 or 2026-11-12, except where marked "from memory".

## What I assumed you need
- **R1 (must):** actual audio files such as .wav, not precomputed features.
- **R2 (must):** labelled Parkinson's (PD) patients and healthy controls (HC).
- **R3 (nice to have):** downloadable now, without a long approval.
- I assumed any language is fine, since you didn't specify one.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | VOC-PD (Mandarin) | open download, minutes | CC-BY-4.0 | 1,551 wav (811 PD, 740 HC), 367 MB | strong | today |
| 2 | MDVR-KCL (King's College London, smartphone) | open download, minutes | CC-BY-4.0 | 606 MB | strong | today |
| 3 | Italian Parkinson's Voice and Speech (IEEE DataPort) | free account, minutes | CC-BY | 565 MB, wav + xlsx | strong | today |
| 4 | Arabic PD Speech Dataset | open download, minutes | CC-BY-4.0 | 17 PD + 23 HC, 39 MB | strong | today |
| 5 | NeuroVoz (Castilian Spanish) | request access, days (my estimate) | CC-BY-NC-ND-4.0 | 2,977 audio files | strong | today |
| 6 | Processed MRI + Speech for PD (ParkMultiNet) | open download, minutes | CC-BY-4.0 | 502 clips, 1.3 GB with MRI | partial | today |

## Details
1. **VOC-PD** (https://doi.org/10.5281/zenodo.21775027)
   - It has five task folders: numbers, phrases, sentences, vowels and more.
   - Download the zips from the Zenodo record.
   - It's a 2026 release and nobody has cited it yet.
   - Check the xlsx for speaker IDs so you can split train and test by speaker.
2. **MDVR-KCL** (https://doi.org/10.5281/zenodo.2867215)
   - It has read speech and spontaneous dialogue with early and advanced PD patients, recorded over a phone-quality channel.
   - It has about 3,000 downloads and 17 citations.
   - The cohort is small, roughly 37 speakers. That figure is from memory, not confirmed today.
3. **Italian Parkinson's Voice and Speech** (https://doi.org/10.21227/aw6b-tg17)
   - The IEEE DataPort page says: "Open Access dataset files are accessible to all logged in users." Create a free account, log in and download.
   - Hugging Face holds several uploader copies. Cite and download from IEEE DataPort, not the copies.
   - Which recordings are PD and which are HC is from memory. Check it in the xlsx.
4. **Arabic PD Speech** (https://zenodo.org/records/22036480)
   - It has sustained vowels, a read passage and spontaneous speech.
   - Forty speakers is too few to train on alone. It's useful as a cross-lingual test set.
5. **NeuroVoz** (https://zenodo.org/records/13647600)
   - It has about 27 recordings per participant, from PD patients and controls.
   - Zenodo says: "The record is publicly accessible, but files are restricted." Log in, use "Request access" and accept the Data Usage Agreement.
   - The licence is non-commercial and no-derivatives. Ask the owners whether trained models or augmented audio count as derivatives.
   - One paper that used it is [Multilingual evaluation of interpretable biomarkers in PD speech](https://doi.org/10.3389/fneur.2023.1142642) (2023).
6. **ParkMultiNet** (https://zenodo.org/records/22082939)
   - It's a repackaging of clips from other public sources, plus MRI.
   - It will overlap with other sets, so don't mix it with them in train and test splits.
   - I haven't confirmed whether the clips are waveforms or spectrograms.

## Known, not confirmed
- **PC-GITA** (Colombian Spanish): no registry record found. From memory, it's available from the authors on request only.
- **mPower** (Synapse, smartphone voice): no registry record found. From memory, it needs a Synapse account and a study application.
- **Two figshare sets**: "Parkinson-Disease-voice-Dataset" (https://doi.org/10.6084/m9.figshare.32588973.v2) and "Dataset for Parkinson Disease" (https://doi.org/10.6084/m9.figshare.33212514.v1). The DOIs are registered, but figshare blocked my page check. I don't know whether they hold audio.
- **Czech and German corpora**: I didn't search for them.

## Not recommended, and why
- **NeuroVoz Rasta-PLP** on Zenodo is features only.
- **Bridge2AI-Voice on PhysioNet**: the page says "This PhysioNet project does not contain raw audios." Raw audio goes through Synapse and needs institutional sign-off.
- **Synthetic PD voice set** (Zenodo 17753641) is synthetic, not real speakers.
- **BenchmarkDatasets/Parkinson_Speech** on Hugging Face looks like a tabular feature set. I didn't open it to confirm.
- **UCI Parkinson datasets** are feature tables. This is from memory.

## What I could not find
- I searched DataCite, Hugging Face, OpenAIRE, PhysioNet and Zenodo, plus the literature. I did not search project sites or challenge pages, so the list may be incomplete.
- For most datasets I didn't find papers that used them. Only NeuroVoz has one, so you'd need to search for baselines yourself.

## Next step
Start with Italian PVS, MDVR-KCL and VOC-PD. Request NeuroVoz access now so it's ready when you need it. Always split by speaker, because several recordings per person make random splits leak.

Files are in /private/tmp/e-xcEAV5/home/cwd:
- dataset-shortlist.html
- dataset-scout/shortlist.json