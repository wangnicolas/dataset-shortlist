I found six datasets of raw PD and healthy-control audio. Four can be downloaded today, one needs a request approved, and one is gated behind institutional sign-off. I checked them on 2026-11-11 and 2026-11-12. Zenodo and DataCite errored on some queries, so the search may have missed some datasets.

## What I assumed you need
- **R1 (must):** actual audio files (wav/mp3), not feature tables.
- **R2 (must):** PD patients and healthy controls, labelled.
- **R3 (nice):** quick access, and a licence that allows ML training.

I assumed any language is acceptable, since you didn't specify one.

## Shortlist
| # | Dataset | Access | Licence | Size / contents | Checked |
|---|---|---|---|---|---|
| 1 | VOC-PD (Mandarin) | Open download | CC BY 4.0 | 1,551 wav files: 811 PD, 740 HC | today |
| 2 | Arabic PD Speech (Mutah Univ.) | Open download | CC BY 4.0 | 40 speakers (17 PD, 23 HC), mp3 | today |
| 3 | MDVR-KCL (London, smartphone) | Open download | CC BY 4.0 | early and advanced PD plus HC | today |
| 4 | Italian Parkinson's Voice and Speech | Free IEEE DataPort account | CC BY (as stated on the page) | wav, ~565 MB | today |
| 5 | NeuroVoz (Castilian Spanish) | Request access, accept a data agreement; I'd guess days to weeks | CC BY-NC-ND 4.0 | multi-task corpus with controls | today |
| 6 | Bridge2AI-Voice | Raw audio via Synapse, needs institutional sign-off; likely weeks to months | Registered Access licence | large, multi-condition; 263 controls | today |

## Details
- **VOC-PD:** https://doi.org/10.5281/zenodo.21775027. It has five task folders: numbers, phrases, sentences, vowels and monophthongs. Download directly from Zenodo. It was published in August 2026, so no papers use it yet. I didn't check how the diagnoses were confirmed.
- **Arabic PD:** https://doi.org/10.5281/zenodo.22036480. It has sustained vowels, a read passage and spontaneous speech. There are only 40 subjects, so split by speaker to avoid leakage. The mp3 format is lossy.
- **MDVR-KCL:** https://doi.org/10.5281/zenodo.2867215. I didn't confirm exact subject counts from the page text. A 2021 arXiv comparison paper used it alongside the Italian corpus (https://doi.org/10.48550/arxiv.2111.10207).
- **Italian:** https://ieee-dataport.org/open-access/italian-parkinsons-voice-and-speech. The page says "Open Access dataset files are accessible to all logged in users", but it also mentions an IEEE DataPort Subscription. Check what the free account actually gives you. HuggingFace copies exist (e.g. `birgermoell/Italian_Parkinsons_Voice_and_Speech`); they are third-party mirrors, so use the IEEE original. A 2024 *Journal of Voice* paper on audio spectrogram transformers (https://doi.org/10.1016/j.jvoice.2024.11.008) came up for this corpus.
- **NeuroVoz:** https://doi.org/10.5281/zenodo.13647600. Zenodo says "The record is publicly accessible, but files are restricted" and that you accept a Data Agreement Usage through request access. The non-commercial, no-derivatives licence may limit sharing models or derived features, so read the agreement. An Interspeech 2025 paper (https://doi.org/10.21437/interspeech.2025-801) used it with pre-trained audio embeddings.
- **Bridge2AI-Voice:** https://physionet.org/content/b2ai-voice/4.0.0/. PhysioNet says raw audio "requires institutional sign off" and goes through Synapse, with requests to DACO@b2ai-voice.org. I didn't check how many PD participants it has. It's a weaker fit than the others.

## Known, not confirmed
These are from memory. I didn't confirm them today.
- **PC-GITA** (Colombian Spanish, GITA group, Univ. of Antioquia): widely used, with sustained vowels, DDK and sentences. As I recall, you request it from the authors and sign a license agreement. It isn't openly downloadable.
- **Czech PD corpora (Rusz et al.):** I recall these as available only on request from the authors.
- **mPower (Sage Bionetworks, Synapse):** voice recordings from a smartphone study of PD patients and controls. As I recall, you register on Synapse and pass a qualification step. I tried the portal (https://www.synapse.org/Synapse:syn4993293), but the page loads by JavaScript and returned no text. Controls there are self-reported and not clinically confirmed, which weakens labels.

## Not recommended, and why
- **Zenodo 10406860 (plosive consonants):** extracted features only, no audio.
- **Two figshare records** (https://doi.org/10.6084/m9.figshare.32588973.v2 and https://doi.org/10.6084/m9.figshare.33212514.v1): described as extracted acoustic features and voice measurements. I couldn't open the pages because of a bot challenge, so they may contain audio, but I doubt it.
- **Synthetic PD voice records on Zenodo:** synthetic data, not real patients.
- **UCI/Oxford PD tables:** these are feature tables, which you ruled out (from memory).

## What I could not find
I found no large English-language PD corpus that you can simply download. Pooling the open sets above gives you four languages, which suits cross-corpus work but adds language and recording-device confounds.

## Next step
Start with VOC-PD, Arabic, MDVR-KCL and Italian today. Submit the NeuroVoz request now, since it's the slow one. Train and test by speaker, and hold out an entire corpus to test generalisation. Two of these sets are small, so a single-corpus score will look better than it should.

Page: `/private/tmp/e-KbBN0V/home/cwd/dataset-shortlist.html`