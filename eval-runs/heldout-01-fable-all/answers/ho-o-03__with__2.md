Use three corpora together: **AMI**, **NOTSOFAR-1** and **ICSI**. All three are real English meetings with speaker-turn annotations, all are CC BY 4.0 (commercial use allowed with attribution), and all are free to download today. Together they give you roughly 200 hours; nothing larger that meets your licence requirement turned up, open or paid.

Licence facts below were read from each dataset's own page on 12 November 2026. Sizes and microphone details marked "from memory" were not confirmed today.

## What I assumed you need
- **Must:** real recorded multi-party conversation, who-spoke-when annotations, English, commercial use allowed (fee acceptable).
- **Nice to have:** business-style meetings, far-field or microphone-array audio.
- **Assumption:** you want data for both training and evaluation.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | AMI Meeting Corpus | Direct download | CC BY 4.0 | ~100 h | Strong | today |
| 2 | NOTSOFAR-1 (Microsoft) | Direct download (AzCopy) | CC BY 4.0, with a conflict noted below | 315 meetings, ~6 min each | Strong | today |
| 3 | ICSI Meeting Corpus | Direct download | CC BY 4.0 | ~70 h | Strong | today |
| 4 | DiPCo | Direct download | CDLA-Permissive 1.0 | ~5 h (from memory) | Partial: dinner party | today |
| 5 | CHiME-6 | Direct download | CC BY-SA 4.0 | ~50 h (from memory) | Partial: dinner party, share-alike | today |
| 6 | Earnings-21 (Rev) | Direct download (Git LFS) | CC BY-SA 4.0 | 39 h | Partial: calls, not far-field | today |
| 7 | LDC meeting corpora (ISL, NIST Pilot) | For-profit membership fee, weeks | LDC agreement | ~10–15 h each (from memory) | Partial | terms via search |
| 8 | Nexdata 172 h US English dialogue | Paid, quote from vendor | Vendor commercial licence | 172 h | Weak: phone close-talk | today |

## Details

**1. [AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/corpus/)**
- **Contents:** about 100 hours with close-talking and far-field microphones; 8-microphone circular arrays (from memory).
- **Fit:** the standard meeting diarization benchmark, and the meetings are design-team project meetings.
- **Limits:** about two-thirds is role-played scenario; the rest is naturally occurring meetings. It was recorded in three rooms in the mid-2000s (from memory).
- **Licence:** the page says signals, transcription and "some of the annotations" are CC BY 4.0, so check the note on the annotation download.
- **Access:** follow the site's Download page, or use the [Hugging Face copy](https://huggingface.co/datasets/edinburghcstr/ami).
- **Paper:** [Unleashing the killer corpus](https://doi.org/10.1007/s10579-007-9040-x) (2007).

**2. [NOTSOFAR-1](https://huggingface.co/datasets/microsoft/NOTSOFAR)**
- **Contents:** 315 meetings in 30 office conference rooms, 4–8 attendees, about 35 speakers. Far-field devices include 7-channel arrays, plus close-talk microphones.
- **Annotations:** speaker ID per utterance and word-level timings.
- **Fit:** the closest match to a modern product setting, but small. The separate 1000-hour training set is simulated, so leave it out.
- **Licence conflict:** the dataset card and the [DATA_LICENSE file](https://github.com/microsoft/NOTSOFAR1-Challenge/blob/main/DATA_LICENSE) both say CC BY 4.0. The older [CHiME-8 data page](https://www.chimechallenge.org/challenges/chime8/task2/data) still says challenge-only, and one third-party comparison table lists it as non-commercial. I'd rely on the licence file, but save a dated copy.
- **Access:** clone the [GitHub repo](https://github.com/microsoft/NOTSOFAR1-Challenge) and download with its script or AzCopy.
- **Papers:** [NOTSOFAR-1 Challenge](https://doi.org/10.21437/interspeech.2024-1788) (2024); [DiCoW](https://doi.org/10.1016/j.csl.2025.101841) (2025).

**3. [ICSI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/icsi/)**
- **Contents:** about 70 hours of natural research-group meetings (not role-played, from memory).
- **Limits:** academic rather than business meetings. The page mentions only close-talking microphones; tabletop distant microphones exist in the corpus from memory, so check they are in the download.
- **Access:** follow the site's download page. Avoid the [LDC copy](https://catalog.ldc.upenn.edu/LDC2004S02), which carries a non-commercial non-member agreement for the same audio.

**4. [DiPCo](https://zenodo.org/records/8122551)**
- Four-person conversations recorded on five far-field 7-microphone arrays plus close-talk. Good far-field test data, but it is a dinner party.

**5. [CHiME-6](https://www.openslr.org/150/)**
- Dinner parties in homes with multiple arrays (from memory); the training archive alone is 97 GB.
- Share-alike applies to adapted material, and whether a trained model counts is unsettled, so ask counsel before training a shipped model on it.
- **Paper:** [CHiME-7 DASR](https://doi.org/10.21437/chime.2023-1) (2023), which also uses DiPCo.

**6. [Earnings-21](https://github.com/revdotcom/speech-datasets)**
- 39 hours of earnings calls: real business vocabulary and long recordings, but call audio. Speaker labels are from memory. The same share-alike caveat applies.

**7. LDC: [ISL Meeting Speech](https://catalog.ldc.upenn.edu/LDC2004S05), [NIST Meeting Pilot](https://catalog.ldc.upenn.edu/LDC2004S09)**
- Commercial use requires [for-profit membership](https://www.ldc.upenn.edu/data-management/using/licensing); a search result put it at about $24,000 a year, which I did not confirm.
- Poor value for these small, old corpora unless you want other LDC data too.

**8. [Nexdata 172 h](https://www.nexdata.ai/datasets/speechrecog/1770)**
- "Paid dataset licensed for commercial use" with timestamps and speaker IDs, but smartphone-recorded prompted dialogues. It adds speaker variety, not meeting acoustics.

## Known, not confirmed
- **CHIL evaluation packages (ELRA):** seminar and meeting recordings with arrays. Search snippets show a commercial licence at several thousand euros, but the [ELRA catalogue](https://catalogue.elra.info/en-us/repository/browse/ELRA-E0017/) timed out today, so content and price are unverified.

## Not recommended, and why
- **MeetingBank:** CC BY-NC-SA, so non-commercial.
- **[MagicData English open sample](https://magichub.com/datasets/multi-stream-spontaneous-conversation-training-datasets_english/):** CC BY-NC-ND; the commercial version is by quote and is not far-field.
- **VoxConverse:** offered "for research purposes", built on YouTube audio, and not meetings.
- **LibriCSS:** read speech replayed in a room, not real conversation.
- **AliMeeting / AISHELL-4:** Mandarin.
- **DIHARD III / Mixer 6:** LDC terms, and not meetings.

## What I could not find
- No large commercially licensed corpus of real English far-field business meetings, either open or off the shelf.
- Searches of Defined.ai, Appen, Shaip and Nexdata showed no such product; they offer custom collection instead.

## Next step
1. Download AMI, NOTSOFAR-1 and ICSI today, and hold out NOTSOFAR-1 as your most realistic test set.
2. If that is not enough, the realistic paid route is a custom collection from a vendor, or your own recordings with consent, in your target rooms and devices.
3. Ask counsel about speaker consent and voice-data privacy; a CC licence covers copyright only.

The interactive shortlist is at `/private/tmp/e-0XYr2E/home/cwd/dataset-shortlist.html`.