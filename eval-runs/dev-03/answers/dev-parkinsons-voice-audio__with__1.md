## What I assumed you need
- **R1 (must):** PD patients and healthy controls, with labels.
- **R2 (must):** raw audio files, not feature tables.
- **R3 (nice):** enough speakers for deep learning, and a permissive licence.

I checked this on 2026-11-11/12. I searched OpenAIRE, Zenodo, DataCite, Hugging Face and PhysioNet, plus the literature and the web. The Zenodo, DataCite and Hugging Face searches partly failed on truncated responses, so the list may be incomplete.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [MDVR-KCL](https://doi.org/10.5281/zenodo.2867215) (UK, smartphone) | Open download | CC BY 4.0 | 606 MB | Strong | today |
| 2 | [VOC-PD](https://zenodo.org/records/21775027) (Mandarin) | Open download | CC BY 4.0 | 367 MB, 1,551 wav (811 PD, 740 HC) | Strong | today |
| 3 | [Arabic PD Speech](https://zenodo.org/records/22036480) | Open download | CC BY 4.0 | 39 MB, 17 PD and 23 HC | Strong, but small | today |
| 4 | [Italian Parkinson's Voice and Speech](https://huggingface.co/datasets/birgermoell/Italian_Parkinsons_Voice_and_Speech) (Hugging Face copy) | Open download | CC BY 4.0 | about 65 speakers | Strong | today |
| 5 | [NeuroVoz](https://zenodo.org/records/13647600) (Castilian Spanish) | Request access, owners approve | CC BY-NC-ND 4.0 | about 100 or more speakers (from memory) | Strong | today |
| 6 | PC-GITA (Colombian Spanish) | By email request | Not stated | 50 PD and 50 HC | Strong | web search; I did not open the page |
| 7 | [Bridge2AI-Voice](https://physionet.org/content/b2ai-voice/4.0.0/) | Application plus institutional sign-off | Custom registered-access licence | 48,226 recordings | Partial | today |
| 8 | mPower (Synapse, smartphone) | Qualified-researcher process | Not stated | 65,022 samples from 5,826 people | Partial | web search; I did not open the page |
| 9 | [HeyJay!](https://doi.org/10.3886/icpsr39448.v6) | Restricted, ICPSR | Not stated | more than 8,500 utterances | Partial | today |

## Details
**1. MDVR-KCL.** It has read and spontaneous speech recorded on a phone in a reverberant exam room, with early and advanced PD patients and controls. Download the zip from Zenodo. The cohort is small, so use speaker-independent splits. The noise makes it realistic but harder.

**2. VOC-PD.** It has 1,551 `.wav` files across five Mandarin tasks. It is new (August 2026), so there is little independent use yet. Check the speaker count in the README.

**3. Arabic PD.** It has sustained vowels, passage reading and spontaneous speech. The files are MP3 at 44.1 kHz, which is lossy. It's too small to train on, but it works as an external test set.

**4. Italian PD (IPVS).** The cohort is 28 PD patients, 22 older controls and 15 young controls. The young controls aren't age-matched to the patients. Hugging Face is a third-party copy. The original is on [IEEE DataPort](https://ieee-dataport.org/datasets/italian-parkinsons-voice-and-speech), where sources disagree on the DOI (`10.21227/aw6b-tg17` or `10.21227/s77k-m138`). I didn't verify the original, so cite Dimauro and Girardi. A free IEEE DataPort account may be needed.

**5. NeuroVoz.** The Zenodo page says "The record is publicly accessible, but files are restricted." To get it:
1. Log in to Zenodo.
2. Request access.
3. Accept the Data Agreement Usage.
4. Wait for the owners to approve. I found no stated timescale, so I'd plan on weeks.

The licence is no-derivatives, so check whether sharing trained models or augmented audio is allowed.

**6. PC-GITA.** This is the standard benchmark for PD speech. A web search says it is available on request from Juan Rafael Orozco-Arroyave at Universidad de Antioquia (rafael.orozco@udea.edu.co). I found no public form or licence terms. The corpus has sustained vowels, rapid syllable repetitions and read sentences. Its [LREC paper](https://aclanthology.org/L14-1549/) describes it. Plan on days to weeks.

**7. Bridge2AI-Voice.** The PhysioNet page says: "Accessing raw audio is a more involved process and requires institutional sign off." Email DACO@b2ai-voice.org, and raw audio is delivered through Synapse. It has clinician-confirmed diagnoses and 263 controls, but PD is only one of many conditions. A [JMIR paper](https://doi.org/10.2196/95609) audits age and site confounding in v3.0.0. Take that seriously, because age imbalance alone can give a high AUC. Plan on months.

**8. mPower.** It is in the Synapse project [syn4993293](https://doi.org/10.7303/syn4993293). Per Sage's GitHub repo, you need to:
1. Have a Synapse account.
2. Have your profile validated.
3. Pass the Certified User quiz.
4. Submit a public Intended Data Use statement.

The recordings are `.m4a` voice clips from uncontrolled home environments. Its PD labels are self-reported, which makes it noisy. Plan on days to weeks.

**9. HeyJay!** The description says "restricted-access study", with PD, ataxia and ALS speakers. I couldn't confirm that it has healthy controls, so check that before applying. ICPSR blocked my automated read, so the application process is unconfirmed.

## Known, not confirmed
- **PC-GITA and mPower** come from web search only. Their access terms are from search summaries, not the owners' pages.
- **Figshare "[Parkinson-Disease-voice-Dataset](https://doi.org/10.6084/m9.figshare.32588973.v2)"** (CC BY 4.0, 697 MB). The description says "acoustic speech features", but the size suggests audio could be included. The landing page blocked me, so open it in a browser.

## Not recommended, and why
- **Feature tables only:** the Mendeley DDK-features set, the Zenodo plosive/VOT features (145 KB), and Figshare "Dataset for Parkinson Disease" (0.9 MB).
- **Metadata only:** the Rochester PD screening set holds predictions and labels, not audio.
- **Synthetic data:** the Zenodo "synthetic voice" and spectral-image PD sets.
- **Wrong modality:** PhysioNet PADS smartwatch and the gait/tremor/keystroke sets are not speech.
- **UCI Parkinsons, Oxford, and Sakar multi-recording sets** have features only (from memory).

## What I could not find
I found no large, open, age-matched PD corpus in English. The open sets are small, in different languages, and recorded differently. The PD-vs-control signal is easy to confound with recording conditions and age, so cross-corpus validation matters.

## Next step
Start with MDVR-KCL, VOC-PD, Arabic and Italian today. Together they give you open training and external-test data. In parallel, email the PC-GITA owner, request NeuroVoz on Zenodo, and start the mPower governance steps.

Interactive page: `/private/tmp/e-fNmNEG/home/cwd/dataset-shortlist.html`