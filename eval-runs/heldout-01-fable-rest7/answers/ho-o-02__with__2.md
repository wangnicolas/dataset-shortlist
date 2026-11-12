Nothing real is downloadable today with a confirmed employer identifier. The fastest real option is the Veneto Worker Histories file (Italy, 1975–2001), released on a signed form by email; the best current data is Germany's SIEED, which takes months and an application from your advisor's chair. All checks were made on 12 November 2026; anything marked "from memory" was not confirmed.

## What I assumed you need

- **R1–R3 (must):** persistent worker ID, persistent employer ID, individual earnings.
- **R4 (must):** at least ten years.
- **R5 (must, my addition):** all or most co-workers observed at each employer. A within/between-firm split needs this, and small worker samples (2–4%) also give badly biased firm effects. This rules out several otherwise "easy" datasets.
- **R6 (nice):** obtainable by a PhD student, ideally soon.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Veneto Worker Histories (Italy) | Signed form emailed to the distributor; weeks (my estimate) | Signed form; required credit line | All private-sector workers and firms in Veneto, 1975–2001 | Strong | Today; earnings variables from memory |
| 2 | SIEED (Germany, IAB) | Institutional agreement, then remote execution or on-site; months | Custom use agreement | 1% of establishments, all their workers, 1975–2023 | Strong | Today; top-coding from memory |
| 3 | LEHD (US Census) | Proposal plus security clearance, secure lab only; 6–12+ months | Federal confidentiality law | Near-universe, 1990s onward | Strong | Process today via secondary sources; contents from memory |
| 4 | LIAB (Germany, IAB) | Same route as SIEED; months | Custom use agreement | Surveyed establishments and their workers, 1993–2023 | Partial | Today; longitudinal variant from memory |
| 5 | Panel tous salariés (France, CASD) | Committee approval plus paid secure access; months | Custom | 1/24 worker sample (1/12 from 2002), from 1976 | Partial (fails R5) | Catalogue today; procedure and fee from memory |
| 6 | MCVL (Spain) | Institution applies to Social Security, free; weeks (from memory) | Non-commercial research terms | 4% of individuals (from memory) | Partial (fails R5) | Eligibility today; sample size from memory |
| 7 | PyTwoWay / BipartitePandas simulated data | `pip install`; minutes | Not checked | Any size you simulate | Pipeline only | Today |

## Details

**1. [Veneto Worker Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)**
- **Contents:** three linkable Stata files (workers, firms, contracts) with an anonymous worker ID and a firm ID; firms are not anonymised.
- **Coverage:** the distributor's page says Treviso and Vicenza only, but [a user's notes page](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources) says it covers all of Veneto and follows workers who leave the region.
- **Access:** the page says "fill and sign the attached form and send it to info@frdb.org". No fee is stated. I could not read the form's terms or turnaround.
- **Limits:** it ends in 2001, covers one region, and users drop the years before 1984–85 because of missing data. That leaves about 17 usable years, but none recent.
- **Used by:** [Kline, Saggio and Sølvsten (2020)](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA16410) for an AKM variance decomposition.

