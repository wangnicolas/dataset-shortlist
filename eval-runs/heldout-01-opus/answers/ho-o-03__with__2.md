**Short answer:** use **AMI**, plus **NOTSOFAR-1** (after one licence check) and **ICSI**. All three are free downloads, and AMI and ICSI are CC BY 4.0, so commercial use is allowed. **DiPCo** and **CHiME-6** add more microphone-array audio, and **Earnings-21/22** adds real business calls. You don't need to buy a licence to start.

Checked 12 Nov 2026. "Today" means I read the licence or access page during this check. Sizes and contents are from memory unless stated. This isn't legal advice.

## What I assumed you need
- **R1 (must):** real multi-party conversations, not simulated, ideally business meetings
- **R2 (must):** who-spoke-when annotations
- **R3 (nice to have):** far-field or microphone-array audio
- **R4 (must):** English
- **R5 (must):** commercial use allowed; a paid licence is fine

## Shortlist
| # | Dataset | Access | Licence | Size (from memory) | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | AMI Meeting Corpus | Direct download, minutes | CC BY 4.0 | ~100 h, 4-person meetings, 8-mic arrays | Strong | today |
| 2 | NOTSOFAR-1 (recorded meetings only) | Direct download, minutes | CC BY 4.0 in the repo, **but conflicting** (see below) | ~315 real office meetings, 4–8 people, commercial meeting devices | Strong | today |
| 3 | ICSI Meeting Corpus | Direct download, minutes | CC BY 4.0 | ~72 h, 3–10 people, tabletop mics | Strong | today |
| 4 | DiPCo (Amazon) | Direct download, minutes | CDLA-Permissive-1.0 | ~5 h, 4 people, five 7-mic arrays | Partial (dinner party) | today |
| 5 | CHiME-6 | Direct download (OpenSLR 150), minutes | CC BY-SA 4.0 | ~50 h, 4 people, six 4-mic Kinect arrays | Partial (home dinner) | today |
| 6 | Earnings-21 / Earnings-22 (Rev) | git clone with Git LFS | CC BY-SA 4.0 | 39 h + ~119 h earnings calls | Partial (no far-field audio) | today |
| 7 | ICSI from LDC (LDC2004S02) | Paid LDC licence, days | LDC commercial terms | Same data as #3 | Strong | from memory |
| 8 | NIST RT-05S and the other NIST Rich Transcription meeting sets (LDC2011S06 etc.) | Paid LDC licence, days | LDC non-member or for-profit agreement | Small evaluation sets, several distant mics and arrays | Partial | today (fee confirmed); commercial terms from memory |

## Details
1. **AMI** – https://groups.inf.ed.ac.uk/ami/corpus/
   - **Contents:** close-talk and array audio, manual speaker segments, a standard train/dev/test split. It's the reference benchmark for meeting diarization.
   - **Licence:** the licence page says "The AMI corpus and its annotations are released under the Creative Commons Attribution 4.0 license."
   - **Caveat:** about 70% are scenario meetings where people role-play a design team. The speech is spontaneous but the topic is staged, and many speakers are non-native.
   - **Paper:** *Speaker diarization in meeting audio for single distant microphone* (Interspeech 2010).

2. **NOTSOFAR-1** – https://github.com/microsoft/NOTSOFAR1-Challenge (also on Hugging Face as `microsoft/NOTSOFAR`)
   - **Why it fits:** natural office meetings recorded on real meeting-room devices. It's the closest match to your product.
   - **Licence conflict:** the repo's `DATA_LICENSE` file and the Hugging Face card both say CC BY 4.0. But the CHiME-8 data page says "This public data is currently licensed for use exclusively in the NOTSOFAR challenge event." **Get written confirmation from Microsoft before commercial use.**
   - **Caveat:** use only the recorded meeting subset. The 1000-hour training set is simulated.
   - **Papers:** the dataset paper (Interspeech 2024, doi 10.21437/interspeech.2024-1788) and *Once more Diarization* (Interspeech 2024).

