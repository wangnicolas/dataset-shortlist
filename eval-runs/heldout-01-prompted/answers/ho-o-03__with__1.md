## Recommendation

For a commercial product, start with **AMI**, then add **NOTSOFAR-1** and **DiPCo**. Skip ICSI unless you're prepared to confirm its licence with Edinburgh or LDC.

Every licence below is the dataset owner's published statement. I haven't had a lawyer read them, so have someone do that before you ship.

### 1. AMI Meeting Corpus: the core set
- **What it is:** about 100 hours of real English meetings. They include scenario meetings, where participants play assigned roles, and natural ones. Audio comes from individual headsets and lapel mics, plus two table-top microphone arrays (8 channels each).
- **Licence:** CC BY 4.0, which allows commercial use with attribution. The [licence page](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml) says "The AMI corpus and its annotations" are CC BY 4.0. The [download page](https://groups.inf.ed.ac.uk/ami/download/) says both annotation zips were relicensed to CC BY 4.0 in April 2017. Other pages still say "some annotations", so I couldn't fully close that gap.
- **Access:** free. You pick meetings and streams on the [download page](https://groups.inf.ed.ac.uk/ami/download/). The array audio is about 360 MB per meeting. It is also mirrored on [OpenSLR (SLR16)](https://www.openslr.org/resources.php), but OpenSLR's page states no licence, so use the Edinburgh licence.
- **Caveats:**
  - Annotations are in NXT format, and the download page doesn't spell out diarization or word timing. Check the annotation documentation for speaker segments before relying on them. Existing AMI RTTM files used in diarization toolkits are derived from these annotations.
  - Treat Hugging Face mirrors with caution. One lists AMI as "non-commercial", which contradicts Edinburgh's licence.
  - Many scenario meetings are role-played, so the content is less spontaneous than real business meetings.

### 2. NOTSOFAR-1 (Microsoft): real far-field meetings
- **What it is:** [recorded meetings](https://github.com/microsoft/NOTSOFAR1-Challenge), 237 of them at about 6 minutes each. That's roughly 24 hours, by my own estimate. They were recorded in 30 conference rooms with 4–8 attendees and 35 unique speakers, on both multi-channel array devices and single-channel devices. The ~1,000 hours of simulated training data in the same release is synthetic, so leave it out given your real-recordings requirement.
- **Licence:** CC BY 4.0, per the repo.
- **Access:** free. Create a Hugging Face token, set `HF_TOKEN`, and use the download helpers in `utils/notsofar_dataset.py`.
- **Caveat:** the page doesn't describe the speaker-turn annotation format. It says ground truth is available for the eval sets and that transcript upgrades are underway for train and dev. Check the annotation coverage per split before you plan around it.

### 3. DiPCo (Amazon): small but properly far-field
- **What it is:** [10 dinner-party sessions](https://zenodo.org/records/8122551) of 15–45 minutes each, with 4 speakers in English. Each speaker has a close-talk mic, and five 7-mic far-field array devices record the room.
- **Licence:** CDLA-Permissive 1.0, which permits commercial use.
- **Access:** open download of a 13.4 GB archive from Zenodo, no login needed.
- **Caveat:** it is casual dinner conversation, not business meetings, and it's small. It is useful as extra far-field data.

### Not recommended, or unresolved
- **ICSI Meeting Corpus:** real research-group meetings with headset and tabletop mics. The licensing is unclear.
  - LDC distributes it under its own agreement, and LDC fees apply for non-members.
  - A Hugging Face card says Edinburgh redistributes it under CC BY 4.0. The [Edinburgh ICSI page](https://groups.inf.ed.ac.uk/ami/icsi/) does say signals, transcription and some annotations are CC BY 4.0.
  - I couldn't find a diarization annotation listed there. The Whipscribe page's claim that it's on OpenSLR as SLR106 is wrong. SLR106 is a West African speech corpus.
  - Write to Edinburgh or LDC to confirm before using it.
- **CHiME-6:** real English dinner parties with far-field arrays, but it is CC BY-SA 4.0. ShareAlike may not fit a commercial model, so ask a lawyer before using it.
- **AliMeeting and AISHELL-4:** Mandarin, and CC BY-SA 4.0, so they fail both of your constraints.
- **Paid vendor data:** The Agentic Data Company sells multi-party English conversations under a commercial licence. The audio isn't recorded on a far-field array. It is mixed down or convolved with a room response to simulate far-field, so it conflicts with your "not simulated" requirement. I didn't verify the vendor beyond its listing.

### Next steps
1. Pull AMI array audio and annotations. Confirm you can derive speaker turns from the annotations.
2. Pull the NOTSOFAR-1 recorded dev/eval sets and check the annotation format.
3. Keep a record of each licence and attribution requirement. CC BY needs credit, and the AMI page also says no endorsement may be implied.
4. If you need more business-style meeting data, you may need to commission recordings or buy a licence from a vendor that records real meetings. I didn't find a public dataset that does this.

Sources:
- [AMI licence](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [AMI download](https://groups.inf.ed.ac.uk/ami/download/)
- [AMI and ICSI Corpora](https://groups.inf.ed.ac.uk/ami/)
- [ICSI at Edinburgh](https://groups.inf.ed.ac.uk/ami/icsi/)
- [NOTSOFAR-1 repo](https://github.com/microsoft/NOTSOFAR1-Challenge)
- [DiPCo on Zenodo](https://zenodo.org/records/8122551)
- [OpenSLR resources](https://www.openslr.org/resources.php)
- [LDC ICSI transcripts](https://catalog.ldc.upenn.edu/LDC2004T04)
- [Spirelight meeting dataset comparison](https://www.spirelight.ai/guides/meeting-speech-datasets)
- [DiariZen licence issue](https://github.com/BUTSpeechFIT/DiariZen/issues/32)
- [The Agentic Data Company](https://theagenticdatacompany.com/datasets/multi-party-conversations)