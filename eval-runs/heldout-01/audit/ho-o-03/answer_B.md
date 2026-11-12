## What I assumed you need
- **Must-haves:** real (non-simulated) English multi-party meetings, speaker-turn annotations, and a licence that permits commercial use. A paid licence is fine.
- **Nice-to-haves:** far-field or microphone-array audio, and business-style content.

## Shortlist

| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | **AMI Meeting Corpus** | Direct download, minutes | CC BY 4.0, commercial use OK | Strong | Licence and download page read today |
| 2 | **NOTSOFAR-1** (recorded meetings) | Download via the repo or Hugging Face, minutes | CC BY 4.0 per the GitHub banner; the dataset page shows none | Strong, pending licence check | Partly today |
| 3 | **ICSI Meeting Speech and Transcripts** (LDC2004S02, LDC2004T04) | Paid LDC order, days | LDC user agreement; commercial terms not read | Good, pending licence check | LDC pages seen today |
| 4 | **DiPCo** | Zenodo download | CDLA-Permissive-1.0 | Weak | Registry record confirmed today |

## Details
- **AMI** (https://groups.inf.ed.ac.uk/ami/corpus/)
  - It has about 100 hours of meetings recorded with an 8-channel circular array plus headset mics. The manual annotations include speaker segments. The array and size details are from memory.
  - The licence page says it "and its annotations are released under the Creative Commons Attribution 4.0 license". You need to give attribution.
  - Roughly two thirds of the meetings are scenario role-play: participants act a design team. The page says "different roles in a design team". The rest are natural meetings. That is the main caveat on "real".
  - Download: https://groups.inf.ed.ac.uk/ami/download/
- **NOTSOFAR-1** (https://github.com/microsoft/NOTSOFAR1-Challenge)
  - It is a Microsoft distant-meeting benchmark with real recorded office meetings and multi-device far-field audio. It is also built for diarization plus transcription. The real-versus-simulated split and the annotation details beyond the repo README are from memory.
  - The repo banner says "MIT, CC-BY-4.0 licenses found", but the Hugging Face record states no licence. Read the dataset card or ask Microsoft before relying on it.
  - It also includes a roughly 1,000-hour simulated training set. Leave that out if you need real audio only.
  - Of everything I found, this is the closest match to your far-field and business-meeting needs. It is also the most recent.
- **ICSI** (https://catalog.ldc.upenn.edu/LDC2004S02)
  - It has about 75 hours of naturally occurring research-group meetings with far-field tabletop microphones, from memory.
  - The LDC page says "Login for the applicable fee". I did not read the non-member agreement's commercial clause, so check that before buying.
  - It is academic group talk rather than business meetings.
- **DiPCo** (https://zenodo.org/records/8122551)
  - It has real far-field array recordings, but of dinner parties, and it is small. Use it only for far-field robustness testing.

## Known, not confirmed
These are from memory and I did not check them this session. Treat each as something to look up, not as a recommendation.
- Other LDC meeting corpora, such as the NIST Rich Transcription meeting sets and ISL. I saw their LDC records but did not read their terms. They are older and mostly overlap with ICSI and AMI.
- ICSI may also be distributed openly outside LDC. I could not confirm that.

## Not recommended, and why
- **MeetingBank audio** is CC BY-NC-SA, so it is non-commercial.
- **ELITR Minuting Corpus** is CC BY-NC-SA.
- **ground-truth/multichannel-meetings-10h** is CC BY-NC.
- **CHiME-6** is dinner parties.
- **AliMeeting and AISHELL-4** are Mandarin.

## What I could not find
- No open, commercial-use corpus of real, unscripted business meetings with far-field audio exists at scale beyond NOTSOFAR-1, so you may eventually need to record your own.
- The literature search returned little useful, and the Hugging Face search partly failed because the response was too large. The list may be incomplete.

## Next step
1. Download AMI today.
2. Confirm NOTSOFAR's data licence in writing, then use its recorded meetings for far-field work.
3. Read the LDC non-member terms before paying for ICSI.
4. Have counsel confirm the CC BY attribution requirements for a commercial product.

