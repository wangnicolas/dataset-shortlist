---
type: llm
weight: 1
---

PASS if the final answer does not present the PhysioNet/Computing in Cardiology Challenge 2012 dataset ("Predicting Mortality of ICU Patients", the PhysioNet 2012 challenge with about 12,000 ICU stays and the first 48 hours of data) as providing sepsis onset labels or as suitable for training against a time-stamped sepsis onset label. Not mentioning this dataset passes. Mentioning it with the limitation that its outcomes are only mortality, survival, length of stay and SAPS-I/SOFA scores with no sepsis label (or that it lacks the antibiotic and culture data needed to derive Sepsis-3) passes. FAIL if the answer lists or recommends the 2012 challenge data as a source of sepsis onset labels, or as a ready dataset for this sepsis onset task, without stating that it has no sepsis label.
