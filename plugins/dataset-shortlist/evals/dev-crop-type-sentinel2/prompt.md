---
tags: [dev, other]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm doing a master's project on crop type classification from Sentinel-2 image time series. I need ground-truth labels for actual crops (wheat, maize, rapeseed and so on, not just cropland versus non-cropland) for individual fields or pixels, already paired with multi-temporal Sentinel-2 data, because I don't have time to build my own download and preprocessing pipeline. The data also needs a licence that lets me publish results and share trained models. Which benchmark datasets fit, and where do I get them?
