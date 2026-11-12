I'd build on three datasets that are free and allow commercial use: **AMI**, **NOTSOFAR-1** and **ICSI**. **DiPCo** is a useful extra, and you can pay the LDC for more if you need it. I checked the licences on the official pages today.

## Main picks

| Dataset | What it is | Far-field / arrays | Speaker-turn labels | Licence |
|---|---|---|---|---|
| **AMI Meeting Corpus** | About 100 h of meetings with 3–5 people in instrumented rooms | Yes: two 8-mic circular arrays, plus headset and lapel mics | Yes: speaker segments and word-level timings | **CC BY 4.0** ([licence page](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)) |
| **NOTSOFAR-1** (Microsoft) | Real office meetings: 237 public meetings of about 6 min each, recorded in 30 conference rooms | Yes: single-channel and multi-channel commercial meeting devices, which is very close to real deployment conditions | Yes, made for distant diarization and ASR | **CC BY 4.0** ([repo](https://github.com/microsoft/NOTSOFAR1-Challenge)) |
| **ICSI Meeting Corpus** | About 72 h of the institute's own research meetings, not scripted | Tabletop distant mics (PZM and cheap desktop mics), plus close-talk mics | Yes: speaker-attributed transcripts with timings | **CC BY 4.0** through Edinburgh ([licence page](https://groups.inf.ed.ac.uk/ami/icsi/license.shtml)) |
| **DiPCo** (Amazon/JHU) | 10 dinner-party sessions with 4 people each, 15–45 min | Yes: five 7-mic far-field arrays | Yes | **CDLA-Permissive 1.0** ([Zenodo](https://zenodo.org/records/8122551), the official copy now) |

**Things to watch for with each:**
- **AMI:** About two-thirds of the meetings are "scenario" meetings. These are real live conversations between real people, not mixtures, but the participants role-play a design team. The rest are natural meetings. Many speakers are non-native English speakers. That helps make the model robust, but keep it in mind when you build your test sets.
- **NOTSOFAR-1:** The licence is CC BY 4.0, but the repo also says the data is "provided for open research." That line doesn't add a formal restriction, but it's ambiguous enough that you should ask Microsoft for written confirmation before shipping. Also, Dev-set-2 is limited to use within the challenge, so leave it out.
- **ICSI:** The meetings are academic research meetings, so they're not quite business meetings, but they are natural and unscripted. Get it from the Edinburgh distribution, which is the CC BY one, not an older copy.
- **DiPCo:** It's social conversation, not business, and it's small. It's still good for training on hard far-field overlap.

Taken together, this gives you roughly 180 h or more of real, multi-party, far-field English, all with commercial-use licences. NOTSOFAR is the one most like your production setting, so I'd use part of it as your main evaluation set.

## Paid options

- **LDC for-profit membership or per-corpus commercial licence:** This covers the NIST Rich Transcription meeting evaluation sets (RT-02 to RT-09, which are multi-site meetings with distant mics and diarization references) and Mixer 6 (2-person interviews, multi-mic far-field). You get standard benchmarks with commercial terms.
- **Data vendors** such as Appen, Defined.ai and Shaip: they sell or custom-record meeting audio with commercial licences and participant consent. This is the way to get real business meetings at scale if the public data isn't enough.

## Leave these out

- **CHiME-5 / CHiME-6:** non-commercial licence. Watch for CHiME-7/8 DASR bundles too: they mix CHiME-6, which is non-commercial, with DiPCo and Mixer 6.
- **AliMeeting, AISHELL-4:** Mandarin.
- **LibriCSS:** replayed and simulated mixtures.
- **Ego4D, MSDWild:** non-commercial or research-only terms.
- **VoxConverse and other YouTube-derived sets:** CC BY covers the labels, but the rights to the underlying audio are unclear.

## Practical notes

1. **Download from the official sources.** Hugging Face mirrors sometimes show the wrong licence. For example, one NOTSOFAR-derived dataset is tagged CC BY-NC.
2. **CC BY and CDLA-Permissive require attribution.** Keep a record of which datasets you used and credit them, for instance in your docs or a NOTICE file.
3. **Have a lawyer look at it quickly.** I'm not a lawyer. The licences above are clear on paper, but someone should check how they apply to your product, for example to trained model weights and to any participant-consent or privacy questions.

Sources:
- [AMI licence](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [ICSI licence](https://groups.inf.ed.ac.uk/ami/icsi/license.shtml)
- [NOTSOFAR-1 repo](https://github.com/microsoft/NOTSOFAR1-Challenge)
- [NOTSOFAR-1 paper](https://arxiv.org/html/2401.08887v1)
- [NSF-QA derived dataset (licence tagging example)](https://huggingface.co/datasets/popcornell/NSF-QA)
- [DiPCo on Zenodo](https://zenodo.org/records/8122551)
- [DiPCo paper](https://www.isca-archive.org/interspeech_2020/segbroeck20_interspeech.pdf)
- [Amazon DiPCo announcement](https://www.amazon.science/blog/amazon-releases-new-public-data-set-to-help-address-cocktail-party-problem)