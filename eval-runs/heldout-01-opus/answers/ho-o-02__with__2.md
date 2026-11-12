Short answer: no openly downloadable linked employer-employee panel with real data exists in any country. You can start building and testing your AKM code today on simulated data and the IAB test files. The fastest real data are the **Veneto Worker Histories** and Spain's **MCVL** (a simple request form, probably a few weeks). Germany's **SIEED** is the best fit if you can wait a few months. Checked on 12 Nov 2026.

## What I assumed you need
- **R1 (must):** worker and employer identifiers that persist over time, so you can follow movers between firms.
- **R2 (must):** earnings for each job spell.
- **R3 (must):** at least 10 years of panel.
- **R4 (nice to have):** enough coverage that the connected set is large. Ideally that means nearly all workers, or all workers at the sampled firms.
- **R5 (nice to have):** a PhD student at a non-local institution can get it, ideally by remote access. I assumed you are not based in any of these countries. If you are, that country's registers jump up the list.

## Shortlist
| # | Dataset | Access | Size / coverage | Fit | Checked |
|---|---|---|---|---|---|
| 1 | **IAB SIEED** (Germany, 1975–2023) | Application to the IAB research data centre (FDZ) plus a use agreement signed by your institution. You run code remotely or on-site, never download. ~2–4 months | Full job histories of every worker ever employed at a ~1–1.5% sample of establishments | Strong | today |
| 2 | **MCVL** (Spain, 1980s–today) | Free request form to the Social Security directorate (DGOSS); you receive the data files. ~weeks | 4% of everyone with a Social Security record, with employer account codes | Strong (sample thin for firm effects) | today (eligibility of foreign institutions: from memory) |
| 3 | **Veneto Worker Histories** (Italy, 1975–2001) | Signed form emailed to the Fondazione Rodolfo Debenedetti (fRDB). ~weeks | All private firms in two provinces, with each worker followed wherever they move | Strong, but ends in 2001 | today |
| 4 | **Quadros de Pessoal via BPLIM** (Portugal, 1985–) | Application, confidentiality agreement signed by you and your supervisor, and CV. Free. BPLIM runs your code on the real data. May need a Banco de Portugal co-author. ~months | Nearly all private-sector workers and firms | Strong | today (co-author rule from a 2018 guide) |
| 5 | **Admin3 / Admin4** (Hungary, 2003–2017) | Only for researchers at the research centre that hosts it (KRTK), their co-authors, or PhD students they supervise. The new Admin4 has a remote level worth checking | 50% of the population, monthly | Strong | today |
| 6 | **US LEHD** via a Census research data centre | Proposal to Census with IRS and SSA approval, then security clearance. ~6–18 months | Nearly all workers, for participating states | Strong | today (timeline from memory) |
| 7 | **France: Panel tous salariés / DADS / BTS** via CASD | Approval by France's statistical secrecy committee, then paid access through CASD. Probably needs a French host | Panel covers 1/12 of workers | Strong | partly today |
| 8 | **UK ASHE** (SN 6689; NES back to 1975) | UK Data Service Secure Lab: Safe Researcher training plus an institutional application | 1% of workers | Partial: connected set too small | today |
| 9 | **Brazil RAIS identificada** | Formal cooperation agreement with the Labour Ministry, in practice through a Brazilian institution | All formal jobs since 1985 | Strong, hard to get | today |
| 10 | **Finland, FIONA remote access** | Agreement always goes through a Finnish organisation; per-module fees | Full population | Strong | partly (site unreachable today) |

