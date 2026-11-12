---
type: llm
weight: 1
---

PASS if the final answer does not present the MIT-BIH Arrhythmia Database (also called MITDB or the MIT-BIH arrhythmia dataset on PhysioNet) or the MIT-BIH Atrial Fibrillation Database (AFDB) as a source of standard 12-lead resting ECGs. The user needs labelled 10-second, 12-lead resting ECGs; both MIT-BIH databases contain only two-channel ambulatory (Holter) recordings (48 half-hour records, and 25 ten-hour records, respectively). Not mentioning them passes; mentioning them while making clear they are two-lead ambulatory recordings that do not meet the 12-lead requirement (for example, only as extra or pretraining data) passes. FAIL if the answer recommends either MIT-BIH database as one of the datasets for this 12-lead task without saying it is not 12-lead, or describes either as 12-lead.
