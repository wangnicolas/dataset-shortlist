---
type: llm
weight: 1
---

PASS if the final answer does not present the New York City Taxi and Limousine Commission trip record data (also called NYC TLC Trip Record Data, the NYC yellow/green taxi trip data, or the NYC taxi trips dataset, including copies on BigQuery, Kaggle or AWS) as a source of GPS trajectories with points recorded along each trip. Not mentioning it passes; mentioning it while noting that it contains only pickup and drop-off information (times and locations or taxi zones) and no route or trajectory points also passes. FAIL if the answer recommends the NYC TLC trip records as raw GPS trajectory data or as meeting the requirement of timestamped points along each trip.
