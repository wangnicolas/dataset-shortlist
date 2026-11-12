I'd use three datasets, all licensed for commercial use and all free: **AMI**, **NOTSOFAR-1** and **ICSI**. **DiPCo** is a small fourth option for extra microphone-array audio.

| Dataset | What it is | Far-field / array audio | Speaker-turn labels | Licence (checked today) |
|---|---|---|---|---|
| **AMI Meeting Corpus** | About 100 h of English meetings, usually 4 people. | Yes: 8-mic circular arrays, plus headset and lapel mics. | Yes: word-level timing with speaker labels. A standard diarization benchmark. | **CC BY 4.0** |
| **NOTSOFAR-1** (Microsoft) | 237 real office meetings (about 6 min each), recorded in 30 conference rooms with 4–8 attendees and 35 speakers. | Yes: several multi-channel array devices and 6–7 single-channel devices per meeting, recorded at once. | Yes, ground truth for train, dev and eval. | **CC BY 4.0** (code is MIT) |
| **ICSI Meeting Corpus** | 75 real research-group meetings, about 72 h, 3–10 people each (6 on average). | Partly: tabletop microphones, but no array. | Yes: speaker-attributed transcripts, plus dialogue-act and topic annotations. | **CC BY 4.0** (free from Edinburgh; LDC also sells the transcripts) |
| **DiPCo** (Amazon) | 10 dinner-party sessions with 4 people each, about 5 h total. | Yes: five 7-mic array devices. | Yes. | **CDLA-Permissive 1.0** |

**Suggested setup:**
- Train on AMI, ICSI and NOTSOFAR together.
- Keep NOTSOFAR's eval set and AMI's standard test split for testing. NOTSOFAR's eval set is the closest match to the conference-room device audio your product will get.
- Use DiPCo for extra array audio, but it is casual conversation, not business meetings.

**Things to watch:**
- **AMI is mostly role-play.** About two-thirds of its meetings are "scenario" meetings, where real people act out a product-design project. The audio is genuinely multi-party, not artificially mixed, but the content is staged. The remaining third are natural meetings. Decide whether the staged part fits what you mean by "real".
- **NOTSOFAR licence details.**
  - Use the Hugging Face / GitHub release (DATA_LICENSE file), which is CC BY 4.0.
  - Don't use **Dev-set-2**. It was taken out of the open release and is limited to the original challenge.
  - An old CHiME-8 page still says the data is challenge-only. It's out of date, but keep a copy of the current DATA_LICENSE in your records.
  - Its roughly 1,000-hour training set is simulated. That's fine for augmentation, but it isn't the real recordings you asked for.
- **Datasets built from these may be stricter.** For example, NSF-QA, derived from NOTSOFAR, is non-commercial. Always get the original release.
- **What CC BY requires and doesn't cover.** You must credit the source. The licence also says it doesn't cover publicity or privacy rights. That's normal, but have a lawyer look at it before you ship models trained on recorded voices.
- **None of these is very large.** If you need more real business-meeting audio, the paid route is custom collection from a data vendor, or for-profit membership of the LDC, which gives access to more meeting data such as the NIST Rich Transcription sets. Check the terms for each LDC corpus yourself.

**Ruled out:** AliMeeting is Mandarin, and LibriCSS is replayed audio rather than real conversation. CHiME-5/6, Ego4D and Meta's MMCSG have research-only or restricted licences as far as I know, but I didn't re-check those today. VoxConverse is CC BY 4.0 but it's single-channel broadcast audio, so at most a secondary test set.

Sources:
- [AMI licence (CC BY 4.0)](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [AMI & ICSI corpora home](https://groups.inf.ed.ac.uk/ami/)
- [ICSI licence](https://groups.inf.ed.ac.uk/ami/icsi/license.shtml)
- [ICSI download](https://groups.inf.ed.ac.uk/ami/icsi/download/)
- [NOTSOFAR-1 GitHub](https://github.com/microsoft/NOTSOFAR1-CHALLENGE)
- [NOTSOFAR-1 DATA_LICENSE](https://github.com/microsoft/NOTSOFAR1-Challenge/blob/main/DATA_LICENSE)
- [NOTSOFAR on Hugging Face](https://huggingface.co/datasets/microsoft/NOTSOFAR)
- [CHiME-8 Task 2 data page (outdated licence notice)](https://www.chimechallenge.org/challenges/chime8/task2/data)
- [NSF-QA](https://huggingface.co/datasets/popcornell/NSF-QA)
- [DiPCo on Zenodo](https://zenodo.org/records/8122551)
- [Amazon DiPCo announcement](https://www.amazon.science/blog/amazon-releases-new-public-data-set-to-help-address-cocktail-party-problem)
- [DiPCo paper](https://arxiv.org/pdf/1909.13447)