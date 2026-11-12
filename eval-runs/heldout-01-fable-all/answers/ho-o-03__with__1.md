Start with **AMI**, **NOTSOFAR-1** and **ICSI**: all three are real English meetings with speaker-attributed transcripts and distant-microphone audio, and all three are released under CC BY 4.0, which allows commercial use with attribution. Together they give you roughly 200 hours you can download today. Nothing I found offers hundreds of hours of genuine corporate meetings with far-field audio under a commercial licence.

All facts below were checked on 2026-11-12 against the named pages unless marked "from memory".

## What I assumed you need
- **Must:** real recorded multi-party conversation (no simulated mixtures), speaker-turn annotation, English, and a licence that allows commercial use (a fee is acceptable).
- **Nice to have:** business-style meetings, and far-field or microphone-array audio.
- **My assumption:** "commercial use" means training and evaluating models that ship in your product, not redistributing the audio.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | AMI Meeting Corpus | Direct download | CC BY 4.0 | 100 h | Strong | today |
| 2 | NOTSOFAR-1 recorded meetings | Free Hugging Face account and token | CC BY 4.0, with "for open research" wording | 237 meetings of about 6 min | Strong | today |
| 3 | ICSI Meeting Corpus | Direct download | CC BY 4.0 | about 72 h, 75 meetings | Strong | licence today; size from a search result |
| 4 | DiPCo | Direct download | CDLA-Permissive 1.0 | about 5 h (from memory) | Partial: dinner party | today |
| 5 | CHiME-6 | Direct download | CC BY-SA 4.0 | about 40–50 h (from memory) | Partial: dinner party, share-alike | today |
| 6 | Earnings-21 | Direct download | CC BY-SA 4.0 | 39 h | Partial: business, not far-field | today |
| 7 | LDC corpora via for-profit membership | Membership agreement and fee, weeks | LDC member agreement | varies | Partial | terms today; sizes and fee from memory |

## Details

