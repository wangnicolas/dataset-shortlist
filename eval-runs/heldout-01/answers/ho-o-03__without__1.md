**Short list for commercial use:** NOTSOFAR-1, AMI and ICSI cover your requirements. All three are real conversations with far-field audio, speaker annotations and English speech. I'm going from memory, so check each licence on the official page before you commit.

## Core picks

| Corpus | What it is | Far-field / array | Licence (as I recall) |
|---|---|---|---|
| **NOTSOFAR-1** (Microsoft) | About 300 real meetings in office conference rooms, with a range of participant counts and acoustic conditions. It has diarization and transcript annotations. | Yes. It has both single-device and multi-device multichannel recordings. | CC BY 4.0 |
| **AMI Meeting Corpus** | About 100 hours of meetings with headset and 8-channel circular array recordings. It has speaker segmentation and word-level transcripts. | Yes | CC BY 4.0 |
| **ICSI Meeting Corpus** | About 70 hours of naturally occurring research-group meetings. | Tabletop mics plus headsets | I believe CC BY 4.0 now, but confirm. |

- **NOTSOFAR-1** is the closest match to your product and the most recent. It was built for far-field meeting transcription with diarization.
- **AMI** is the standard benchmark, so you can compare your results with published numbers.
  - Roughly two-thirds of it is scenario-driven. Participants play assigned roles in a design team, but the dialogue is unscripted.
  - Many speakers are non-native English speakers, which is useful for robustness.
- **ICSI** is fully natural, but the room is a single setup and the speakers are mostly researchers.

## Smaller or supplementary
- **DiPCo** (Amazon) is about 5 hours of dinner-party conversations recorded with far-field arrays. As I recall it's under a permissive CDLA licence. It's casual rather than business, but it's useful as an extra test set for overlapping speech.
- **LDC meeting corpora** (ISL, NIST meeting room, and similar) are available under LDC licences. LDC has commercial licensing options, and non-members pay fees. This is the "pay a licence fee" route, but the data is old and mostly redundant with AMI and ICSI.

## What to avoid
- **CHiME-6:** I believe its terms are restrictive. Check before using it.
- **VoxConverse, AVA-AVD, MSDWild:** the audio comes from YouTube or film, so the rights are unclear. It's also not far-field meeting audio.
- **LibriCSS and similar:** these are simulated or re-recorded mixtures.
- **Fisher, Switchboard, CallHome:** these are telephone calls, mostly two-party. They're also LDC-licensed.

## Practical notes
1. **Attribution:** CC BY requires credit and a licence notice. It doesn't restrict commercial training or fine-tuning. Keep a data-provenance file listing each source, licence and version.
2. **Consent and privacy:** these corpora were recorded with participant consent, but if you serve EU users, ask counsel about voice data as biometric data.
3. **Size:** about 500 hours total is enough to fine-tune or evaluate diarization models, but not to train one from scratch. Plan on adding your own consented customer or pilot recordings over time.
4. **Evaluation:** hold out NOTSOFAR-1's dev/eval sets and AMI's standard test split so your DER numbers are comparable to published ones.

I can pull up the official licence pages and confirm the exact terms for each one if you'd like.