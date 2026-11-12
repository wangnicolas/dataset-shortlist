There is one real dataset you can probably hold within days to weeks (Veneto Worker Histories), one that may be downloadable today (Chile's unemployment insurance sample), and a serious long-run option whose application you should start now (German IAB data). I checked the access pages for those three today; the "from memory" rows below are from my own knowledge and need checking before you rely on them.

## Options, ranked by how fast you could be working

| Data | What it is | What access takes | Fit for an AKM decomposition |
|---|---|---|---|
| **Veneto Worker Histories (Italy)** | Social security records, 1975–2001; all private-sector employees of firms in the covered area, with workers followed when they leave it | Sign a form and email it to Fondazione Rodolfo Debenedetti; the page lists no fee or eligibility test, and you get the files themselves | Good. A standard AKM dataset, but it ends in 2001 and covers one region |
| **Chile Seguro de Cesantía sample** | Public anonymised samples of 3%, 5% and 12% of affiliates, combinable to 20%, updated yearly | Download from the Superintendencia de Pensiones | Uncertain. A worker sample, and I could not confirm the employer ID (see below) |
| **Spain MCVL** | 4% sample of people in social security records, with full work histories and anonymised firm IDs (from memory) | Institutional application to Seguridad Social for non-commercial research; I found no nationality rule, but could not confirm that foreign institutions qualify | Moderate. A worker sample, with capped earnings unless you get the tax-data version |
| **Italy LoSaI** | Roughly 7% sample of private-sector workers, 1985–2016 | Research proposal to the Ministry of Labour, signed by you and your institution's data contact, plus confidentiality declarations | Moderate. Again a worker sample |
| **Germany IAB (SIEED, LIAB)** | SIEED: 1% of establishments with all their workers' full biographies, 1975–2023 | Project application and a contract with your institution; no scientific use file, so on-site or remote execution only | Very good. Establishments rather than firms, and wages are top-coded |
| **Portugal Quadros de Pessoal** | Annual census of private-sector firms and their workers, uncapped wages (from memory) | Accreditation through Statistics Portugal or the Banco de Portugal microdata lab | Excellent if you can get in; easiest with a Portuguese coauthor |
| **France DADS panel** | Long worker panel from payroll declarations (from memory) | Confidentiality committee approval, then a paid secure-access device from CASD; expect months | Good, but a worker sample |
| **US LEHD** | Near-universe state unemployment insurance records | Census research data centre proposal, security clearance, usually a year or more; hard for non-US nationals (from memory) | Excellent, but not a second-year starting point |
| **Nordic registers, Netherlands** | Full population registers | Usually a local institutional affiliation or host, plus fees (from memory) | Excellent with a local coauthor |
| **Brazil RAIS** | Universe of formal jobs | The identified version needs a ministry agreement or an insider coauthor (from memory) | Excellent, but the public version has no worker IDs, so it is useless for AKM |

## Details that change the decision

- **Veneto coverage:** the foundation's page says Treviso and Vicenza provinces only, while one recent paper citing the same page reports all seven Veneto provinces. Ask which version you are getting when you apply.
- **Chile employer ID:** a press release says tax IDs of natural and legal persons are replaced with sequential numbers, which suggests an anonymised employer ID. I could not open the codebook, and the portal link I found returned a 404 today, so check this first.
- **Worker samples:** in a 4–20% sample of workers, most firms have too few observed movers, so firm effects are noisy and the between-firm variance is biased upward. Plan on a bias-corrected estimator such as the Kline–Saggio–Sølvsten leave-out method.
- **IAB from outside Germany:** remote desktop is limited to institutions based in Germany. The US has six on-site locations (Ann Arbor, Berkeley, Harvard, Cornell, Los Angeles, Princeton), but US, Canadian and UK sites are closed to stays under nine months. Remote job submission (JoSuA) is the fallback, and it is slow because you only see vetted output.
- **IAB shortcuts:** test data for SIEED is downloadable so you can write code before approval. The IAB also publishes pre-estimated AKM person and establishment effects (1985–2023) that merge into its datasets.

## What I would do

1. **This week:** send the Veneto form. It gives you a real, widely used AKM dataset to build and debug the whole pipeline on, and replication of published variance decompositions as a check.
2. **In parallel:** start the IAB application for SIEED with your advisor, since the contract with your institution is the slow part. This is the data most likely to carry a paper on rising inequality, because it runs to 2023.
3. **If you need recent years quickly:** check the Chilean codebook for the employer ID, and apply for MCVL or LoSaI depending on where your institution sits.

Veneto alone will not answer a question about the recent rise in inequality, since it stops in 2001. Tell me where your institution is and I can narrow the list, because eligibility for most of these runs through the institution.

Sources:
- [FRDB: Veneto Workers Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- [FDZ-IAB: SIEED 7523](https://fdz.iab.de/en/int_bd_pd/the-sample-of-integrated-employer-employee-data-sieed-sieed-7523-version-1/)
- [FDZ-IAB: on-site use and remote data access](https://fdz.iab.de/en/data-access/on-site-use/)
- [FDZ-IAB: locations](https://fdz.iab.de/en/appointment-locations-and-fdz-online-calendar/)
- [FDZ-Methodenreport 03/2025: AKM effects](https://doku.iab.de/fdz/reporte/2025/MR_03-25_EN.pdf)
- [Superintendencia de Pensiones: 12% sample release](https://www.spensiones.cl/portal/institucional/594/w3-article-12931.html)
- [Superintendencia de Pensiones: anonymised samples](https://www.spensiones.cl/portal/institucional/594/w3-article-7521.html)
- [Seguridad Social: MCVL portal](https://portaldatos.seg-social.gob.es/mcvl)
- [Ministero del Lavoro: microdata research proposal form](https://www.lavoro.gov.it/documenti-e-norme/studi-e-statistiche/Documents/Microdati%20per%20la%20ricerca/ALLEGATO3-microdati.pdf)
- [LoSaI description](https://www.disuguaglianzesociali.it/glossario/?idg=71)