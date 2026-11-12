I recommend building on **NOTSOFAR-1 and AMI**, adding **ICSI**, and using **DiPCo** as an extra far-field test set. I checked the licence page for each one, and all four allow commercial use with no fee. Each needs attribution, and for each I've noted what's weaker about it.

### Best fits

| Corpus | What it is | Far-field / arrays | Size | Licence |
|---|---|---|---|---|
| **NOTSOFAR-1** (Microsoft, CHiME-8) | Real office meetings with 4–8 people, recorded in 30 different conference rooms | Several commercial multi-channel array devices plus single-channel devices per meeting | 237 recorded meetings averaging ~6 min, plus ~1,000 h of simulated training data | **CC BY 4.0** (confirmed in the repo's DATA_LICENSE) |
| **AMI Meeting Corpus** | Business-style meetings of about 4 people, with speaker-turn and word-level annotations | Two 8-mic circular arrays, plus headset and lapel mics | ~100 h | **CC BY 4.0** |
| **ICSI Meeting Corpus** | Real weekly research-group meetings with 3–10 people | Tabletop distant mics plus close-talk mics; no proper arrays | ~72 h | **CC BY 4.0** through the Edinburgh distribution (no LDC fee) |

How they differ:
- **NOTSOFAR-1** is the closest match to your product: real, unscripted meetings on the kind of hardware customers actually use. It's small, though. The training and dev annotations are still being upgraded, and the 1,000 h training set is simulated, which is the kind of data you said you don't want. Use the real recordings for fine-tuning and evaluation. Using the simulated set is up to you.
- **AMI** has the most real meeting audio recorded on arrays. About 70% of it is scenario meetings: real people talking spontaneously, but playing assigned roles in a made-up design project. The other ~30% are naturally occurring meetings. Many of the speakers aren't native English speakers. That's good for robustness, but keep it in mind when you evaluate.
- **ICSI** gives you real, long meetings with many speakers and lots of overlap. The recordings are older and it has no arrays.

### Useful extra
- **DiPCo** (Amazon): real 4-person dinner-party conversations recorded with five far-field 7-mic arrays plus close-talk mics. It's 10 sessions of 15–45 min each. The licence is **CDLA-Permissive 1.0**, which allows commercial use. It isn't business talk, but it's a good far-field test set. The original S3 link is dead, so get it from Zenodo (record 8122551).

### Ruled out
- **CHiME-5/6**: research-only licence.
- **MSDWild**: non-commercial.
- **AliMeeting, AISHELL-4, MISP**: Mandarin.
- **LibriCSS** and similar: simulated or replayed mixtures.
- **VoxConverse**: YouTube audio, so the rights to the audio are unclear.

### If you need more real data
The open corpora together give a few hundred hours, which may be less than you need for training. Two ways to get more:
- **LDC for-profit membership or commercial licences.** For example, the NIST Meeting Pilot Corpus (LDC2004S09). LDC licences explicitly cover commercial use for paying for-profit members. Check each corpus's terms.
- **Commercial data vendors** such as Appen, Defined.ai or Shaip. They sell or custom-collect meeting audio with diarization labels and commercial rights. Custom collection is the only way to get recordings that match your own mic setups.

### Practical notes
- CC BY and CDLA-Permissive only require attribution and keeping the licence notices. Keep an attributions file listing each dataset you use. This isn't legal advice, so have whoever handles your contracts read the licence texts before you ship.
- The participants consented to research recordings years ago. The licences allow commercial use, but if you plan to publish voice samples from these recordings in marketing material, ask your counsel first.

Sources:
- [AMI licence](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [ICSI licence (Edinburgh)](https://groups.inf.ed.ac.uk/ami/icsi/license.shtml)
- [NOTSOFAR-1 repo](https://github.com/microsoft/NOTSOFAR1-Challenge) and [DATA_LICENSE](https://raw.githubusercontent.com/microsoft/NOTSOFAR1-Challenge/main/DATA_LICENSE)
- [DiPCo on Zenodo](https://zenodo.org/records/8122551), [DiPCo paper](https://arxiv.org/pdf/1909.13447), [Amazon Science blog](https://www.amazon.science/blog/amazon-releases-new-public-data-set-to-help-address-cocktail-party-problem)