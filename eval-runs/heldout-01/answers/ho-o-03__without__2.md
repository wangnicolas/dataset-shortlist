**Recommendation:** start with NOTSOFAR-1, AMI and ICSI. All three are real recorded meetings, and all three have been released under CC BY 4.0, which permits commercial use with attribution. I'm going from memory and haven't checked the licence pages just now. Before you commit, read the current licence text on each distribution page and save a copy for your records.

| Corpus | What it is | Far-field | Licence | Fit |
|---|---|---|---|---|
| **NOTSOFAR-1** (Microsoft, CHiME-8 task 2) | About 280 real, unscripted office-style meetings with 4–8 participants. It has speaker-attributed transcripts and diarization labels. | Yes, multiple commercial devices, including single-mic and multi-mic arrays. | CC BY 4.0 | Best match for a business-meeting product. |
| **AMI** | About 100 hours of meetings with headset, lapel and 8-channel circular-array audio. It has word-level and speaker-segment annotations. | Yes | CC BY 4.0 | The standard diarization benchmark. |
| **ICSI Meeting Corpus** | About 70 hours of natural meetings of research groups, recorded with headsets and tabletop mics. | Yes, tabletop mics | CC BY 4.0 | Good for natural overlap and interruption behaviour. |

**Caveats**
- **NOTSOFAR-1:** use only the real recorded meeting sets. Its training data also includes a large simulated portion, which you said you don't want.
- **AMI:** about two thirds of the meetings are scenario-based. Participants role-play a design team, so the speech is real but the topics are staged. Many speakers are non-native English speakers, which is useful for robustness but not representative of every market.
- **ICSI:** the meetings are academic, not corporate. The content is technical and the speaker pool is small, so don't rely on it alone.
- **Check the annotation licence separately.** Where audio and annotations are distributed separately, confirm that both are covered.

**Datasets to skip**
- **LibriCSS:** the mixtures are played back through speakers, so they aren't real conversations.
- **CHiME-5/6:** dinner-party recordings with research-only terms.
- **DIHARD and VoxConverse:** the audio is mostly not meeting-style, and the rights status is murky (YouTube-sourced audio for VoxConverse, LDC terms for DIHARD).
- **AliMeeting and MISP:** not English.

**Paid options for more data**
- **LDC** sells commercial licences for some meeting corpora, including the NIST rich-transcription meeting sets. Terms vary by corpus, so ask them directly.
- **Defined.ai, Appen, Speechocean and Datatang** sell English multi-party far-field meeting data with commercial terms. You can also commission custom collection that matches your target acoustics, such as conference rooms, laptops and speakerphones.

A practical plan is to train and evaluate on NOTSOFAR-1, AMI and ICSI. Then, if domain mismatch shows up, buy or collect a few dozen hours of in-domain meetings. Hold out whole meetings, and ideally whole speakers, for evaluation. AMI and ICSI recur across published benchmarks, so keep their official splits if you want your numbers to be comparable.

I can check the current licence pages and download terms for each of these if you'd like.