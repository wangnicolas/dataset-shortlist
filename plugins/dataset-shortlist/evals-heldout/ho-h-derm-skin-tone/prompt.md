---
tags: [heldout, health]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill]
---

For a fairness audit I want to test whether dermatology image classifiers do worse on darker skin. I need skin images where every image (or patient) comes with a skin tone label, either Fitzpatrick type or Monk scale, as well as a diagnosis, and the darker types (V and VI) have to actually be represented rather than a handful. Clinical photos or dermoscopy are both fine, and it doesn't have to be skin cancer only. Which public datasets have that?
