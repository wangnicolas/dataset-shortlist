## What I assumed you need
- **Must-have:** real meetings (not simulated), speaker-turn labels, English, and a licence that allows commercial use.
- **Nice-to-have:** far-field or microphone-array audio, and business-style meetings.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NOTSOFAR-1 (Microsoft, CHiME-8) | Free download, minutes | CC BY 4.0 (GitHub), dataset-card licence unconfirmed | Real dev/eval meetings, plus a ~1000 h simulated training set | Strong | Access today. Licence partly. |
| 2 | AMI Meeting Corpus | Free download, minutes | CC BY 4.0 | ~100 h | Strong | Licence today |
| 3 | ICSI Meeting Corpus | Free download, minutes | CC BY 4.0 | ~70 h | Partial | Licence today |
| 4 | DiPCo (Amazon) | Free download on Zenodo | CDLA-Permissive-1.0 | Small | Partial | Today |
| 5 | NIST Rich Transcription sets (LDC) | Fee through LDC, weeks | LDC agreement, commercial terms unknown | Small | Partial | Today, fee only |

## Details
- **NOTSOFAR-1:**
  - **Links:** [repo](https://github.com/microsoft/NOTSOFAR1-Challenge) and [Hugging Face](https://huggingface.co/datasets/microsoft/NOTSOFAR). The Hugging Face dataset is not gated.
  - **What it contains:** real meetings recorded on multi-channel array devices, built for distant diarization plus ASR. The paper is "NOTSOFAR-1 Challenge: New Datasets, Baseline, and Tasks for Distant Meeting Transcription" (2024).
  - **Licence:** GitHub shows "MIT, CC-BY-4.0 licenses found", but the registry gave no licence for the data. Check the dataset card before you ship.
  - **Caution:** the ~1000 h training set is simulated, so use only the recorded-meeting subsets for your real-data requirement.
  - **Recalled, not confirmed:** office-style meetings.
- **AMI:**
  - **What it contains:** the standard benchmark. The [licence page](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml) says the corpus and annotations are "released under the Creative Commons Attribution 4.0 license". Array and headset audio, and the design-team meetings, are from memory.
  - **Caution:** about half the meetings are acted scenarios, and it is small and heavily studied.
- **ICSI:**
  - **What it contains:** real research-group meetings. The [page](https://groups.inf.ed.ac.uk/ami/icsi/) says the signals, transcripts and some annotations were released under CC BY 4.0. The page describes close-talking microphones. Table-top far-field mics are from memory.
  - **Caution:** the meetings are academic, not business.
- **DiPCo:**
  - **What it contains:** real four-person conversations captured by five 7-mic far-field arrays.
  - **Caution:** it is a dinner-party setting, so it fits your array need but not "business meetings".
- **NIST RT / LDC:**
  - **What it contains:** classic meeting evaluation sets, with a per-corpus LDC fee (the LDC page says "Login for the applicable fee").
  - **Caution:** LDC non-member terms are often research-oriented, so ask LDC in writing about commercial use. I couldn't confirm this.

## Known, not confirmed
- **CHiME-6 / CHiME-5:** the data page returned 404. From memory the licence is non-commercial, so treat it as excluded unless you confirm otherwise.

## Not recommended
- **MeetingBank:** CC BY-NC-SA, and it is city-council data.
- **ground-truth/multichannel-meetings-10h:** CC BY-NC.
- **DIHARD (LDC):** mixed domains and a fee, not meeting-focused.

## What I could not find
No large, commercially licensed corpus of real business meetings with far-field audio exists in what I searched. The Hugging Face search partly failed, and the registries returned a lot of noise. For production-scale data you would likely need to record and license your own, or negotiate with a commercial speech-data vendor.

## Next step
Start with NOTSOFAR-1's real-meeting subsets and AMI today, and confirm the NOTSOFAR dataset-card licence. Checked 2026-11-11 and 2026-11-12. Interactive page: `dataset-shortlist.html`.