**Recommendation: use AMI as your core dataset. Add DiPCo and CHiME-6 only as secondary sets for far-field robustness. There's no other free English meeting corpus that fits all your criteria.**

## 1. AMI Meeting Corpus (primary)
- **What it is:** About 100 hours of real, non-simulated meetings in English. Roughly two-thirds are scenario-driven, where participants play assigned roles, so they're staged but spoken naturally. The rest are natural meetings. It's the closest match to business-style meetings I found.
- **Audio:** Individual headsets, lapel mics, and a headset mix. The far-field audio comes from two table-top microphone arrays. The official download page lists it as "audio channels from two table-top arrays".
- **Licence:** The [AMI licence page](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml) states that the corpus and its annotations are CC BY 4.0. That licence allows commercial use if you give attribution. The [download page](https://groups.inf.ed.ac.uk/ami/download/) says the manual (v1.6.2) and automatic (v1.5.1) annotation zips were also changed to CC BY 4.0. It adds that some other annotations may not be covered, so check the files you actually use.
- **Access:** Free download from the [AMI download page](https://groups.inf.ed.ac.uk/ami/download/). You pick meetings and audio streams there, and the annotations come as NXT-format zips. I didn't confirm which annotation file carries the speaker segmentation. The [annotation docs](https://groups.inf.ed.ac.uk/ami/corpus/annotation.shtml) should say.
- **Caveats:**
  - A Hugging Face card for `knkarthick/AMI` says "non-commercial". That contradicts the official CC BY 4.0 licence and looks like an error. Rely on the Edinburgh pages and keep a copy of the licence text.
  - Most speakers are non-native English speakers. The recordings are also from 2000s-era rooms, so they're a limited sample of modern conference-call audio.
  - Licences on pretrained models still matter. A pyannote or DiariZen checkpoint trained on mixed data can carry restrictions even though AMI itself is clean.

## 2. DiPCo (secondary, far-field)
- **What it is:** Dinner-party conversations, not meetings. It has 10 sessions of 15–45 minutes, with four people per session. Each person wore a close-talk mic. Five far-field devices with 7-mic arrays were placed around the room.
- **Licence:** CDLA-Permissive 1.0, which allows commercial use. The [Zenodo record](https://zenodo.org/records/8122551), the Interspeech paper and Amazon's release blog all agree.
- **Access:** Free from Zenodo (about 12 GB). The original S3 link has expired.
- **Caveat:** It's small, and the content is casual dinner talk.

## 3. CHiME-6 (secondary, far-field)
- **What it is:** English dinner-party recordings. It has 4 participants per session, recorded on several distant 4-mic Kinect arrays.
- **Licence:** CC BY-SA 4.0, listed on [OpenSLR SLR150](https://www.openslr.org/150/). That allows commercial use, but ShareAlike applies to derivatives. Have a lawyer decide whether your trained models count as derivatives before you use it for a commercial product.
- **Access:** Free from OpenSLR. Training data is about 97 GB, and the JSON transcriptions are a separate file.
- **Caveat:** Its content is domestic and very hard acoustically. It's useful for robustness, but it isn't meeting-like.

## Ruled out or not usable as-is
- **ICSI Meeting Corpus:** The Edinburgh [ICSI page](https://groups.inf.ed.ac.uk/ami/icsi/) says it is CC BY 4.0 for signals, transcription and some annotations. But that page says it was recorded on close-talking microphones. Another source says ICSI is a paid LDC corpus, and the [LDC catalogue entry](https://catalog.ldc.upenn.edu/LDC2004S02) lists the "LDC User Agreement for Non-Members" with the fee behind a login. It does have table-top mics, with about 72 hours across 75 meetings. If you want it, ask LDC about commercial terms. I couldn't see them, and you should confirm which distribution applies.
- **Fisher English:** It's paid LDC data, but it's telephone speech, not meetings or far-field.
- **AliMeeting and AISHELL-4:** These are far-field meeting corpora, but they're Mandarin.

## What I couldn't find
I found no commercially licensed English corpus that has real business meetings, far-field arrays and diarization labels beyond AMI. The paid route would be to ask a data vendor for custom-recorded meetings. I haven't researched specific vendors.

## Suggested next steps
1. Download AMI with the array audio and the manual annotations. Check the licence on the specific annotation files you use.
2. Add DiPCo for extra far-field data.
3. Ask LDC about commercial terms for ICSI, and a lawyer about CHiME-6's ShareAlike clause.
4. Evaluate on AMI. It's the standard benchmark, but your own recordings will tell you more about real-world performance.

Sources:
- [AMI licence](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [AMI download](https://groups.inf.ed.ac.uk/ami/download/)
- [AMI overview](https://groups.inf.ed.ac.uk/ami/corpus/overview.shtml)
- [ICSI at Edinburgh](https://groups.inf.ed.ac.uk/ami/icsi/)
- [ICSI at LDC](https://catalog.ldc.upenn.edu/LDC2004S02)
- [CHiME-6 on OpenSLR](https://www.openslr.org/150/)
- [DiPCo on Zenodo](https://zenodo.org/records/8122551)
- [DiariZen licence issue](https://github.com/BUTSpeechFIT/DiariZen/issues/32)