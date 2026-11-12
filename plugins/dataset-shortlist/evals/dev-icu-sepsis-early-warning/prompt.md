---
tags: [dev, health]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm a second-year PhD student starting a project on early prediction of sepsis onset in adult ICU patients, using the vitals and lab values that are routinely charted during the stay. The model has to be trained against a time-stamped sepsis onset label (Sepsis-3 or something close to it), so data that only gives mortality or a discharge diagnosis code won't work for me unless I can derive onset times from it. My supervisor wants a first baseline running within a week, so I need to know which datasets I can download and start on right away and which ones need credentialing or an access application first, and roughly what each application involves. Which datasets should I be looking at?
