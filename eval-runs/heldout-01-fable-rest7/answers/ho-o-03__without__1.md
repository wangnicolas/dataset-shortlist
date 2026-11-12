**Start with AMI, ICSI and NOTSOFAR-1.** All three are real recorded English meetings with speaker-turn annotations, and all are CC BY 4.0, which allows commercial use with attribution and no fee. I checked the licences on the official pages today, except where noted below.

| Corpus | What it is | Far-field / array | Licence | Caveats |
|---|---|---|---|---|
| **[AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/corpus/)** | 100 h of meetings, with word-level transcripts and speaker segments | Yes: microphone arrays plus headset and lapel mics | CC BY 4.0 | About two-thirds are scenario meetings (role-played design-team projects, though genuinely recorded); many non-native speakers |
| **[ICSI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/icsi/)** | About 70 h of naturally occurring research-group meetings | Partly: a few distant tabletop mics (from memory, not a proper array), plus close-talk | CC BY 4.0 | Technical/academic content; early-2000s recordings |
| **[NOTSOFAR-1](https://github.com/microsoft/NOTSOFAR1-Challenge)** (Microsoft) | Roughly 240–315 short meetings (about 6 min each), 4–8 attendees, about 30 conference rooms | Yes: commercial far-field array devices, plus close-talk references | CC BY 4.0 per the GitHub repo and [Hugging Face card](https://huggingface.co/datasets/microsoft/NOTSOFAR) | Only about 35 unique speakers; one dev subset is flagged challenge-only |

NOTSOFAR-1 is the closest match to modern conference-room audio, but confirm its licence before you rely on it. The [CHiME-8 data page](https://www.chimechallenge.org/challenges/chime8/task2/data) still carries older challenge-only wording, and I did not open the licence file in the repo itself.

**Useful supplements, but not business meetings:**
- **[DiPCo](https://zenodo.org/records/8122551)** (Amazon): about 5 h across 10 dinner-party sessions of 4 speakers, with five 7-mic far-field arrays plus close-talk. It is CDLA-Permissive 1.0, so commercial use is fine, and it works well as a held-out far-field test set.
- **[CHiME-6](https://www.openslr.org/150/)**: real dinner parties recorded on multiple far-field arrays, with heavy overlap and noise. It is CC BY-SA 4.0, which allows commercial use, but have counsel look at the ShareAlike clause before training shipped models on it.

**If you need more or closer-matched data, these are the paid routes:**
- **LDC**: it holds the NIST meeting sets and conversational telephone corpora (Fisher, Switchboard, CALLHOME). Commercial rights generally require a for-profit membership, and terms vary by corpus, so check each agreement.
- **Commercial vendors** (Appen, Defined.ai, Datatang, Shaip and similar): they sell off-the-shelf or custom-collected meeting recordings with diarization labels. I have not checked their current catalogues or prices.

**What I'd avoid:**
- **VoxConverse** and other YouTube-derived sets: the annotations are openly licensed, but the underlying audio rights are not cleared.
- **LibriCSS**: it is replayed mixtures, not real conversations.
- **AliMeeting and AISHELL-4**: both are Mandarin.

Public data alone won't cover your speaker and room diversity, since AMI and ICSI come from a handful of rooms and NOTSOFAR-1 has few speakers. I'd train on those three and build a small in-domain evaluation set from your own consented recordings as early as you can.

Sources:
- [AMI Corpus](https://groups.inf.ed.ac.uk/ami/corpus/)
- [ICSI Corpus](https://groups.inf.ed.ac.uk/ami/icsi/)
- [NOTSOFAR-1 GitHub](https://github.com/microsoft/NOTSOFAR1-Challenge)
- [NOTSOFAR on Hugging Face](https://huggingface.co/datasets/microsoft/NOTSOFAR)
- [NOTSOFAR-1 paper](https://arxiv.org/abs/2401.08887)
- [CHiME-8 Task 2 data page](https://www.chimechallenge.org/challenges/chime8/task2/data)
- [CHiME-6 on OpenSLR](https://www.openslr.org/150/)
- [DiPCo on Zenodo](https://zenodo.org/records/8122551)
- [DiPCo paper](https://arxiv.org/pdf/1909.13447)