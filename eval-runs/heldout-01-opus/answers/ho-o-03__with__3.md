Use **AMI** and **NOTSOFAR-1** first. Both are real English meetings with speaker-attributed transcripts and microphone-array audio, under CC BY 4.0, which allows commercial use. You can download both today. If you want more data later, a paid LDC for-profit membership is the main way to add more.

Checked on 12 Nov 2026 against each dataset's official pages unless marked "from memory".

## What I assumed you need
- **Must have:** real (not simulated) multi-party conversation; who-spoke-when labels; English; a licence that allows commercial use (a fee is fine).
- **Nice to have:** business-style meetings; far-field or microphone-array audio.
- **Assumed:** "Commercial use" means training and evaluating models for a product. You don't need to redistribute the raw data.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/download/) | Direct download, minutes | CC BY 4.0 | ~100 h, 2 tabletop 8-mic arrays + headsets | Strong | today |
| 2 | [NOTSOFAR-1](https://huggingface.co/datasets/microsoft/NOTSOFAR) ([repo](https://github.com/microsoft/NOTSOFAR1-Challenge)) | Direct download, no sign-up | CC BY 4.0 | 315 office meetings, 30 rooms, up to 7 far-field devices | Strong | today |
| 3 | [ICSI Meeting Corpus (free Edinburgh release)](https://groups.inf.ed.ac.uk/ami/icsi/) | Direct download | CC BY 4.0 | ~72 h | Partial: headset audio only | today |
| 4 | [DiPCo](https://zenodo.org/records/8122551) | Direct download | CDLA-Permissive 1.0 | 10 sessions, 4 speakers each, 5 arrays | Partial: dinner parties | today |
| 5 | [CHiME-6 (OpenSLR 150)](https://openslr.org/150/) | Direct download, ~120 GB | CC BY-SA 4.0 | ~40 h, 6 Kinect arrays | Partial: dinner parties | today |
| 6 | [ICSI Meeting Speech, LDC2004S02](https://catalog.ldc.upenn.edu/LDC2004S02) | LDC for-profit membership, weeks | LDC commercial licence | ICSI including far-field mics | Strong | today (terms); far-field contents from memory |
| 7 | [NIST RT-05S eval set, LDC2011S06](https://catalog.ldc.upenn.edu/LDC2011S06) (+ RT-06S/07S) | LDC for-profit membership | LDC | Small benchmark sets | Partial | today (catalog); contents partly from memory |
| 8 | [NIST Meeting Pilot, LDC2004S09](https://catalog.ldc.upenn.edu/LDC2004S09) | LDC for-profit membership | LDC | ~15 h | Partial | catalog today; details from memory |
| 9 | [ISL Meeting Speech, LDC2004S05](https://catalog.ldc.upenn.edu/LDC2004S05) | LDC for-profit membership | LDC | — | Partial | catalog today |
| 10 | [Rev Earnings-21](https://github.com/revdotcom/speech-datasets) | git clone (LFS) | CC BY-SA 4.0 (transcripts) | ~39 h | Weak: calls, not far-field | today |

## Details
**1. AMI.** About two-thirds are "scenario" meetings: real people playing a product-design team, unscripted, usually 4 participants. The rest are natural meetings. The free download includes the headset audio and two tabletop microphone arrays. The download page says: *"audio channels from 2 table top microphone arrays"*. Manual word-level transcripts with speaker IDs come in NXT format, and the usual diarization references are built from them.
- **Licence:** the licence page says *"released under the Creative Commons Attribution 4.0 license"*. You only need to give credit.
- **Steps:** download the manual annotations zip, then use the page's chooser to pick the array and headset streams. It generates a wget script.
- **Caveats:** recorded around 2005 in 3 rooms, mostly 4 speakers, many non-native speakers. The role-play is a nuance, but it is real conversation, not a simulated mixture.
- **Papers:** [Carletta 2007, corpus description](https://doi.org/10.1007/s10579-007-9040-x); [Speaker diarization for meeting room audio, 2009](https://doi.org/10.21437/interspeech.2009-271).

**2. NOTSOFAR-1 (Microsoft).** Real office meetings with 4–8 attendees, recorded on commercial far-field devices: 4 tabletop devices with 7-mic arrays and 3 linear devices that give a single processed channel. It was used for the CHiME-8 distant diarization and speech recognition task.
- **Licence:** I read the repo's DATA_LICENSE file today. It is plain CC BY 4.0 with no commercial restriction. The Hugging Face dataset is not gated.
- **Caveats:** only 35 unique speakers, and meetings average about 6 minutes.
  - The 1000-hour training set is **simulated**, so use only the recorded meetings.
  - The repo says Dev-set-2 was approved only for use within the challenge.
- **Papers:** [NOTSOFAR-1 dataset paper, Interspeech 2024](https://doi.org/10.21437/interspeech.2024-1788); [BUT/JHU CHiME-8 system](https://doi.org/10.21437/chime.2024-4).

**3. ICSI (Edinburgh).** Natural weekly research meetings with 3–10 people, released under CC BY 4.0. The download page lists only *"Headset mix"* and *"Individual channel headsets"*, so the free release has **no far-field audio**. I believe the transcripts carry speaker-timed segments (from memory; check the transcript files).

**4. DiPCo (Amazon).** Real, unscripted conversation among volunteers, recorded on five 7-mic arrays, under CDLA-Permissive. It is small (about 5 h) and social rather than business. Use the Zenodo record; the original AWS link has expired.

**5. CHiME-6.** Real dinner parties in homes, with JSON transcripts carrying speaker and start/end times. The OpenSLR page says *"License: Attribution-ShareAlike 4.0"*, which allows commercial use.
- **Conflict:** the old CHiME-5 terms charged commercial users £2,000. Keep the bundled LICENSE.txt and have counsel confirm.
- **ShareAlike** applies to redistributed adapted data. Whether it reaches trained models is a legal question.

**6–9. LDC meeting corpora.** LDC's non-member licence is research-only. LDC newsletters say for-profit organisations without membership *"cannot use LDC data to develop or test products for commercialization"*. Commercial use needs the [For-Profit Membership](https://www.ldc.upenn.edu/sites/default/files/for-profit-membership-agreement.pdf). An undated agreement PDF puts the Standard tier at **$24,000/year for up to 16 corpora**; ask LDC for a current quote. Membership gets you:
- the ICSI far-field (PZM tabletop) channels, from memory: 4 tabletop + 2 cheap microphones;
- the NIST RT meeting sets, which are the classic meeting-diarization benchmarks;
- the NIST Meeting Pilot and ISL meeting corpora.

**10. Earnings-21.** Real business calls with speaker IDs per word (Earnings-22 has no speaker labels). It's telephone/webcast audio dominated by presenters. CC BY-SA covers the transcripts, but the Earnings-22 paper rests the audio on fair use. Get legal review before training a product on it.

## Known, not confirmed
- **Commercial data vendors** (Appen, Defined.ai, Shaip and similar) sell or commission English meeting recordings with diarization labels and full commercial rights. I didn't check their current catalogues or prices.

## Not recommended, and why
- **EasyCom (Meta):** CC BY-NC 4.0, so non-commercial.
- **ELITR Minuting Corpus:** text only (no audio), and reported as CC BY-NC-SA.
- **VoxConverse:** YouTube debates and news, not meetings. Its page says the audio is *"currently not available on this website"*, and the audio rights belong to the YouTube creators.
- **LibriCSS and other simulated mixtures:** you excluded these.
- **AliMeeting, AISHELL-4, MISP-Meeting:** Mandarin.
- **SPGISpeech:** non-commercial licence (from memory).
- **DIHARD III, Mixer 6 (LDC):** mostly not meetings. Consider them only if you already hold an LDC membership.

## What I could not find
- No free, commercially licensed corpus of real **business** meetings with arrays is larger than about 100 h (AMI). NOTSOFAR-1 is the most realistic but small.
- For production-scale training you will probably need to commission or buy data, or record your own customers' meetings with consent.

The registry searches were noisy, and the Hugging Face search partly failed. LDC's fee page blocked automated access.

## Next step
1. Download AMI (arrays and annotations) and NOTSOFAR-1 today, and build your diarization training and evaluation pipeline on them.
2. Use DiPCo and CHiME-6 for far-field robustness, after counsel confirms the CHiME-6 ShareAlike terms.
3. Ask LDC for a for-profit membership quote. It gets you ICSI far-field and the NIST RT sets as extra benchmarks.
4. Get quotes from one or two vendors for custom business-meeting recordings.

Licences and access rules change, so recheck these before you sign anything. I didn't save anything to your repo's git history. The interactive page lets you filter and compare the datasets and export an access plan.

Files are in `/private/tmp/e-FNI7jr/home/cwd`:
- `dataset-shortlist.html`
- `dataset-scout/shortlist.json`