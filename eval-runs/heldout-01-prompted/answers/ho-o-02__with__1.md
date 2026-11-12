Nothing I found lets you run a real AKM decomposition on open data. The nearest things to start with are the SIAB Campus File (to practice the pipeline) and an email to the IAB (to open the process for real data).

My searches mostly turned up overview pages. Wherever a page didn't state something, I say so rather than fill in from memory. Rules change, so confirm the details with each data holder.

## Options ranked by how likely they are to work for you

**1. German IAB data (the most realistic route for a PhD student)**
- **SIAB (Sample of Integrated Labour Market Biographies).** It's an administrative worker-level panel with data since 1975, so ten years is easy. The current releases are SIAB 7523 and Regional File 7523. There are three versions:
  - *Weakly anonymous:* research visits only, which includes remote data access.
  - *Regional File (scientific use file):* downloadable by your institution after a use agreement with the IAB.
  - *Campus File:* free after registering, but for teaching only. It can't be used for inference or publication.
- **AKM effects.** An IAB-affiliated guide to the SIAB says AKM effects can be requested when you apply, or by email to iab.fdz@iab.de for an existing project. That means you may not have to estimate the model yourself.
- **Open question.** An older guide says the Regional File scientific use file has no establishment identifiers. I couldn't confirm whether the AKM effects come with that version or only the on-site one, so ask the FDZ before applying. The SIAB is also a sample, not the full population. From my own background knowledge, not something I verified here, a sample makes it harder to build a connected set of movers.
- **LIAB (Linked Employer-Employee Data).** It's a worker panel linked to the IAB Establishment Panel (a survey of workplaces). Versions run 1975–2021 and 1993–2019. It's on-site only (with remote access afterwards), has no scientific use file, and requires an application.
- **How to start.** Email the FDZ. I couldn't find eligibility, cost or processing-time details, so ask about those, and about the International Data Access Network (IDAN) if you're outside Germany. The FDZ phone line is +49 911 179-1752.
- [FDZ data access](https://fdz.iab.de/en/data-access) · [SIAB](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/) · [LIAB 1975–2021](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/) · [SIAB guide](https://link.springer.com/article/10.1186/s12651-023-00335-w)

**2. Italy: INPS VisitINPS Scholars**
- This is a refereed call for projects. You work on-site at INPS in Rome.
- INPS lists an annual private-sector employer-employee database covering 1974–2025 and a monthly one covering 2005–2025. It also lists firm data and balance sheets (CERVED, ORBIS).
- The most recent call I found had a January 2026 deadline for the Type B round. Calls recur, so check the programme page for the next one. There are fellowship and scholar types, and they differ in funding.
- It takes a real project proposal and a stay in Rome, but the data are very good.
- [INPS programme page](https://www.inps.it/it/it/dati-e-bilanci/attivit--di-ricerca/programma-visitinps-scholars.html) · [Databases available](https://www.inps.it/content/dam/inps-site/pdf/datiebilanci/visitinps-scholars/documents/Banche_dati_disponibili_EN.pdf)

**3. Brazil RAIS (identified)**
- It's a full formal-sector linked employer-employee dataset with worker (PIS) and firm (CNPJ) identifiers. Non-identified microdata are public, but they can't be used for AKM because they lack persistent IDs.
- The identified data come from an application to the Ministry of Labour and Employment. A replication README describes it (observatoriotrabalho@mte.gov.br). The application needs:
  - project details;
  - a justification for why you need time-consistent person and employer IDs;
  - a person at your institution who can sign legal agreements.
- I didn't find a published processing time or fee. Ask the ministry directly.
- [EM2022 README](https://github.com/economoser/EM2022/blob/main/README.md)

**4. Denmark (Statistics Denmark, IDA)**
- IDA links every employee to their workplace for the whole population, with secure remote access.
- Authorisation goes to Danish institutions only. Foreign researchers need a Danish authorised institution to take responsibility for them. I'd treat this as a co-author or visiting route, not something you can apply for alone.
- [Authorisation of institutions](https://dst.dk/en/TilSalg/Forskningsservice/Dataadgang/Autorisering)

**5. US Census LEHD**
- Job-level files cover UI-covered jobs, mostly from 2000 on and only for some states. Access is through a Federal Statistical Research Data Center (FSRDC), which requires an approved project.
- Some files contain tax data and need extra IRS approval. This is a long, heavy process.
- [Census LEHD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)

**6. Portugal (Quadros de Pessoal / Relatório Único)**
- The data are annual, cover private-sector employers, and ran as QP until 2009.
- The Banco de Portugal lab's 2018 guide says QP is for internal researchers and their collaborators, and external researchers can apply for surrogate access only for relevant projects.
- That guide is old, so I can't tell you today's rules. Other papers thank the Ministry of Employment's planning office (GEP) for access.
- [BPLIM guide](https://cicee.autonoma.pt/wp-content/uploads/2024/03/BPlim_Guide_for_Researchers_v2018sep26.pdf)

**7. Veneto Workers History (Italy, 1975–2001)**
- The dataset exists and has been used in published papers, but I found no open download or formal application. It appears to be obtained from Giuseppe Tattara's group at Ca' Foscari. The Fondazione Rodolfo Debenedetti (FRDB) lists it on its data page.
- Since it ends in 2001, it won't show recent inequality trends. Its terms are unclear, so only pursue it if you have a personal contact.

## What you can do now
- **Today:** Register for the SIAB Campus File and build your cleaning pipeline and AKM code on it. Don't use it for any results you want to publish.
- **This week:**
  - Email the FDZ-IAB about the Regional File and the AKM effects.
  - Ask your advisor whether your department has a data-access contact or a Danish, German or Italian co-author. That is often what decides whether access happens in months or years.
  - Look for the next VisitINPS call.
- **Cross-country comparison:** Many papers using restricted data publish replication code and sometimes AKM effects or summary tables. These are good benchmarks, but they won't give you your own decomposition.

Sources:
- [FDZ-IAB LIAB longitudinal model](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)
- [FDZ data access](https://fdz.iab.de/en/data-access)
- [FDZ SIAB overview](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/)
- [SIAB 7519 guide](https://link.springer.com/article/10.1186/s12651-023-00335-w)
- [Statistics Denmark authorisation](https://dst.dk/en/TilSalg/Forskningsservice/Dataadgang/Autorisering)
- [EM2022 README (RAIS)](https://github.com/economoser/EM2022/blob/main/README.md)
- [Census LEHD restricted data](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)
- [INPS databases](https://www.inps.it/content/dam/inps-site/pdf/datiebilanci/visitinps-scholars/documents/Banche_dati_disponibili_EN.pdf)
- [VisitINPS Scholars](https://www.inps.it/it/it/dati-e-bilanci/attivit--di-ricerca/programma-visitinps-scholars.html)
- [BPLIM guide](https://cicee.autonoma.pt/wp-content/uploads/2024/03/BPlim_Guide_for_Researchers_v2018sep26.pdf)
- [FRDB data page](https://www.frdb.org/en/pagina-dati/)