**1. [AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/corpus/)**
- **Contents:** 100 hours of recorded meetings with headset, lapel and microphone-array channels, plus manual transcripts with speaker and timing.
- **Limits:** most meetings are role-played ("participants play different roles in a fictitious design team"), so they are business-style but elicited. The recordings come from a small number of instrumented rooms in the mid-2000s (from memory).
- **Access:** pick meetings and signals on the [download page](https://groups.inf.ed.ac.uk/ami/download/) and fetch the 22 MB manual annotations file.
- **Licence:** "The AMI corpus and its annotations are released under the Creative Commons Attribution 4.0 license."
- **Used in:** [Carletta 2007](https://doi.org/10.1007/s10579-007-9040-x) (corpus description) and [ECAPA-TDNN diarization, 2021](https://doi.org/10.21437/interspeech.2021-941).

**2. [NOTSOFAR-1](https://github.com/microsoft/NOTSOFAR1-Challenge)** (Microsoft)
- **Contents:** "237 meetings, each averaging 6 minutes, recorded across 30 conference rooms" with 35 speakers, captured on single-channel and multi-channel array devices, with ground-truth speaker-attributed transcripts. This is the closest match to real product acoustics.
- **Limits:** only about 24 hours of distinct meetings. Dev-set-2 is challenge-only and not in the open release.
- **Access:** create a Hugging Face token, set `HF_TOKEN`, and call `download_meeting_subset` from the repository.
- **Licence:** the README says CC BY 4.0 but also "The datasets are provided for open research", and the Hugging Face record has no licence tag. Have counsel read the data licence file or ask Microsoft before relying on it.
- **Used in:** [NOTSOFAR-1 Challenge paper, 2024](https://doi.org/10.21437/interspeech.2024-1788).

**3. [ICSI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/icsi/)**
- **Contents:** naturally occurring research-group meetings with per-speaker headset channels, distant table microphones (not a geometric array, from memory) and speaker-attributed transcripts.
- **Limits:** academic rather than corporate meetings, recorded around 2000–2002 (from memory).
- **Access:** download from the Edinburgh site. The LDC copy (LDC2004S02) is under LDC terms, so avoid it.
- **Licence:** "The ICSI corpus and its annotations are released under the Creative Commons Attribution 4.0 license."
- **Used in:** [Janin et al. 2003](https://doi.org/10.1109/icassp.2003.1198793).

**4. [DiPCo](https://zenodo.org/records/8122551)**
- **Contents:** real four-person dinner-party conversations on far-field array devices plus close-talk microphones (device layout from memory).
- **Use:** small, so best as far-field test or adaptation data.
- **Licence:** Community Data License Agreement Permissive 1.0, open download.

**5. [CHiME-6](https://openslr.org/150/)**
- **Contents:** home dinner parties recorded on multiple arrays; the training tarball is 97 GB.
- **Licence:** "Attribution-ShareAlike 4.0". Commercial use is allowed, but whether a trained model must carry the same licence is unsettled. Using it only as a test set avoids the question.
- **Used in:** [CHiME-7 DASR, 2023](https://doi.org/10.21437/chime.2023-1), alongside DiPCo and Mixer 6.

**6. [Earnings-21](https://github.com/revdotcom/speech-datasets/tree/main/earnings21)** (Rev.com)
- **Contents:** 39 hours of real earnings calls with a speaker id on every reference token.
- **Fit:** good for business vocabulary and long-form multi-speaker evaluation, but it is phone and webcast audio.
- **Licence:** CC BY-SA 4.0, with the same share-alike caveat as CHiME-6.

**7. LDC via for-profit membership** (for example [NIST Meeting Pilot, LDC2004S09](https://catalog.ldc.upenn.edu/LDC2004S09), [Mixer 6, LDC2013S03](https://catalog.ldc.upenn.edu/LDC2013S03), Fisher)
- **Terms:** the [LDC licensing page](https://www.ldc.upenn.edu/data-management/using/licensing) says "For-profit organizations who are or were LDC members may conduct commercial technology development with LDC data". Nonmembers, including companies paying the non-member fee, "cannot use LDC data to develop or test products for commercialization".
- **Steps:** ask LDC for a for-profit quote, join, then license older corpora at the reduced member fee. Check each corpus-specific agreement.
- **Cost and time:** tens of thousands of US dollars a year (from memory), and weeks to complete.
- **Value:** mainly large telephone conversational sets and a few small meeting-room sets.

## Known, not confirmed
- **Defined.ai "Meeting Recordings":** search snippets describe 99,500 hours of English meetings with audio, video and transcripts, and the vendor says its datasets are cleared for commercial use. The catalogue page would not load, so speaker labels, capture conditions and price are unknown. Ask whether transcripts carry timed speaker turns and whether the audio is far-field or online-meeting capture.
- **Nexdata and Magic Data:** they list English conversational sets of 172 to 1,178 hours with paid commercial licences. The snippets describe these as close-talk or speaker-separated dialogue, not far-field meetings.
- **Earnings-22:** 119 hours in the same Rev repository. I did not confirm its licence or whether it has speaker labels.
- **ELRA CHIL seminars and Fearless Steps (Apollo):** both may fit from memory. I did not check them today.

## Not recommended, and why
- **MeetingBank:** CC BY-NC-SA 4.0, so non-commercial.
- **VoxConverse:** released "for research purposes", and the audio is taken from YouTube videos the dataset does not own.
- **DIHARD II/III:** the LDC non-member agreement gives no commercial rights.
- **NOTSOFAR simulated training set, LibriCSS, LibriWASN:** simulated or replayed speech.
- **AliMeeting and AISHELL-4:** Mandarin (from memory).

## What I could not find
- A large, far-field corpus of genuine corporate meetings in English under a commercial licence.
- A vendor listing that confirms both microphone-array capture and speaker-turn labels.
- Search coverage was incomplete: one Hugging Face registry query failed.

## Next step
Download AMI, NOTSOFAR-1 and ICSI today, and hold out NOTSOFAR-1's eval set as your product-like benchmark. In parallel, send Defined.ai and Nexdata the two questions above. Because CC licences cover copyright but not participant consent or voice-data privacy, get a short legal review before shipping models trained on any of these.

The interactive shortlist is at `/private/tmp/e-4TKw7J/home/cwd/dataset-shortlist.html`.