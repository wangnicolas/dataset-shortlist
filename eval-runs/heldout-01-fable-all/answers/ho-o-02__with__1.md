Nothing I found is a ready-made open file that fully fits, but two options are close to immediate: the Veneto Workers Histories (a signed form, likely days) and Chile's public unemployment-insurance samples (public release, though I could not open the download page today). Everything else takes an institution-signed application and weeks to months. All access facts below were checked on 12 November 2026 unless marked "from memory".

## What I assumed you need

- **R1 (must):** a worker identifier plus an employer identifier shared across workers.
- **R2 (must):** workers followed across employers for 10+ years.
- **R3 (must):** earnings per job and period.
- **R4 (important for your question):** all or most coworkers observed in each firm. A within/between-firm variance split needs firm-level wage distributions, and files that sample *workers* (Spain, Chile, France, UK) show only one or two people in most firms.
- **R5 (nice to have):** reachable by a PhD student without residence or a co-author in the country.

## Shortlist

| # | Dataset | Access | Licence / terms | Size and span | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Veneto Workers Histories (Italy) | Signed form e-mailed to the foundation; likely days | Citation requirement; form terms not read | All private-sector firms and workers in the covered area, 1975–2001 | Strong, but ends 2001 | Today |
| 2 | SIEED (Germany, IAB) | Institutional agreement, on-site then remote execution; 1–3 months | Data use agreement | 1% of establishments, all their workers, 1975–2023 | Strong | Today |
| 3 | MCVL (Spain) | Application by your institution; weeks (from memory) | Non-commercial research, credit and send outputs | About 4% of individuals (from memory), full histories | Partial (worker sample) | Today |
| 4 | Seguro de Cesantía samples (Chile) | Public download per the regulator's press releases; minutes if the page works | None stated | 3%, 5% or 12% of affiliates, 2002 onward | Partial (worker sample) | Partly: download page failed |
| 5 | Quadros de Pessoal via BPLIM (Portugal) | Application plus confidentiality agreement; may need a Banco de Portugal co-author; months | Scientific use only, no fee | Universe of firms and employees, mid-1980s onward (from memory) | Strong | Access today, content from memory |
| 6 | Panel tous salariés (France, CASD) | Committee approval, institutional contract, paid secure terminal; months | Contract with CASD | 1/24 of workers to 2001, 1976–2022 | Partial (worker sample) | Today |
| 7 | LEHD (US Census) | Proposal, background check, secure data centre; 6–12 months | Title 13/26 confidentiality | Near-universe of US jobs | Strong | Today, timeline from search |
| 8 | RAIS identificada (Brazil) | Cooperation agreement between an institution and the ministry; months | Confidentiality term per user | Universe of formal jobs | Strong | Today (via search) |
| 9 | LIAB longitudinal (Germany, IAB) | As SIEED | Data use agreement | 1975–2024 | Partial | Today |
| 10 | Admin3 (Hungary, KRTK) | Only with a KRTK co-author or supervisor | Server access only | Population sample, 2003–2017 | Partial | Today (via search) |
| 11 | ASHE (UK) | Accredited researcher, secure lab; months | Secure access | 1% of employees, 1997–2025 | Partial (worker sample) | Search only; checker could not read the catalogue |

## Details

