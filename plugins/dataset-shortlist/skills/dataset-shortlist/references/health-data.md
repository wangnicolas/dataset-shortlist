# Health and biomedical data

Read this whenever the data is about patients or human research participants.
Access rules here exist to protect the people in the data, so they are stricter,
slower and more varied than in other fields, and they are where careless answers
do the most damage.

## De-identified does not mean unrestricted

Most clinical research data has had names and dates removed and is still not a
free download. Expect one of these patterns, and say which one applies:

| Pattern | What it involves | Typical time |
|---|---|---|
| Open | Small, fully de-identified collections, teaching subsets and challenge data. Direct download. | minutes |
| Registered | An account and an agreement accepted online. | minutes to an hour |
| Credentialed | The researcher's identity is checked, a human-subjects research training certificate is required, and a data use agreement is signed. Access is personal: each team member applies separately. | days to two weeks |
| Controlled | A data access committee reviews a project proposal; often the institution's legal signatory must sign, ethics approval is expected, and renewal is periodic. Common for genomic data and national cohorts. | weeks to months |
| Enclave only | Data never leaves the provider's secure environment; analysis runs there, sometimes for a fee. | weeks to months |

Also check and report: who is eligible (students often need a supervisor to
apply or to vouch; some sources are limited by country or to academic
institutions), whether there is a fee, and whether a description of the project
is required.

## What to report for every health dataset

1. The access pattern and the exact steps, in order.
2. Any training that is required, and roughly how long it takes.
3. Whether the agreement is signed by the individual or by the institution.
4. Where analysis may happen: download to own machine, institutional server, or
   only inside the provider's environment.
5. The conditions that change how a project is run: no attempts at
   re-identification, no sharing of the data with anyone who does not hold
   access, citation and acknowledgement duties, deletion at the end of the
   project.
6. A realistic time to access, and a dataset the user can start on today while an
   application is pending, when one exists. Open subsets, demonstration versions
   and challenge data built from the same source are the usual candidates, and
   say plainly how they differ from the full data.

## Using online AI services with restricted data

Many data use agreements forbid sharing the data with third parties, and data
providers read that as covering online AI services. If the user plans to use a
hosted language model on restricted records, tell them to check before they
start, and report what the provider says.

PhysioNet states its position for its credentialed and restricted data in a post
dated 24 September 2025 (https://physionet.org/news/post/llm-responsible-use/):

- the agreement "explicitly prohibits sharing access to the data with third
  parties, including sending it through APIs or using it on online platforms"
- locally deployed models are strongly recommended
- a cloud service may be used only when zero data retention, no use of the data
  for model training and no human review are verified, and "if a service's data
  handling practices are unclear or cannot be fully verified, do not use the
  service"
- access is personal; sharing within a team or a class is not permitted
  (https://physionet.org/about/faqs/)

Check the provider's current page rather than relying on this summary, and give
the user the link. Other providers have their own rules; look for a statement on
AI services or third-party processing in the agreement.

The same care applies to this conversation. Work from documentation, variable
lists and summary statistics. Do not ask the user to paste restricted records
into the chat, and say why if they offer to.

## Fit checks that matter most in clinical data

- **Is the outcome recorded, or must it be derived?** Many clinical outcomes are
  not a column. They are built from diagnosis codes, laboratory criteria or
  timestamps. Say which, because deriving a label is work and its definition
  shapes the results.
- **Is the outcome built from the same measurements that would be the inputs?**
  If so, say it. It limits what can honestly be called prediction.
- **Unit and scale.** Patients, admissions, unit stays and recordings are
  different counts. Report the one the question needs.
- **Population and setting.** Adult or paediatric, one hospital or many, which
  country and years. A model question about one setting is not answered by data
  from another.
- **Time resolution and length** for signals and time series.
- **Linkage.** Whether notes, images, waveforms and records for the same
  patients can be joined, and whether each part has its own access condition.

## Ethics

Open or de-identified data may still need a determination from the user's own
institution that the work is exempt from ethics review. Suggest they check with
their institution early; it is usually quick and occasionally a blocker.
