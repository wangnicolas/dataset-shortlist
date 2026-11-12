I found no dataset that is both open to download and suitable for a full AKM decomposition. The closest to "start now" is the Veneto Workers Histories, which you get by sending a signed form. The other options need institutional applications or in-person visits. I haven't checked costs, turnaround times, or eligibility for some of these, and I say so below.

## What you can start on now

**Veneto Workers Histories (VWH), Italy, 1975–2001**
- **What it is:** Social-security records for every private-sector firm in the provinces of Treviso and Vicenza, plus every worker those firms employed. Workers are followed across their whole careers, including jobs outside the area. There are three linkable files: a worker registry, yearly contribution records, and firm information with tax codes. The [FRDB data page](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/) lists it and the [FRDB description PDF](https://www.frdb.org/wp-content/uploads/2015/03/Description_database_VWH.pdf) documents it. [Jaime Arellano-Bover's page](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources) has extra resources for users.
- **Access:** Download the access form from FRDB, sign it, and email it to info@frdb.org. I could not find eligibility rules, fees, or turnaround time on the page. Ask FRDB before you plan around it.
- **Fit:** It has 27 years of data and stable worker and firm IDs. Card, Devicienti and Maida (2014) used it for rent-sharing work.
- **Limits:** The data end in 2001, so it can't speak to recent inequality trends. It also covers two provinces, not all of Italy.

**IAB's SIAB Scientific Use File, Germany**
- **What it is:** A 2% sample of German social-security records, 1975–2023, with a downloadable [Regional File](https://fdz.iab.de/en/pd_hd/factually-anonymous-version-of-the-sample-of-integrated-labour-market-biographies-siab-regionalfile-version-7523-v1/). Institutions apply for it through the [FDZ](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/). I could not confirm eligibility for non-German institutions or the fees.
- **Why it doesn't work for AKM:** The Regional File has no shared establishment ID. It only has a counter that numbers establishments within each person's career. That means you can't build the worker–firm connected set. The [ZEW discussion paper](https://www.zew.de/fileadmin/FTP/dp/dp26025.pdf) and the [FDZ AKM documentation](https://doku.iab.de/fdz/reporte/2023/MR_01-23_EN.pdf) both point this way, but I am relying on search snippets, not the codebook. Check the codebook before you apply.
- **What it is good for:** Practice with the data structure and wage-inequality descriptives.

## What it takes to get real AKM-quality data

**Germany, full IAB data (LIAB, or SIAB weakly anonymous)**
- **Access:** On-site at an IAB research data centre, or remote access through the JoSuA system after first working on-site. You need an application and a data use agreement. See the [LIAB page](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/) and the [FDZ SIAB page](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/). Plan for a research stay in Nuremberg.
- **Precomputed AKM effects:** The FDZ offers worker and establishment effects estimated on the full data, covering 1985–2023 ([documentation](https://doku.iab.de/fdz/reporte/2025/MR_03-25_EN.pdf)). They are available only with the weakly anonymous data, through on-site or remote access, and may not combine with the SUF. They cover regular full-time workers only. This is the most practical route to a within- versus between-firm decomposition.

**Brazil, RAIS identified microdata**
- **Access:** You apply to the Ministry of Labor and Employment through your university. The application needs a project description and a justification for why you need identified data with consistent worker and employer IDs. It also needs a contact at your institution who can sign legal agreements. [Engbom and Moser's replication package](https://github.com/economoser/EM2022) describes this. The [Cambridge supplement](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0007123425100859/resource/name/S0007123425100859sup001.pdf) confirms the university route. I found no processing-time estimate.
- **Public version:** The de-identified files are downloadable (the [`raisr` package](https://cran.r-project.org/web/packages/raisr/index.html) reads them). I did not verify whether they carry worker IDs you could follow over time. I would assume they don't until you check.
- **Fit:** It covers the whole formal sector over many years. Engbom and Moser's work on Brazilian wage inequality is close to your question.

**United States, LEHD**
- **Access:** Restricted microdata are available only inside a Federal Statistical Research Data Center. You need an approved project, and some files need extra IRS approval. See the [Census LEHD page](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html). Expect a long approval process.
- **Public alternative:** The public Job-to-Job Flows and Quarterly Workforce Indicators tables are aggregates, so you can't estimate AKM with them.

**Nordic countries**
- **Denmark:** Statistics Denmark authorises only Danish institutions. A foreign researcher needs a Danish affiliate ([overview](https://www.dst.dk/Site/Dst/SingleFiles/GetArchiveFile.aspx?fi=645846915&fo=0&ext=forskning)).
- **Norway:** Foreign institutions generally get only anonymous data. Identifiable data go through projects run by Norwegian institutions ([Statistics Norway guidelines](https://www.ssb.no/en/data-til-forskning)).
- **Sweden:** The MONA platform (Statistics Sweden's remote-access system) can't be used from the US or Canada ([terms of use](https://www.scb.se/en/services/ordering-data-and-statistics/microdata/mona--statistics-swedens-platform-for-access-to-microdata/rules-and-regulations/terms-of-use/)). Unless you are in the EU or EEA, you would need a local collaborator or a visit.

## My recommendation
1. Email FRDB this week for VWH, so you have something to build and test the estimation pipeline on.
2. Ask your advisor which of these they can sponsor or co-apply for. Germany needs a stay in Nuremberg, Brazil needs your university to sign legal agreements, and the Nordic routes need a local collaborator.
3. Use the [ABC of AKM guide](https://arxiv.org/pdf/2603.17034) for methods. It covers the limited-mobility bias that affects small samples like the SIAB, and your decomposition will need that correction.

## What I didn't verify
- Where you are based. That decides the Sweden and US options.
- Fees and turnaround for FRDB, IAB, and the Brazilian ministry.
- Whether other countries have workable options, such as Portugal, France, or Italy's national INPS data. I didn't search for them.

I can look into any of these next if you tell me where you are based.

Sources:
- [FDZ LIAB longitudinal model](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)
- [FDZ SIAB](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/)
- [SIAB Regional File 7523](https://fdz.iab.de/en/pd_hd/factually-anonymous-version-of-the-sample-of-integrated-labour-market-biographies-siab-regionalfile-version-7523-v1/)
- [IAB AKM effects 1985–2023](https://doku.iab.de/fdz/reporte/2025/MR_03-25_EN.pdf)
- [IAB AKM effects (2023)](https://doku.iab.de/fdz/reporte/2023/MR_01-23_EN.pdf)
- [ZEW discussion paper](https://www.zew.de/fileadmin/FTP/dp/dp26025.pdf)
- [FRDB VWH page](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- [FRDB VWH description](https://www.frdb.org/wp-content/uploads/2015/03/Description_database_VWH.pdf)
- [Arellano-Bover VWH resources](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources)
- [Engbom–Moser replication package](https://github.com/economoser/EM2022)
- [Cambridge data access supplement](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0007123425100859/resource/name/S0007123425100859sup001.pdf)
- [raisr](https://cran.r-project.org/web/packages/raisr/index.html)
- [Census LEHD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)
- [Statistics Denmark](https://www.dst.dk/Site/Dst/SingleFiles/GetArchiveFile.aspx?fi=645846915&fo=0&ext=forskning)
- [Statistics Norway](https://www.ssb.no/en/data-til-forskning)
- [Statistics Sweden MONA terms](https://www.scb.se/en/services/ordering-data-and-statistics/microdata/mona--statistics-swedens-platform-for-access-to-microdata/rules-and-regulations/terms-of-use/)
- [The ABC of AKM](https://arxiv.org/pdf/2603.17034)