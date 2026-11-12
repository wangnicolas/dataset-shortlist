I'm working from memory and haven't checked the current licence pages. Confirm each licence at the source before you commit.

## Best fits

**1. NOTSOFAR-1 (Microsoft, 2024)**
- **Content:** About 450 real, unscripted English meetings of office-style conversation, recorded on multi-channel far-field devices (several mic-array form factors) and on single-channel devices.
- **Annotations:** Speaker-attributed transcripts with timing, so you can derive who spoke when. The recordings were made across many rooms with varied acoustics.
- **Licence:** I recall CC BY 4.0, which allows commercial use with attribution.
- **Caveat:** Participants were recruited and given loose topics, so the meetings are natural but not actual company meetings.
- **Fit:** This is the closest match to your brief. I'd start here.

**2. ICSI Meeting Corpus**
- **Content:** About 75 hours of genuinely naturally occurring research-group meetings, with 4–10 speakers each.
- **Audio:** Close-talk headsets plus tabletop far-field mics.
- **Annotations:** Speaker turns and transcripts.
- **Licence:** I recall CC BY 4.0 via the Edinburgh AMI/ICSI hosting.
- **Caveat:** The content is academic and technical, and the recordings are from the early 2000s.

**3. AMI Meeting Corpus**
- **Content:** About 100 hours of English meetings.
- **Audio:** Headsets, lapel mics, and an 8-channel circular far-field array.
- **Annotations:** Speaker turns, words, and more.
- **Licence:** CC BY 4.0, including the audio, as far as I recall.
- **Caveat:** About two-thirds are role-played "design team" scenarios, with the rest natural meetings. Many speakers are non-native English speakers, which may help or hurt depending on your users.
- **Fit:** It is the standard benchmark, so it's useful for comparing your results with published numbers.

## Worth considering, with licence caveats
- **NIST RT evaluation sets, DIHARD, and similar LDC corpora:** Real meeting and conversational speech with diarization labels. LDC licences are per corpus and per membership tier, and commercial use usually needs a for-profit membership or a separate agreement. Ask LDC before relying on them.
- **DiPCo (Amazon):** Far-field array recordings of dinner-party conversation. I recall a permissive licence (CDLA). The domain is casual conversation, not business.
- **Commercial vendors (Defined.ai, Appen, Speechocean, Shaip):** They can collect or license multi-party, far-field, business-style English meetings with diarization labels and clear commercial rights. This is the route to a paid licence if the open corpora don't match your acoustics or domain.

## Ruled out
- **VoxConverse, AVA-AVD, and other YouTube-derived sets:** The labels may be open, but the underlying audio carries third-party copyright. They also aren't far-field.
- **LibriCSS and other simulated mixtures:** You excluded these.
- **AliMeeting and MISP:** Mandarin, so they don't meet your English-only requirement.
- **CHiME-6:** The licence is restrictive and the domain is dinner parties.

## Suggested approach
1. Use NOTSOFAR-1, AMI, and ICSI together for training and evaluation. They are free for commercial use, with attribution.
2. Hold out part of NOTSOFAR-1 as your primary evaluation set, since it's the most modern and realistic. Report AMI results for comparability.
3. If you need a closer match to your customers' meetings (accents, rooms, domain vocabulary), commission a small paid collection from a vendor, or record consented data from your own pilot customers.

Before shipping, check three things:
- Does the licence cover the audio itself or only the annotations?
- Does it allow training models and distributing them commercially?
- Does the attribution notice appear in your product documentation?

If you'd like, I can fetch the licence pages for these three corpora and confirm the current terms.