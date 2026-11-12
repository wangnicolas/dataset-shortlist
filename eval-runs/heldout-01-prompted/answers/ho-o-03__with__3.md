**Short answer: use the AMI Meeting Corpus.** It is the only dataset I found that meets all your requirements. Add ICSI as a smaller secondary option if you want more data.

## 1. AMI Meeting Corpus (recommended)

- **What it is:** About 100 hours of real English meetings with 3–5 participants. Many are scenario-driven design-team meetings, which means participants were role-playing a scenario. The rest are naturally occurring meetings. Most speakers are non-native.
- **Audio:** Individual headsets, a headset mix, and far-field audio from table-top microphone arrays. (The AMI download page lists the array audio as coming from two table-top arrays.)
- **Annotations:** Manual annotations are NXT XML, which includes word- and segment-level speaker timing. The download page doesn't mention RTTM files, so you would derive turn boundaries yourself.
- **Licence:** The Edinburgh licence page says "the AMI corpus and its annotations are released under the Creative Commons Attribution 4.0 license". CC BY 4.0 allows commercial use with attribution. The download page is narrower. It says the signals, the transcription and *some* annotations are CC BY 4.0, and it gives no licence for the DOME and social-role annotation sets. I did not find a list of exactly which annotations are covered. The manual and automatic annotation zips are stated to be CC BY 4.0.
- **Access:** Free download from the [AMI download page](https://groups.inf.ed.ac.uk/ami/download/). You select meetings and audio streams there, then unzip the annotation archives next to the signals.
- **Easier route for diarization:** [diarizers-community/ami on Hugging Face](https://huggingface.co/datasets/diarizers-community/ami) is listed as CC-BY-4.0. It is about 21 GB of Parquet, with `timestamps_start`, `timestamps_end` and `speakers` fields. It loads with `load_dataset("diarizers-community/ami", "ihm")`. The page doesn't define the "ihm" and "sdm" subsets. I'd expect "ihm" to be headset and "sdm" to be a single distant microphone, but that is my assumption. For multichannel array audio, use the original download.

The upstream licence is clear, but I'd still keep a copy of the licence pages and the date you downloaded. Also check the Hugging Face copy against the original before you rely on it.

## 2. ICSI Meeting Corpus (secondary)

- **What it is:** About 70 hours of real research-group meetings. The recordings are close-talking microphones, available as separate SPH files or one mixed WAV. The Edinburgh page doesn't mention table-top microphones, so don't count on far-field audio from it.
- **Licence:** The [Edinburgh ICSI page](https://groups.inf.ed.ac.uk/ami/icsi/) says signals, transcription and some annotations are CC BY 4.0.
- **Caveat:** The same corpus is also sold through the LDC under terms that bar non-member for-profit organisations from commercial development. Use the Edinburgh copy, not the LDC one.

## What I ruled out

- **NOTSOFAR-1:** Real far-field array recordings, but a secondary source says it is CC BY-NC-ND. I did not check this myself, and I would confirm it before you spend time on it. If it is correct, it fails your commercial-use requirement.
- **LibriCSS:** The audio is played back through loudspeakers, not recorded in real meetings, so it doesn't fit.
- **CHiME-6:** English dinner-party conversations, not business meetings. I couldn't confirm its licence, so I wouldn't use it.
- **AliMeeting and LOTUSDIS:** Mandarin and Thai respectively, so they fail the English-only requirement.

## Mistakes in what I found

- One search result suggested that OpenSLR 106 was a CC-BY copy of ICSI. I checked, and it is a West African speech corpus under CC BY-SA 4.0. It has nothing to do with ICSI.
- A Hugging Face card (knkarthick/AMI) labels AMI "non-commercial licence: cc-by-4.0". That is self-contradictory and conflicts with Edinburgh's own terms. It looks like a third-party mislabel.

## Caveats

- **Domain gap:** AMI is a modest amount of data, with mostly scripted scenarios and one room set-up per site. For a commercial product, expect to need more in-domain data, and AMI will probably work better for evaluation than for training alone.
- **Paid options:** I did not find a commercially licensable real-meeting English corpus with array audio beyond AMI. You could commission recordings or negotiate with a data vendor. I haven't researched specific vendors.
- **Pretrained models:** If you fine-tune or ship pretrained diarization models, check their training-data licences too. A DiariZen maintainer noted that a checkpoint inherited non-commercial restrictions from other datasets in its training mix.

Sources:
- [AMI download page](https://groups.inf.ed.ac.uk/ami/download/)
- [AMI licence page](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [AMI corpus page](https://groups.inf.ed.ac.uk/ami/corpus/)
- [ICSI at Edinburgh](https://groups.inf.ed.ac.uk/ami/icsi/)
- [diarizers-community/ami](https://huggingface.co/datasets/diarizers-community/ami)
- [OpenSLR 106](https://www.openslr.org/106/)
- [LDC licensing](https://www.ldc.upenn.edu/data-management/using/licensing)
- [DiariZen licence issue](https://github.com/BUTSpeechFIT/DiariZen/issues/32)
- [Meeting speech datasets comparison (Spirelight)](https://www.spirelight.ai/guides/meeting-speech-datasets)