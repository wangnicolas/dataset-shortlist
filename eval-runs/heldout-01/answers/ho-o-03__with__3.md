## What I assumed you need

- **R1 (must):** real, not simulated, multi-party English conversation.
- **R2 (must):** who-spoke-when annotations.
- **R3 (must):** commercial use allowed. A paid licence is fine; research-only and non-commercial data is out.
- **R4 (nice to have):** business-style meetings.
- **R5 (nice to have):** far-field or microphone-array audio.

I checked on 2026-11-12. The literature search returned nothing useful, so the list comes from the registries plus what I already knew.

## Shortlist

| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | NOTSOFAR-1 recorded meetings (Microsoft) | Direct download, minutes | CC BY 4.0 per the GitHub repo; the Hugging Face record states none | Strong | Partly: repo licence read today, Hugging Face licence missing |
| 2 | AMI Meeting Corpus | Direct download, minutes | CC BY 4.0 | Strong, but scenario-driven | Today |
| 3 | DiPCo (Dinner Party Corpus) | Direct download, minutes | CDLA-Permissive-1.0 | Partial: informal setting | Today |
| 4 | ICSI Meeting Speech and Transcripts (LDC) | LDC account and fee, days | LDC non-member agreement | Partial, commercial terms unconfirmed | Today |

## Details

**1. NOTSOFAR-1** ([GitHub](https://github.com/microsoft/NOTSOFAR1-Challenge), [Hugging Face](https://huggingface.co/datasets/microsoft/NOTSOFAR))
- **Content:** real meetings in office conference rooms, recorded with several multi-microphone array devices and single-channel devices. It was built for a distant diarization and ASR challenge.
- **Real versus simulated:** the dataset also includes a roughly 1,000-hour simulated training set. Use only the recorded-meeting part to meet R1.
- **Licence:** the repo says "MIT, CC-BY-4.0 licenses found", but the Hugging Face record shows no licence. I believe the data is CC BY 4.0, but that is from memory. Get it in writing before you rely on it.
- **Business fit (R4, from memory):** office-style meetings, but participants were given topics.
- **Access:** use the `download_meeting_subset` function in the repo.

**2. AMI** ([site](https://groups.inf.ed.ac.uk/ami/corpus/))
- **Content:** 100 hours with close-talk and far-field array microphones, and speaker-attributed annotations.
- **Licence:** the official licence page says "released under the Creative Commons Attribution 4.0 license". The OpenSLR mirror still lists the old non-commercial CC BY-NC-SA 2.0 licence. Treat the official AMI site as authoritative, and keep a copy of the page in your records.
- **Caveats:** about two-thirds of AMI is role-play, with participants acting as a design team. The rest is naturally occurring meetings. It is also heavily used, so many off-the-shelf models are already tuned to it.

**3. DiPCo** ([Zenodo](https://zenodo.org/records/8122551))
- **Content:** four Amazon employees having a natural conversation, recorded by five 7-microphone far-field arrays, with human-labelled transcripts.
- **Caveats:** it is small and set at a dinner party, not a meeting. It is useful for far-field robustness, not for business-meeting style.

**4. ICSI Meeting Corpus** ([speech LDC2004S02](https://catalog.ldc.upenn.edu/LDC2004S02), [transcripts LDC2004T04](https://doi.org/10.35111/0sq8-s977))
- **Content:** real research-group meetings with tabletop microphones.
- **Access:** create an LDC account, pay the fee, and ask LDC explicitly about commercial use. The page lists the "LDC User Agreement for Non-Members" but I couldn't read the agreement text.
- **From memory:** ICSI may also host a CC BY 4.0 release. I couldn't reach the ICSI site to confirm.

## Known, not confirmed

- **CHiME-5/6:** real far-field dinner-party data. The official page says "available under licence", and I couldn't confirm the terms. A Hugging Face mirror shows CC BY-SA, but a mirror doesn't set the original terms.
- **Paid vendors** such as Defined.ai, Appen, Speechocean and Nexdata sell licensed multi-speaker English meeting data. I didn't check them. This is probably your best route to business-style, far-field data with a clean commercial licence.

## Not recommended, and why

- **MeetingBank audio:** CC BY-NC-SA 4.0.
- **ground-truth/multichannel-meetings-10h:** CC BY-NC 4.0.
- **VoxConverse:** the official site doesn't distribute the audio. It is single-channel YouTube material and not meetings.
- **DIHARD I/II (LDC):** mixed sources rather than meetings, and the commercial terms are unconfirmed.
- **Hugging Face "synthetic" and "simulation" diarization sets:** these are simulated, which fails R1.

## What I could not find

- No large business-meeting corpus with an explicit commercial licence beyond AMI and NOTSOFAR.
- Hugging Face registry search partly failed because the response was too large.

## Next step

1. Start with AMI and NOTSOFAR-1 today, since both are downloadable now.
2. Email Microsoft or check the NOTSOFAR LICENSE files to settle the data licence.
3. Ask LDC about commercial terms for ICSI.
4. Request a quote from a vendor for business-style far-field data. Public sets are modest in size and style.

Page: `/private/tmp/e-b3LFWs/home/cwd/dataset-shortlist.html`