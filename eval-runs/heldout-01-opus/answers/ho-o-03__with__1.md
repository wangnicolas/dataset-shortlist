For data you can use commercially and download today, start with **NOTSOFAR-1** and **AMI**, both CC BY 4.0. Add **CHiME-6**, **ICSI** and **DiPCo** for more variety, and **Earnings-21/22** if you want real business speech that isn't far-field. Together these come to roughly 250–300 hours. Every licence below was checked against the official source on 2026-11-12, unless it's marked "from memory".

## What I assumed you need
- **R1 (must):** real multi-party conversation, ideally business meetings. I counted AMI's role-play design meetings as real, because the talk itself is unscripted.
- **R2 (must):** speaker-turn labels (who spoke when).
- **R3 (nice to have):** far-field or microphone-array audio.
- **R4 (must):** English.
- **R5 (must):** commercial use allowed. A fee is fine; non-commercial or "research only" is out. I took "commercial use" to include training models that you then ship.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NOTSOFAR-1 (recorded meetings) | Open download | CC BY 4.0 | 237 meetings of about 6 min each, several devices per meeting | Strong | today |
| 2 | AMI Meeting Corpus | Open download | CC BY 4.0 | About 100 h | Strong | today (size from memory) |
| 3 | CHiME-6 (dinner parties) | Open download, about 120 GB | CC BY-SA 4.0 | About 40 h (from memory) | Strong for far-field, but not business | today |
| 4 | ICSI Meeting Corpus (Edinburgh release) | Open download | CC BY 4.0 | About 70 h | Partial: no far-field audio in this release | today |
| 5 | DiPCo (Amazon) | Open download | CDLA-Permissive-1.0 | About 5 h (from memory) | Partial: small, not business | today |
| 6 | Earnings-21 / Earnings-22 (Rev) | Open download (GitHub, Git LFS) | CC BY-SA 4.0 | 39 h, plus about 119 h for E-22 (from memory) | Partial: phone/webcast audio | today |
| 7 | LDC meeting sets: ICSI with far-field channels (LDC2004S02), NIST RT-05S, ISL | Paid: LDC for-profit membership, takes weeks | LDC membership agreement | Small | Partial | today (fees from memory) |

## Details
1. **NOTSOFAR-1** (github.com/microsoft/NOTSOFAR1-Challenge; data at huggingface.co/datasets/microsoft/NOTSOFAR)
   - **Contents:** the README describes "237 meetings… recorded across 30 conference rooms with 4-8 attendees", recorded on both single-channel and multi-channel far-field devices, with ground-truth labels. This is the closest match to your product.
   - **Licence:** the README says "licensed under the Creative Commons Attribution 4.0 International License".
   - **Get it:** call `download_meeting_subset()` from the repo.
   - **Watch out for:**
     - Only 35 unique speakers, so speaker variety is low.
     - The same README calls the data "provided for open research". The licence it states is still CC BY 4.0, but get a quick legal read.
     - Leave out the ~1000 h simulated training set if you only want real audio.
   - **Used in:** the Interspeech 2024 dataset paper (doi:10.21437/interspeech.2024-1788) and the BUT/JHU CHiME-8 system (doi:10.21437/chime.2024-4).
2. **AMI** (groups.inf.ed.ac.uk/ami/corpus/)
   - **Licence:** the licence page says "The AMI corpus and its annotations are released under the Creative Commons Attribution 4.0 license".
   - **Contents (from memory):** headset, lapel and two 8-mic circular arrays, with speaker-aligned transcripts.
   - **Watch out for:** about two thirds are role-play design-team meetings. Many speakers are non-native.
   - **Used in:** the corpus paper (doi:10.1007/s10579-007-9040-x).
3. **CHiME-6** (openslr.org/150)
   - **Licence:** OpenSLR lists "License: Attribution-ShareAlike 4.0". This is the current release; CHiME-5 originally had a more restrictive licence, so make sure you take this one.
   - **Contents:** real 4-person dinner parties recorded on distributed Kinect arrays, with JSON transcripts carrying speaker IDs and times. There is a lot of overlapping speech.
   - **Watch out for:** ShareAlike means any modified dataset you share must stay CC BY-SA. Whether trained model weights count is a question for your lawyer.
   - **Used in:** the CHiME-8 DASR overview (doi:10.21437/chime.2024-1).
4. **ICSI, Edinburgh release** (groups.inf.ed.ac.uk/ami/icsi/)
   - **Licence:** CC BY 4.0, confirmed on the page.
   - **Contents:** real research-group meetings.
   - **Watch out for:** the download page only offers "Headset mix" and "Individual channel headsets". From memory, the tabletop distant mics are only in the LDC version (#7).
5. **DiPCo** (zenodo.org/records/8122551)
   - **Contents:** real conversations between "four Amazon employee volunteers", recorded with close-talk mics and "five far-field 7-microphone" arrays.
   - **Licence:** CDLA-Permissive-1.0, which allows commercial use.
   - **Best use:** a small, clean far-field evaluation set.
6. **Earnings-21/22** (github.com/revdotcom/speech-datasets)
   - **Licence:** CC BY-SA 4.0.
   - **Contents:** real business calls with a speaker ID on every word.
   - **Check:** whether the `ts`/`endTs` timing columns are filled in. If not, you'll need forced alignment to get turn times.
   - **Watch out for:** no far-field audio, and less overlap than real meetings.
7. **LDC (paid route).** I confirmed this on LDC's licensing page today:
   - Non-members, including for-profit companies, "cannot use LDC data… for any commercial purpose".
   - For-profit members get commercial rights to the data they license during their membership year.
   - So buying a single corpus without joining does **not** give you commercial rights; you have to join.
   - From memory, for-profit membership has cost tens of thousands of USD a year. Ask the LDC Membership Office for current fees.

## Known, not confirmed
- **Commercial data vendors** such as Appen, Defined.ai and Shaip. From memory, they sell off-the-shelf meeting audio or collect it to order with diarization labels and commercial licences. I didn't check any of them. If you need hundreds of hours of varied, consented business meetings recorded on devices like yours, this is probably the only route.

## Not recommended, and why
- **VoxConverse:** the README says "for research purposes", and the audio comes from YouTube. It's also broadcast content, not meetings.
- **MeetingBank and ground-truth/multichannel-meetings-10h:** non-commercial licences (NC).
- **Simulated or replayed audio** (NOTSOFAR simulated set, LibriCSS, LibriWASN): you've ruled these out.
- **AliMeeting and AISHELL-4:** Mandarin.
- **DIHARD, Fisher, Switchboard, CALLHOME, Mixer 6:** these come from LDC (so membership is needed for commercial use), and most are 2-party phone calls or interviews.
- **Unofficial Hugging Face mirrors of ICSI and DiPCo:** use the official sources instead.

## What I could not find
I found no large (hundreds of hours), recent, real English business-meeting corpus with array audio and a commercial licence. The open sets above are the whole public supply. The literature search added little, because the speech conference venues are poorly indexed in the sources the tool uses.

## Next step
1. Download NOTSOFAR-1 and AMI today and set up your diarization benchmark: DER on NOTSOFAR, AMI and DiPCo.
2. Have counsel sign off on two things: CC BY-SA for CHiME-6 and Earnings, and the NOTSOFAR "open research" wording.
3. Then decide whether to scale up with a vendor collection or with LDC membership.

The interactive shortlist, with filters and an access-plan export, is at `/private/tmp/e-55YarO/home/cwd/dataset-shortlist.html`.