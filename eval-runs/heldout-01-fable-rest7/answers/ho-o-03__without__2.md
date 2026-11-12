**Use the AMI Meeting Corpus as your core dataset, and add ICSI and NOTSOFAR-1.** All three are real recorded English meetings with speaker-turn annotations and far-field audio, and all are CC BY 4.0, which allows commercial use with attribution and no fee.

I checked the licence pages for AMI, ICSI, NOTSOFAR-1 and CHiME-6 today. The DiPCo licence and the LDC terms come from search results, and the corpus sizes for AMI, DiPCo and CHiME-6 are from memory.

| Dataset | What it is | Far-field audio | Licence |
|---|---|---|---|
| **AMI** | About 100 h of 4-person meetings; roughly two-thirds are role-played design-team scenarios, the rest natural meetings | 8-mic circular arrays, plus headset and lapel mics | CC BY 4.0 |
| **ICSI Meeting Corpus** | About 72 h across 75 natural research-group meetings, 53 speakers | Tabletop distant mics plus headsets | CC BY 4.0 |
| **NOTSOFAR-1** (Microsoft) | 237 short meetings (about 6 min each), 4–8 attendees, 30 conference rooms | Multi-channel and single-channel commercial meeting devices | CC BY 4.0 |
| **DiPCo** (Amazon) | About 5 h of 4-person dinner-party conversation | Multiple 7-mic arrays plus close-talk | CDLA-Permissive 1.0 |
| **CHiME-6** | About 40 h of 4-person dinner parties in real homes | Multiple Kinect arrays | CC BY-SA 4.0 |

- **AMI:** this is the closest match to business meetings and the standard diarization benchmark. The scenario meetings are acted, but they are real people talking in a real room, not simulated mixtures. Many speakers are non-native English speakers.
- **ICSI:** these are fully natural meetings with heavy overlap, but they are academic discussions, not business ones. Get it from the Edinburgh site; the LDC copy comes under LDC's own terms.
- **NOTSOFAR-1:** this is the most product-like acoustically, since it was recorded on actual conference-room devices. Two cautions:
  - The README says the data is "provided for open research" alongside the CC BY 4.0 grant. The licence itself has no non-commercial clause, but have counsel confirm.
  - Dev-set-2 is approved for the challenge only, so do not use it.
- **DiPCo and CHiME-6:** these are not meetings, but they add far-field robustness. The ShareAlike clause on CHiME-6 applies to derivatives of the data; whether that reaches trained models is unsettled, so get a legal view before training on it.

**What to avoid**
- **VoxConverse:** the annotations are CC BY, but the audio is YouTube video you would have no rights to.
- **LibriCSS:** it is replayed mixtures, not real conversation.
- **AliMeeting and AISHELL-4:** these are Mandarin.
- **LDC corpora (NIST RT sets, DIHARD, CALLHOME):** commercial use requires for-profit LDC membership at the time you obtain the data, and corpus-specific agreements can still override that. I'd only go this route if you need the NIST RT meeting sets for evaluation.

One thing the licences do not cover is privacy. CC BY settles copyright, but these are recordings of identifiable voices. If you operate in the EU or under biometric-privacy laws, check the consent basis for each corpus.

Sources:
- [AMI corpus licence](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [ICSI corpus licence](https://groups.inf.ed.ac.uk/ami/icsi/license.shtml)
- [NOTSOFAR-1 Challenge repo](https://github.com/microsoft/NOTSOFAR1-Challenge)
- [CHiME-8 Task 2 data page](https://www.chimechallenge.org/challenges/chime8/task2/data)
- [CHiME-6 on OpenSLR (SLR150)](https://www.openslr.org/150/)
- [DiPCo paper](https://arxiv.org/pdf/1909.13447)
- [Amazon Science DiPCo announcement](https://www.amazon.science/blog/amazon-releases-new-public-data-set-to-help-address-cocktail-party-problem)
- [DiPCo on Hugging Face](https://huggingface.co/datasets/huckiyang/DiPCo)
- [LDC licensing policy](https://www.ldc.upenn.edu/data-management/using/licensing)