**2. [SIEED 7523](https://fdz.iab.de/en/int_bd_pd/the-sample-of-integrated-employer-employee-data-sieed-sieed-7523-version-1/)**
- **Contents:** every worker ever employed at a 1% sample of German establishments, with full biographies. Wages are top-coded and there are no hours (from memory).
- **Access:** there is no off-site file. Per the [access page](https://fdz.iab.de/en/data-access/on-site-use/), the agreement is between your institution and the data centre, and for thesis work the supervising chair must apply and name you. The legal check "could take up to one month".
- **Working mode:** you then submit Stata scripts remotely and receive disclosure-checked output, or work on-site. Sites in the US, Canada and UK are only for stays of nine months or more and use extra-anonymised data. Remote desktop is only for institutions in Germany.
- **Available now:** test data with the real file structure can be downloaded, but it is "random and therefore not eligible for analysis".

**3. [LEHD](https://www.census.gov/topics/research/guidance/restricted-use-microdata/standard-application-process.html)**
- **Eligibility:** US residence for 36 of the past 60 months and a US institution; your advisor should be co-PI.
- **Timeline:** 1–2 months to write the proposal, several months of review, then at least 3–4 months for the background check. Budget a year.
- **Caveat:** the page I verified is the general Census application page, not one specific to LEHD.

**4. [LIAB](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-cross-sectional-model-1993-2023-version-1/)**
- It adds establishment survey variables (bargaining coverage, works councils) to the worker records, through the same application as SIEED.
- The page I verified is the cross-sectional model; the longitudinal model is the one for AKM (from memory).

**5. [Panel tous salariés](https://www.casd.eu/en/source/all-employee-panel/)**
- It is long (from 1976) but a worker sample, so it cannot give within-firm variance.
- The exhaustive annual files in the same secure centre can be chained across years instead (from memory).
- Approval goes through the Comité du secret statistique. Whether non-French institutions are eligible, and the price, were not confirmed.

**6. [MCVL](https://portaldatos.seg-social.gob.es/mcvl)**
- The portal says public and private institutions may request it for non-commercial scientific research. It is free, and employment spells carry the employer's contribution account code.
- It is good for mobility and earnings dynamics but not for firm effects. Whether institutions outside Spain qualify was not confirmed.

**7. [PyTwoWay](https://tlamadon.github.io/pytwoway/)**
- It simulates a worker-firm panel with known worker and firm effects, and includes AKM plus the standard bias corrections.
- It cannot answer your question, but it lets you build and test the whole pipeline now. The [2026 JEP guide to AKM](https://doi.org/10.1257/jep.20231372) covers estimation practice.

## Known, not confirmed

- **Chile, unemployment insurance samples:** this is the lead most worth an hour of your time. The regulator publishes anonymised 3%, 5% and 12% worker samples, monthly since 2002, and published papers describe downloading them directly. A separate public sample of the employer database also exists. The download address those papers cite returned 404 today, and I could not confirm an employer identifier in the public files. Even with one, the worker samples would fail R5; check whether the employer sample includes all workers at sampled firms. Start from the [regulator's announcement](https://www.spensiones.cl/portal/institucional/594/w3-article-12931.html).
- **Portugal, Quadros de Pessoal:** the classic AKM dataset. Access appears to run through a researcher accreditation platform and a contract with the statistics office; the conditions for foreign institutions were not found.
- **Brazil, RAIS (identified version):** requires an application to the Brazilian ministry, per the [Engbom–Moser replication package](https://github.com/economoser/EM2022), which also ships AKM code.
- **Italy, full social security archives:** on-site in Rome through the VisitINPS programme, which is competitive. A separate 6.5% worker sample (LoSaI) is released by the Ministry of Labour on a research proposal; I could not confirm a firm identifier.
- **Not checked at all (from memory, all secure-environment access through a national statistics office):** Nordic registers, the Netherlands, Austria, UK (ASHE), Hungary, Canada. Most are much easier with a local co-author.

## Not recommended, and why

- **SIAB (Germany), including its Scientific Use File:** a 2% worker sample, so co-workers are almost never observed. It is the easiest IAB file to hold off-site but the wrong design for this question.
- **PSID, NLSY, SIPP, SOEP:** they follow workers across jobs but do not link co-workers to a common employer ID (from memory).
- **European Structure of Earnings Survey:** allows a within/between-workplace split, but workers are not followed, so no AKM.
- **Public LEHD tabulations and public RAIS extracts:** aggregates, or no person IDs (from memory).

## What I could not find

- No real linked panel with a confirmed employer ID that downloads without an application.
- The text of the Veneto access form, the Spanish request forms and the French secure-centre prices.
- Whether the test data in the [Kline–Saggio–Sølvsten code repository](https://github.com/rsaggio87/LeaveOutTwoWay) is real or simulated.

Dataset registries hold almost nothing for this kind of data, so most facts come from the owners' pages and web search.

## Next step

1. **Today:** install PyTwoWay and build the pipeline on simulated data.
2. **This week:** send the Veneto form, and ask your advisor whether the chair will submit the SIEED application. That request is the long pole, and you can code against the test data while it runs.
3. **If you need a US result:** start the LEHD conversation with your nearest research data center now, in parallel.

The interactive shortlist is at `/private/tmp/e-M9mN91/home/cwd/dataset-shortlist.html`.