**1. [Veneto Workers Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)**
- **Contents:** three Stata files (workers, firms, yearly contribution records) from Italian social-security archives, 1975–2001.
- **Access:** the page says "fill and sign the attached form and send it to info@frdb.org". [Arellano-Bover's user notes](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources) say a copy "can easily be obtained" this way.
- **Gaps:** it ends in 2001, so it covers a historical rise in inequality only. The foundation's page says the provinces of Treviso and Vicenza, while papers describe the whole Veneto region; ask which extract you get. The page does not list earnings variables (from memory: annual earnings and days or weeks paid per job).
- **Used by:** [Kline, Saggio and Sølvsten](https://arxiv.org/pdf/1806.01494) for bias-corrected AKM variance decompositions, and [Card, Devicienti and Maida](https://davidcard.berkeley.edu/papers/RESTUD-2014.pdf).

**2. [SIEED 7523](https://fdz.iab.de/en/int_bd_pd/the-sample-of-integrated-employer-employee-data-sieed-sieed-7523-version-1/)**
- **Why it fits:** it holds "the entire employment biographies of all people ever employed in the sampled establishments", so whole workforces are visible.
- **Access** ([on-site use page](https://fdz.iab.de/en/data-access/on-site-use/)): a request form, a check that "could take up to one month", then a use agreement signed by your institution. For thesis work "the supervising chair must submit the application".
- **Where you work:** on site at a guest location (Germany, USA, Canada, UK), then by submitting code remotely. Remote desktop is limited to institutions in Germany. No fee is mentioned.
- **Gaps:** wages are top-coded at the social-security ceiling and there are no hours (from memory).
- **Used by:** [Card, Heining and Kline (2013)](https://doi.org/10.1093/qje/qjt006), which is the template for your question on the same underlying data.

**3. [MCVL](https://portaldatos.seg-social.gob.es/mcvl)**
- **Contents:** anonymised Spanish social-security histories, with each spell tied to an employer's contribution account code and monthly contribution bases.
- **Access:** open to "instituciones públicas y privadas que lo soliciten" for non-commercial research. Your university submits the form and researcher sheet, and the social-security directorate approves.
- **Gaps:** contribution bases are capped unless you take the tax-data version (from memory). Whether non-Spanish universities qualify is not stated on the page; from memory, foreign universities have obtained it.
- **Also there:** the same portal lists a firm–worker panel (PET) that I did not check and that may suit R4 better.

**4. [Chile Seguro de Cesantía samples](https://www.spensiones.cl/portal/institucional/594/w3-article-7521.html)**
- **Contents:** monthly contribution histories for sampled affiliates, with workers and employers under consistent anonymous numbers. The regulator's 2024 public account says the samples were refreshed that year.
- **Access:** the regulator says the samples are "a disposición del público" on its website. The download link in its press releases returned a 404 to my client, so open spensiones.cl in a browser and look under statistics and databases.
- **Gaps:** earnings are capped at the contribution ceiling, and early years cover only contracts started after 2002 (both from memory). Confirm the employer identifier in the variable dictionary before building on it.

**5. [Quadros de Pessoal via BPLIM](https://bplim.bportugal.pt/content/access-0)**
- **Access:** application form, project description, CV and a confidentiality agreement that your supervisor also signs. You work remotely on perturbed data and staff run the final code.
- **Catch:** a 2018 version of the lab's guide says this dataset is limited to Banco de Portugal researchers and their co-authors. Check the current Guide for Researchers before investing time.

**6. [Panel tous salariés](https://www.casd.eu/en/source/all-employee-panel/)**
- **Access:** apply through the confidential data access portal, get the producer's agreement and the Statistical Secrecy Committee's approval ([procedure](https://www.casd.eu/en/your-project/procedures-dhabilitation/)). Your institution's legal representative then signs a contract and pays for the secure terminal ([price list](https://www.casd.eu/en/tarifs-2/)).
- **Gaps:** I did not capture the fee amounts.

**7. [LEHD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)**
- **Access:** "researchers must have an approved project" and all work happens in a Federal Statistical Research Data Center.
- **Conditions (from data-centre slide decks found by search, 2018–2025):** advisor as co-principal investigator, about 4–6 months to approval and longer with tax-agency review, and US residency for 3 of the last 5 years.

**8. [RAIS identificada](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)**
- **Access:** requires a cooperation agreement between an institution and the labour ministry, plus a confidentiality term per user. The realistic route is a Brazilian co-author or host whose institution already has one.

**9–11.**
- **[LIAB](https://doi.org/10.5164/iab.liablm7524.de.en.v1):** same procedure as SIEED. Its page says full biographies of all employees are provided only "for establishments with up to 49 employees", so prefer SIEED unless you need the establishment survey.
- **[Admin3](https://adatbank.krtk.mta.hu/en/2020/02/):** open only to KRTK staff, their co-authors and students they supervise.
- **[ASHE](https://datacatalogue.ukdataservice.ac.uk/studies/study/6689):** needs UK accredited-researcher status and an approved project; from memory, access is from within the UK only.

## Known, not confirmed

- **LoSaI (Italy, national social-security worker sample, 1985 onward):** a labour-ministry [research proposal form](https://www.lavoro.gov.it/documenti-e-norme/studi-e-statistiche/Documents/Microdati%20per%20la%20ricerca/ALLEGATO3-microdati.pdf) exists, signed by the lead researcher and a recognised research body. I could not confirm that it carries a firm identifier; check the record layout.
- **VisitINPS (Italy, full social-security archives):** competitive programme with on-site work in Rome (from memory).
- **Austria (social-security database), Denmark, Sweden, Norway, Finland, Netherlands, Canada:** all have full-population linked registers (from memory). Access generally needs an affiliation or co-author at an approved institution in the country, often with fees. I did not check any of their pages today.
- **Cross-country overview:** [Boza and Pető (2025)](https://kti.krtk.hu/wp-content/uploads/2025/02/KRTKKTIWP202502.pdf) review linked employer-employee panels in 33 countries, with an appendix table on access for the European ones. I found it but did not read it.

## Not recommended, and why

- **Public RAIS files (Brazil):** open, but identifiers are removed, so workers cannot be followed.
- **[GRAPH-EE](https://doi.org/10.5255/ukda-sn-858769) (UK, 2007–2023):** open worker–firm panel built from web profiles; its description mentions no wage data.
- **[Synthetic Workplace and Employee Survey](https://doi.org/10.5683/sp3/abotie) (Canada):** open but synthetic, and each worker is followed for two years only (from memory).
- **US tax-record studies (Song et al.; [Lamadon, Mogstad and Setzler](https://doi.org/10.3886/e146661v1)):** the replication package is public, but from memory it has code and no microdata, and outsiders cannot request the records.
- **PSID, NLSY, SIPP:** no employer identifier shared across respondents (from memory).
- **EU Structure of Earnings Survey:** repeated cross-sections, no worker panel (from memory).

## What I could not find

- No open file combines worker and firm identifiers, uncapped earnings, whole firm workforces and recent years.
- The Chilean download page and variable dictionary could not be opened.
- Registry searches (DataCite, OpenAIRE, Zenodo, Hugging Face) returned almost nothing relevant beyond the German records, so most of this comes from the data owners' own pages.

## Next step

1. **This week:** send the Veneto form to info@frdb.org and try the Chilean download in a browser.
2. **Meanwhile:** build and test your AKM pipeline on simulated panels with [BipartitePandas / PyTwoWay](https://github.com/tlamadon/pytwoway), and on the free SIEED test data. The test data are random, so they are for code only.
3. **In parallel:** ask your advisor to start the German application for SIEED, since it is the best fit for a modern within/between-firm decomposition and the paperwork must come from the supervising chair.

The interactive shortlist, with filters and an exportable access plan, is at `/private/tmp/e-1FMVJG/home/cwd/dataset-shortlist.html`.