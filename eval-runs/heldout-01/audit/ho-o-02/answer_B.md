I found no open or free-download dataset that lets you follow workers across firms with firm identifiers. Every usable option needs an application, and the realistic ones take weeks to months. Search results from the data registries were mostly noise, so the access facts below come from the agency pages (checked 2026-11-12) unless I say "from memory".

## What I assumed you need
- **R1:** a panel of at least 10 years.
- **R2:** a worker ID and a firm ID on every job spell.
- **R3:** enough job movers to give a large connected set.
- **R4:** wages or earnings for each job.
- I assumed any country is fine, that you can wait for an application, and that you have no affiliation with a particular country's institutions.

## Shortlist
| # | Dataset | Access | Size / span | Fit | Checked |
|---|---|---|---|---|---|
| 1 | [MCVL (Spain)](https://portaldatos.seg-social.gob.es/mcvl) | Application, free, non-commercial research; weeks | Worker sample, annual waves (from memory: 4% sample, since 2004) | Strong on R1–R3; earnings are capped | Today (page); sample size from memory |
| 2 | [LIAB (Germany)](https://fdz.iab.de/en/our-data-products/integrated-establishment-and-individual-data/liab/) | Application, on-site or remote desktop with vetted output; weeks to months | Daily biographies 1975–2024 | Strong, but selective sample | Today |
| 3 | [SIAB (Germany)](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/) | The downloadable file needs a use agreement; the version with establishment IDs is on-site or remote only | Biographies from 1975 | Partial | Today |
| 4 | [Veneto Worker Histories (Italy)](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/) | Signed form emailed to the foundation that distributes it; weeks | 1975–2001 | Good for methods, but ends in 2001 | Today |
| 5 | [Admin3 (Hungary)](https://adatbank.krtk.mta.hu/en/2020/02/) | Data request form; tied to KRTK researchers; months | 2003–2017 | Strong data, hard to access | Today, partly |
| 6 | [LEHD (US)](https://lehd.ces.census.gov/data/) | Research data center proposal; 6–12+ months | Quarterly earnings, state-based | Strong, slow | Today |
| 7 | [Statistics Denmark IDA](https://dst.dk/en/TilSalg/Forskningsservice/Dataadgang/Autorisering) | Needs a Danish host institution; months | From memory: from 1980 | Strong, but needs a host | Access today, coverage from memory |

## Details
- **MCVL (Spain), my pick for a second-year student.** Institutions that justify non-commercial research can request it, and the Social Security data portal has an online form. A directorate there must approve it, and one academic source mentions about 11 forms (it may have changed). Employer episodes are identified by the employer's social-security account code. Contributions are capped, which understates the top of the distribution, and that matters for rising inequality. You must cite the directorate and send them your outputs. Research rooms in Madrid, Barcelona and Albacete are an alternative. The weeks-level timing is my estimate, not something I confirmed.
- **LIAB (Germany).** Workers come from firms in the IAB Establishment Panel. Firms with up to 49 employees contribute all workers, and larger firms contribute a 20% sample. You pick one base period per project (1993–2000, 2000–2007, 2007–2017 or 2014–2024). The biographies run 1975–2024. The page says the FDZ will provide AKM effects for 1985–2023 on request, which is a useful check on your own estimates. The page doesn't say whether researchers abroad can use it (the FDZ's international network, IDAN, may be the route), so email the FDZ before you plan around it.
- **SIAB (Germany).** The page says the downloadable file has no establishment identifiers, so you can't run AKM on it. The version that has them is on-site or remote only. The 2% sample size is from memory.
- **Veneto (Italy).** The foundation's page says to "fill and sign the attached form" and email it. It has worker and firm files with firm tax codes. A 2018 INPS paper says access is free. It stops in 2001, so it can't speak to recent inequality trends. It does give you full AKM data to build and test your code.
- **Admin3 (Hungary).** The page describes it as 2003–2017, with a successor database (Admin4) described in a 2026 working paper. The access pages suggest you need a KRTK researcher as co-author or supervisor, and the same pages cover several datasets, so confirm the Admin3 terms.
- **LEHD (US).** You work in a secure research data center after Census approval, and the proposal must show a benefit to Census. A regional center's page quotes 6–12 months or more.
- **Denmark IDA.** The statistics office only authorises Danish institutions, so foreign researchers need a Danish host.

## Known, not confirmed
I only searched the web for these and have no verified record.
- **Finland (FLEED).** Population-wide employer-employee data. Foreign access is possible, but remote access needs a Finnish affiliation and business data are often on-site only (old source).
- **Sweden (MONA).** Online remote platform. I found no current rules for foreign researchers.
- **Norway.** The remote system serves researchers with a Norwegian ID.
- **Canada (CEEDD).** Access through Statistics Canada's research data centers or its Centre for Data Development and Economic Research. Researchers cover the full cost (older source).
- **Portugal (Quadros de Pessoal).** Ask the labor ministry's planning office. I found no formal procedure. The Banco de Portugal route appears restricted to the bank's researchers (2018 guide).
- **France, Netherlands, Austria.** Not searched; from memory, restricted-access data exist for all three.

## Not recommended
- **Brazil public RAIS.** It is open, but de-identified, so you can't follow workers across years. The identified version needs a request to the Ministry of Labour and a cooperation agreement.
- **SIAB Campus File.** Free, but teaching only, with no publications allowed.
- **LEHD public aggregates (QWI, LODES, J2J).** No worker histories.
- **Replication packages for the Taiwan and Brazil AKM papers.** Useful as code, but the microdata are restricted. The pages blocked my automated checks.

## What I could not find
- An open worker-by-firm panel with identified firms.
- Current foreign-researcher rules for Sweden, Norway and Finland.

## Next step
**What you can start on today:**
1. Write and test your AKM pipeline on simulated worker–firm data: connected-set pruning, high-dimensional fixed effects, and variance decomposition with a bias correction for limited mobility (e.g. Kline–Saggio–Sølvsten). These tools exist from memory; I did not check them here.
2. Read the replication code from the Taiwan and Brazil papers.

**Applications:**
- Start the MCVL application now.
- In parallel, email the German research data center about LIAB access from abroad.
- Ask your advisor whether anyone has a Danish, Hungarian or US research data center link.

