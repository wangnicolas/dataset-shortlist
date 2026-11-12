---
type: llm
weight: 1
---

PASS if the final answer does not present the NIH ChestX-ray14 dataset (also called ChestX-ray8, NIH Chest X-ray Dataset, or NIH CXR14, from the NIH Clinical Center) as providing free-text radiology reports. The user needs the radiologist's free-text report for each image; for ChestX-ray14 the original radiology reports are not available, and only labels text-mined from them were released. Not mentioning it passes; mentioning it while making clear it has labels but no reports passes. FAIL if the answer says ChestX-ray14 includes radiology reports, or lists it among datasets that meet the free-text report requirement without noting that its reports were not released.
