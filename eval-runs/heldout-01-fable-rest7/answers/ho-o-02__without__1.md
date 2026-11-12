**Nothing fully adequate is downloadable today, but two datasets are within weeks of a signed form, and one of them (Veneto) is the standard AKM testbed.** I checked the access pages where I could; items I could not confirm are marked.

## Start now

- **Veneto Worker Histories (Italy, 1975–2001).** It has worker and firm IDs and all workers in covered firms, and was used by Card–Devicienti–Maida (2014) and Kline–Saggio–Sølvsten (2020). You email a signed form to Fondazione Rodolfo Debenedetti; the page lists no fee or eligibility rules. Its page describes coverage as Treviso and Vicenza provinces, while the papers describe all of Veneto, so ask which version you get. It ends in 2001 and is one region.
- **Chile unemployment insurance samples.** The pensions regulator publishes anonymised 3%, 5% and 12% worker samples with monthly records per employment relationship and sequential firm IDs. The download link I found returned a 404, and I could not confirm the firm ID tracks across employers, so check the codebook first.
- **IAB test data (Germany).** Fake-content files with the real structure are freely downloadable for SIEED and LIAB. They are useless for results, but you can write and debug your whole pipeline while an application is pending.

## Options requiring an application

| Data | What it takes | Fit for your question |
|---|---|---|
| **Germany, IAB SIEED / LIAB** (1975–2023) | Free; your institution signs the contract; document check takes up to a month. A guest stay comes first, then remote job submission. US, Canadian and UK sites require a nine-month minimum stay. A third-party source says students cannot apply alone, so expect your advisor to be the applicant. | Best realistic option. SIEED samples establishments and keeps all their workers. Pre-estimated AKM effects can be added on request. Wages are top-coded. |
| **Spain, MCVL** (2004 onward, with retrospective histories) | Free; institutional application for a defined scientific project; forms in Spanish. I could not confirm rules for foreign institutions. | 4% worker sample, so few coworkers per firm. |
| **US, LEHD** | Census proposal with your advisor as co-PI, showing a benefit to Census. Clearance alone adds 3–4 months after approval. Non-citizens need three of the last five years in the US. Work is done in a secure data centre. | Excellent data, but plan on a year or more before first results. |
| **Brazil, identified RAIS** | Formal cooperation agreement with the Ministry of Labor, or joining one your institution already holds. | The public RAIS files lack worker identifiers, so they cannot be used. |
| **Portugal, Quadros de Pessoal** | Through Banco de Portugal's microdata lab, apparently restricted to Bank researchers and their collaborators (2018 guide, possibly outdated). | Realistically needs a Portuguese co-author. |
| **Italy, LoSaI** | Research proposal to the Ministry of Labour. | Roughly 7% worker sample; I could not confirm it carries a usable firm identifier. |

From memory, not checked this session: the Nordic registers, the Netherlands, France and Austria generally require a local affiliation or accredited institution, usually with fees. Ask your advisor before ruling them out.

## Design constraint

Worker-based samples (MCVL, LoSaI, Chile) are weak for your decomposition. With only a few sampled workers per firm, firm mean wages are noisy and the between-firm share is overstated. Firm effects are also identified off few movers, which inflates their variance. Prefer data with all workers in a firm (Veneto, SIEED, LEHD), and plan on a bias-corrected estimator such as the Kline–Saggio–Sølvsten leave-out method either way.

## Recommendation

1. Send the Veneto form this week and build the full AKM and decomposition pipeline on it.
2. Ask your advisor and department whether anyone already holds an IAB, LEHD or RAIS agreement you can join. This is the fastest route to the big datasets.
3. Start the IAB SIEED application in parallel as the dataset for the actual paper, since it covers the period when German inequality rose.

Sources:
- [fRDB: Veneto Workers Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- [Arellano-Bover: VWH additional resources](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources)
- [Superintendencia de Pensiones: sample announcement](https://www.spensiones.cl/portal/institucional/594/w3-article-12931.html)
- [LSE working paper on Chilean UI data](https://eprints.lse.ac.uk/107824/1/LSE_III_working_paper_54.pdf)
- [Journal of Development Studies article on Chilean UI data](https://www.tandfonline.com/doi/full/10.1080/00220388.2022.2096444)
- [FDZ IAB: SIEED 7523](https://fdz.iab.de/en/int_bd_pd/the-sample-of-integrated-employer-employee-data-sieed-sieed-7523-version-1/)
- [FDZ IAB: LIAB longitudinal model](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)
- [FDZ IAB: on-site use and remote data access](https://fdz.iab.de/en/data-access/on-site-use/)
- [AKM Effects for German Labour Market Data](https://www.degruyterbrill.com/document/doi/10.1515/jbnst-2023-0018/html)
- [MCVL portal](https://portaldatos.seg-social.gob.es/mcvl)
- [Diego Puga: MCVL code and guide](https://diegopuga.org/data/mcvl/)
- [Census FSRDC proposal guidelines](https://www2.census.gov/adrm/FSRDC/Apply_For_Access/Research_Proposal_Guidelines.pdf)
- [Census restricted-use application process](https://www.census.gov/topics/research/guidance/restricted-use-microdata/standard-application-process.html)
- [Atlanta Fed RDC data page](https://www.atlantafed.org/research-and-data/atlanta-research-data-center/data)
- [clean_RAIS repository](https://github.com/rdahis/clean_RAIS)
- [Explainer on public RAIS](https://marianahaase.substack.com/p/rais-publica-que-os-micridados-permitem)
- [BPLIM access](https://bplim.bportugal.pt/content/access-0)
- [BPLIM Guide for Researchers (2018)](https://cicee.autonoma.pt/wp-content/uploads/2024/03/BPlim_Guide_for_Researchers_v2018sep26.pdf)
- [Glossary entry on LoSaI](https://www.disuguaglianzesociali.it/glossario/?idg=71)
- [Kline, Saggio, Sølvsten: Leave-out estimation](https://www.nber.org/system/files/working_papers/w26244/w26244.pdf)