3. **ICSI** – https://groups.inf.ed.ac.uk/ami/icsi/
   - **Why it fits:** real weekly research-group meetings with speaker-attributed, time-aligned transcripts.
   - **Licence:** the page states CC BY 4.0.
   - **Caveats:** the distant mics are tabletop microphones, not a true array. Recorded 2000–2002 and heavy on academic jargon.

4. **DiPCo** – https://zenodo.org/records/8122551
   - **Contents:** natural conversation among four Amazon volunteers around a dining table, recorded with five far-field 7-mic arrays plus close-talk mics, with human-labelled transcripts.
   - **Licence:** CDLA-Permissive-1.0, a permissive licence that allows commercial use.

5. **CHiME-6** – https://www.openslr.org/150/
   - **Licence:** OpenSLR states "License: Attribution-ShareAlike 4.0." The ShareAlike clause matters if you redistribute derived data. Have counsel confirm how it applies to trained models.
   - **Note:** I recall stricter terms for the older CHiME-5 release, so use this OpenSLR release.

6. **Earnings-21/22** – https://github.com/revdotcom/speech-datasets
   - **Why it fits:** real business calls with a speaker per word, plus RTTM files added in 2023 for diarization error rate (DER) scoring.
   - **Gaps:** not far-field, and there's little overlapping speech.

7–8. **LDC** – https://catalog.ldc.upenn.edu/LDC2004S02 and https://catalog.ldc.upenn.edu/LDC2011S06
   - Paid route: the page shows a "User Agreement for Non-Members" with a fee. Worth it only if you want the NIST evaluation sets or your counsel prefers a signed commercial licence.

## Known, not confirmed
- **Commercial data vendors** (from memory): firms such as Appen, Defined.ai and Shaip sell or custom-record consented meeting audio with diarization labels. I didn't check any of their catalogues. They're the realistic way to get real business meetings in large volume.
- **ELRA catalogue** (from memory): it may hold older meeting corpora such as CHIL under commercial licences. I didn't check it.

## Not recommended, and why
- **NOTSOFAR simulated training set:** simulated mixtures, which you ruled out.
- **VoxConverse:** YouTube news and debate audio, not meetings. Its README says it's "for research purposes" even though it's labelled CC BY 4.0, so commercial use of the audio is unclear.
- **DISPLACE 2023/2024:** CC BY 4.0, but the conversations mix Indian languages with English.
- **Trelis/tiron-eval-meetings:** 17 clips re-cut from AMI, ICSI and NOTSOFAR. Use the originals.
- **Mixer 6:** mostly two-party interviews and calls.
- **VIP-MINGLE:** controlled access for research only.
- **AliMeeting, AISHELL-4:** Mandarin.
- **Switchboard, Fisher, CALLHOME:** telephone, mostly two-party.
- **LibriCSS, LibriWASN:** read speech played back in a room, not real conversation.
- **Ego4D, MSDWild, AVA-AVD, CANDOR:** non-commercial or research-only terms (from memory).
- **Santa Barbara Corpus:** its page returned a 404. From memory it's small groups of two or three people on single mics, under a no-derivatives licence.

## What I could not find
No large (over 100 hours), openly licensed corpus of real business meetings with array audio exists beyond AMI, NOTSOFAR and ICSI combined. To go beyond roughly 200 hours of real meetings, you'll need to buy data from a vendor or record your own with consent. The Hugging Face search failed (its response was too large), so coverage there is partial.

## Next step
1. Download AMI (array plus headset streams) and ICSI today, and set up a DER baseline, for example with pyannote.
2. Open a GitHub issue on NOTSOFAR1-Challenge to confirm commercial use under CC BY 4.0, then add its meetings as your main in-domain test set.
3. Have counsel review the ShareAlike terms for CHiME-6 and Earnings before you use them in training.

The interactive shortlist page is at `/private/tmp/e-13pKAA/home/cwd/dataset-shortlist.html`.