## Details
**1. SIEED (Germany).** [Product page](https://fdz.iab.de/en/our-data-products/integrated-establishment-and-individual-data/sieed/). This is the dataset most clearly built for AKM-style work. For each sampled establishment it has the full job histories of everyone who ever worked there, plus the IAB's establishment panel. Access is "On-site Use / Remote Desktop Access including Remote Execution". The data centre has sites in the USA, UK and Canada and a remote-execution system called JoSuA. [Test data](https://doku.iab.de/fdz/siab/SIAB_Testdaten_en.pdf) let you write your code in advance.
- **Limits:** wages are top-coded at the social security ceiling, so you have to impute. You only see moves between sampled establishments. The full-population data used by Card, Heining and Kline (2013) requires a much heavier special project.
- **Alternative:** the related LIAB dataset is another German option on the same route.

**2. MCVL (Spain).** [Portal](https://portaldatos.seg-social.gob.es/mcvl).
- **Contents (portal, today):** each job spell is tied to an employer "código de cuenta de cotización". Contribution bases are recorded "mes a mes … a lo largo de su vida laboral" (month by month over the working life). A version with tax data adds uncensored earnings.
- **Who can apply:** public and private institutions, for non-commercial scientific use, free of charge. Juan José Dolado wrote in 2024 that some MCVL requests had been rejected that year.
- **Not confirmed:** whether institutions outside Spain qualify. Many non-Spanish researchers have used it, but that is from memory. Email DGOSS before you rely on it.
- **Limits:** with only 4% of workers you see few coworkers per firm. Plan on grouped firm effects (the BLM clustering approach) or keep to large firms.
- **Help:** [Diego Puga's MCVL code](https://diegopuga.org/data/mcvl/).
- **Related:** the same portal offers a firm-worker panel (PET) and remote research rooms.

**3. Veneto Worker Histories (Italy).** [fRDB page](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/). The only step is to "fill and sign the attached form and send it to info@frdb.org". The data are Italian social security records with worker and firm IDs and contract-level earnings. Kline, Saggio and Sølvsten used it for their [leave-out AKM estimator](https://arxiv.org/pdf/1806.01494). Jaime Arellano-Bover keeps [practical notes](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources). The catch is that it ends in 2001.

**4. Quadros de Pessoal (Portugal).** [BPLIM access page](https://bplim.bportugal.pt/content/access-0). This is the data behind Card, Cardoso and Kline (2016). Outside researchers write code on pseudo-data and BPLIM staff run it on the real data. A [2018 guide](https://cicee.autonoma.pt/wp-content/uploads/2024/03/BPlim_Guide_for_Researchers_v2018sep26.pdf) limits QP to Banco de Portugal researchers and joint projects with them. Check the current Guide for Researchers.

**5–10.** Sources for the rest:
- Hungary: [Admin3 page](https://adatbank.krtk.mta.hu/en/2020/02/) and the [Admin4 working paper](https://kti.krtk.hu/wp-content/uploads/2026/02/KRTKKTIWP202601.pdf)
- US: [LEHD restricted data](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html). Proposals must state a benefit to the LEHD programme.
- France: [CASD record](http://datapresentation.casd.eu/10.34724/CASD.21.5012.V1)
- UK: [ASHE catalogue entry](https://datacatalogue.ukdataservice.ac.uk/studies/study/6689). The tool could not check this page automatically.
- Brazil: [gov.br request page](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)
- Finland: [FIONA guide](https://guides.stat.fi/remote-access-to-research-data/application-process-and-agreement-practices)

## What you can start today
- **[PyTwoWay](https://github.com/tlamadon/pytwoway/) / [BipartitePandas](https://github.com/tlamadon/bipartitepandas).** `pip install pytwoway`. It simulates worker-firm data with known true effects and runs AKM with standard bias corrections (KSS, BLM). Build and validate your whole within/between decomposition on it. [The ABC of AKM](https://lamadon.com/paper/akm-abc.pdf) is a good companion.
- **IAB test data.** Write your code in the format the German research data centre expects, so it runs on SIEED as soon as you are approved.
- **This week:** email fRDB for the Veneto data and DGOSS for the MCVL. Both are cheap, and Veneto in particular gives you real data on a full set of firms within weeks.

## Not recommended
- **Public RAIS (Brazil):** no worker or firm identifiers.
- **PSID, NLSY, SOEP:** no coworker structure, so firm effects can't be identified.
- **LEHD public products (QWI, LODES):** aggregate tables only.
- **SIAB:** a 2% sample of workers, which makes the connected set too thin. Use SIEED or LIAB instead.

## What I could not check
- Whether the MCVL accepts foreign institutions (the portal blocked direct reading).
- Whether foreign researchers can use the French data.
- Austria (the ASSD and the new Austrian Micro Data Center), Denmark, Norway, Sweden, the Netherlands and Canada (CEEDD), apart from a quick search on Austria that didn't settle anything. From memory, all of them need an institution based in that country.

## Next step
For the dissertation, aim for **SIEED** (or Portugal's QP if a Banco de Portugal co-author is realistic) for the main analysis. Use **Veneto** or **MCVL** to get going within weeks, and develop on PyTwoWay in the meantime. Talk to your advisor early, because the German, Portuguese and Hungarian routes all go faster with an institutional agreement or a co-author.

I've saved an interactive version of this shortlist, with filters and an exportable access plan, at `/private/tmp/e-qPJ7dL/home/cwd/dataset-shortlist.html`.

Sources: [MCVL portal](https://portaldatos.seg-social.gob.es/mcvl) · [Dolado, Nada es Gratis](https://nadaesgratis.es/dolado/pesadilla-con-el-pet) · [FDZ SIEED](https://fdz.iab.de/en/our-data-products/integrated-establishment-and-individual-data/sieed/) · [FDZ access](https://fdz.iab.de/en/data-access/on-site-use/) · [fRDB VWH](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/) · [BPLIM access](https://bplim.bportugal.pt/content/access-0) · [KRTK Admin3](https://adatbank.krtk.mta.hu/en/2020/02/) · [LEHD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html) · [CASD BTS](http://datapresentation.casd.eu/10.34724/CASD.21.5012.V1) · [UKDS ASHE](https://datacatalogue.ukdataservice.ac.uk/studies/study/6689) · [RAIS identificada](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged) · [Statistics Finland FIONA](https://guides.stat.fi/remote-access-to-research-data/application-process-and-agreement-practices) · [PyTwoWay](https://github.com/tlamadon/pytwoway/)