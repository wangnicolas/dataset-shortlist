For a baseline in a week, start with the PhysioNet 2019 Challenge data today. At the same time, begin the PhysioNet credentialing for MIMIC-IV and eICU-CRD, because that process is the bottleneck. I confirmed every dataset below exists and how it is accessed by reading its source page or searching for it. Some details come only from search summaries, and I've flagged those.

## Download today, no application

**PhysioNet/CinC Challenge 2019, "Early Prediction of Sepsis from Clinical Data" (v1.0.0)**
- It is open access under CC BY 4.0. Download it with `wget -r -N -c -np https://physionet.org/files/challenge-2019/1.0.0/`.
- It has 40,336 ICU stays in two training sets (A: 20,336 and B: 20,000). It is 42 MB, with one pipe-separated file per patient. Columns are hourly vitals, labs, demographics, and `SepsisLabel`.
- The label is time-stamped. For sepsis patients, `SepsisLabel` is 1 from 6 hours before the Sepsis-3-derived onset time. For other patients it is always 0.
- The label is already offset by 6 hours, and the data are hourly and pre-aggregated. This is fine for a baseline, but it limits what you can do about label definitions or finer time resolution.
- The hidden test set is not public, so you will have to create your own splits.

The open demo subsets of MIMIC and eICU are also available now, but they are too small for anything beyond testing your pipeline.

## Credentialed, same PhysioNet application

Both datasets below use one PhysioNet credentialing, so you apply once.

1. Register a PhysioNet account.
2. Complete the CITI course "Data or Specimens Only Research" and upload the completion report.
3. Submit your affiliation and reference details, and wait for approval.
4. Sign the dataset-specific DUA (PhysioNet Credentialed Health Data Use Agreement 1.5.0). Each dataset needs its own signature.

One secondary source reported approval taking about 1–2 weeks, which I did not confirm on a PhysioNet page. Plan for it to miss your one-week deadline, so submit it today. Your supervisor may need to act as your reference, and your institution may need to confirm your affiliation.

- **MIMIC-IV v3.1** has a PhysioNet page that I read directly. It is the standard choice for this task. The PhysioNet page does not mention sepsis, so you derive onset times yourself, typically with the Sepsis-3 code in the MIT-LCP `mimic-code` repository (suspected infection plus a SOFA rise of 2 or more). I did not verify that repository in this search. You will need to make and document choices about the infection time window and the SOFA baseline.
- **eICU-CRD v2.0** has over 200,000 admissions from US hospitals in 2014–2015. It is multi-center, so it is useful for external validation. It also has no ready-made Sepsis-3 label, and its time resolution is coarser than MIMIC-IV's.

## Separate application, not within your first week

- **HiRID v1.1.1** has about 34,000 admissions from Bern University Hospital, with data every 2 minutes. Its access type is "Contributor Review", which is stricter than credentialed. You need PhysioNet credentialing, and the data owners must also approve each study, with a specific research question. The PhysioNet page does not mention sepsis, and the original study was on circulatory failure. A search summary said the HiRID-ICU-Benchmark paper applied Sepsis-3 criteria, but I could not confirm that. Treat HiRID as a possible later addition, not a baseline dataset.
- **AmsterdamUMCdb v1.5.0** is free but needs a separate application. You enter your institutional email in an online portal and accept an End User License. A reference, who should be an intensivist, must also accept the terms from their own mailbox. The administrators check your training and reference, normally within five business days. After that you request the files from DANS Data Station Life Sciences. Published Sepsis-3 code exists for it (`tedinburgh/sepsis3-amsterdamumcdb`), which makes it a good external validation set. I could not load the main site page directly. This process comes from a search summary of it, so check the exact training course on the portal.

## Suggested plan

1. **Today:** download Challenge 2019 and start the CITI course and PhysioNet application.
2. **Week 1:** build the baseline on Challenge 2019, using patient-level splits. Treat it as a pipeline prototype, not a final result.
3. **Once approved:** re-derive Sepsis-3 onset in MIMIC-IV and move your main experiments there. Use eICU for external validation. Consider AmsterdamUMCdb as well.

I did not find or check any dataset beyond the five above. Ones such as the Emory/Grady data in Challenge 2019 or other national ICU databases may exist but are not covered here.

Sources:
- [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/3.1/)
- [How do I access MIMIC?](https://mimic.mit.edu/docs/faq/how-to-get-access.html)
- [PhysioNet Credentialed Access: How It Works — CASRAI](https://casrai.org/guides/physionet-credentialed-access-restricted-data)
- [Challenge 2019 v1.0.0](https://physionet.org/content/challenge-2019/1.0.0/)
- [eICU-CRD v2.0](https://physionet.org/content/eicu-crd/2.0/)
- [HiRID v1.1.1](https://physionet.org/content/hirid/1.1.1/)
- [HiRID-ICU-Benchmark (arXiv)](https://arxiv.org/html/2111.08536v4)
- [AmsterdamUMCdb](https://amsterdammedicaldatascience.nl/)
- [AmsterdamUMCdb on GitHub](https://github.com/AmsterdamUMC/AmsterdamUMCdb)
- [Sepsis-3 in AmsterdamUMCdb (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0304133)