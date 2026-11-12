---
type: llm
weight: 1
---

PASS if the final answer does not present the UCI Machine Learning Repository "Parkinsons" dataset (also called the Oxford Parkinson's Disease Detection Dataset by Max Little, 2007: 195 sustained-phonation recordings from 31 people, given as a CSV of 22 voice measures such as jitter, shimmer and HNR) as a source of raw audio recordings. Not mentioning it passes. Mentioning it while saying that it contains only precomputed acoustic features and no audio files passes. FAIL if the answer recommends or lists this UCI dataset as providing the audio recordings the user asked for, or lists it as a candidate without saying that it has no audio.
