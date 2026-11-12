No dataset like this is openly downloadable. In every country I checked, the employer ID is exactly what gets removed from the public files, so every option below needs an application. The quickest are **Spain's MCVL** and the **Veneto worker histories** (a form, then probably weeks). Germany and Portugal take a few months. Brazil, the US and Hungary are slower or need a local partner. What you can start on **today** is your full AKM pipeline on simulated data with **pytwoway**, and on Germany's free practice files, which match the real LIAB layout.

Checked 2026-11-12. "Confirmed" means I read it on the data owner's page today; "from memory" means I couldn't confirm it.

## What I assumed you need
- **R1 (must):** a worker ID and an employer ID that are consistent across workers and years. Without both, you can't estimate firm effects from people who change jobs.
- **R2 (must):** earnings for each job spell.
- **R3 (must):** at least 10 years.
- **R6 (must):** a PhD student can get it. I assumed you may not be based in that country.
- **Nice to have:** near-complete coverage of a firm's workers, so many firms are connected through movers (R4), and earnings that aren't capped at a ceiling (R5).

## Shortlist
| # | Dataset | Access | Years | Fit | Checked |
|---|---|---|---|---|---|
| 1 | Spain: MCVL, 4% sample of social security records (Social Security agency) | Application, free, files sent to you; weeks | 1980s–present | Strong (small sample per firm) | today, plus some from memory |
| 2 | Germany: IAB LIAB longitudinal model | Application and agreement; code is run for you or on-site; months | 1975–2021/2024 | Strong | today |
| 3 | Portugal: Quadros de Pessoal, via Banco de Portugal's data lab (BPLIM) | Application, confidentiality agreement, secure remote server; months | mid-1980s onward | Strong | access rules today, contents from memory |
| 4 | Italy: Veneto Worker Histories (VWH) | Signed form emailed to the distributor; probably weeks | 1975–2001 | Strong, but old and regional | today |
| 5 | Brazil: identified RAIS | Cooperation agreement between an institution and the Labour Ministry; months | 1985–present | Strong | today |
| 6 | US: LEHD, through a Census research data center | Proposal, sworn status, several agency approvals; 6–12+ months | ~2000 onward | Strong | today |
| 7 | Germany: SIAB, on-site version | Same process as LIAB | 1975–2023 | Partial (2% worker sample) | today |
| 8 | Hungary: Admin3 (KRTK Databank) | Needs a KRTK coauthor | 2003–2017 | Partial | today |
| 9 | pytwoway simulated data | Open, `pip install` | any | For building code only | today |

## Details

**1. MCVL (Spain).** [portaldatos.seg-social.gob.es/mcvl](https://portaldatos.seg-social.gob.es/mcvl)
- **What it is:** a 4% random sample of everyone with any link to Spanish Social Security. Each person's full work history is included, back as far as computer records go. Monthly contribution earnings are included (confirmed on the portal). From memory, each job also carries an anonymised employer account and a firm tax ID.
- **How to get it:** download the application form and researcher form from the portal. Request the version **with tax data**, because the social security earnings are capped at the top and bottom and the tax data aren't. The Social Security directorate (DGOSS) approves requests from institutions doing non-commercial research.
- **Use this code:** [Diego Puga's MCVL code](https://diegopuga.org/data/mcvl/) for building the panel.
- **Watch out for:**
  - With 4% of workers, most firms have only 0–2 sampled employees. Firm effects will be noisy and the connected set small, so plan on bias-corrected (KSS-type) estimates.
  - Approval isn't automatic. Juan José Dolado reported two rejections in 2024 ([Nada es Gratis](https://nadaesgratis.es/dolado/pesadilla-con-el-pet)).
  - From memory, foreign universities can apply. Confirm this by email.

**2. LIAB longitudinal model (Germany).** [FDZ page](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)
- **What it is:** firms sampled through the IAB's annual firm survey, with complete employment histories of their workers.
- **Who can apply:** non-German researchers on the same terms as Germans. About half of current projects include collaborators abroad.
- **How you work with it:** you can't download it. You submit code that FDZ staff run for you (their remote-execution system, JoSuA), or you work on-site in Germany or at a guest site: Michigan, Berkeley, Harvard, Princeton, UCLA, Cornell, London, Essex, Vancouver ([locations](https://fdz.iab.de/en/appointment-locations-and-fdz-online-calendar/)).
- **Watch out for:**
  - Earnings are capped at the social security ceiling (imputation is standard).
  - The 7524 page says full employment histories are provided only for firms with fewer than 50 employees.
  - Sites outside the EU add extra anonymisation that can't be undone.
  - FDZ also publishes ready-made AKM firm effects you can merge in ([method report 03/2025](https://doku.iab.de/fdz/reporte/2025/MR_03-25_EN.pdf)).
- **Key paper:** Card, Heining & Kline (2013), [doi:10.3386/w18522](https://doi.org/10.3386/w18522).

**3. Quadros de Pessoal (Portugal).**
- **What it is (from memory):** a mandatory annual census of all private-sector employers and their workers, without an earnings cap. It's the data behind Card, Cardoso & Kline (2016).
- **How to get it (confirmed on [BPLIM's access page](https://bplim.bportugal.pt/content/access-0)):** application form, CV and confidentiality agreement. It's free and for research only. You build code on practice data, then work on BPLIM's external server. You can't transfer files yourself; outputs are sent to you by email.
- **Not confirmed:** whether outside researchers also need approval from the Labour Ministry, which supplies the data under a protocol ([2018 guide](https://cicee.autonoma.pt/wp-content/uploads/2024/03/BPlim_Guide_for_Researchers_v2018sep26.pdf)).

**4. Veneto Worker Histories (Italy).** [FRDB page](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- **What it is:** every private-sector firm in Treviso and Vicenza and all their workers, followed through their whole careers, 1975–2001.
- **How to get it:** sign the form on that page and email it to info@frdb.org. The page doesn't say who is eligible or how the data are delivered.
- **Watch out for:** it ends in 2001, so it says little about recent trends.
- **Key paper:** Kline, Saggio & Sølvsten's leave-out (KSS) method was developed on this data ([arXiv 1806.01494](https://arxiv.org/pdf/1806.01494)).

**5. Identified RAIS (Brazil).** [Request page](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)
- **What it is:** every formal job in Brazil, with worker and firm IDs.
- **How to get it:** the request must come from an *organisation*, not a person. It signs a cooperation agreement with the Labour Ministry's statistics office, and each user signs a confidentiality agreement.
- **In practice:** this is hard for a foreign university. It's worth asking whether your department or advisor already holds an agreement.

**6. LEHD (US).** [Census LEHD page](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)
- **What it is:** quarterly earnings for nearly all jobs in participating states, mostly from 2000 on, with no hours.
- **How to get it:**
  - A proposal through a Federal Statistical Research Data Center (FSRDC), with your advisor as co-PI. It must show a benefit to the Census Bureau.
  - Special Sworn Status, and approvals from the IRS and Social Security for some files.
- **Rules:** you must have lived in the US for 3 of the last 5 years, results must cover at least 3 states, and all work happens inside an FSRDC.

**7–8.** The on-site **SIAB** has the IDs but samples only 2% of workers, so it's weak for firm effects. **Admin3** is a 50% population sample with monthly employer links, but only for KRTK researchers and their coauthors. A newer Admin4 may offer wider access tiers.

**9. Start today.** [pytwoway](https://github.com/tlamadon/pytwoway):
- `pip install pytwoway`
- Simulate worker-firm data with chosen sorting and mobility using `bpd.SimBipartite`.
- Estimate AKM with plug-in, homoskedastic and KSS corrections using `tw.FEEstimator(he=True)`.
- Also download FDZ's free LIAB practice data in Stata format from the LIAB page. The values are random but the variables match the real data, so code written on it will carry over to remote execution.

## Known, not confirmed
- **Finland** (FOLK employment modules through the FIONA remote system): full-population data, but the agreement must be with a Finnish organisation and there are fees. The site blocked automated checks.
- **Not checked at all:**
  - Denmark, Sweden and Norway registers: these normally need a local institution.
  - France's DADS / Panel tous salariés, accessed through its secure research environment (CASD).
  - Austria's social security database (ASSD), UK ASHE, Canada CEEDD, Italy's INPS programme for visiting researchers (VisitINPS), Taiwan, Chile, Mexico (IMSS).

## Not recommended
- **PSID and NLSY:** employer IDs aren't shared across respondents, so firm effects can't be estimated.
- **SIAB download version and public RAIS:** both are free, but neither has employer IDs that link workers.

## Next step
1. This week, build the pipeline on pytwoway simulated data.
2. Submit the MCVL application (with tax data) and the VWH form now. Both are cheap.
3. Start the FDZ LIAB application with your advisor, since it's the strongest long-run option. If Portugal is attractive, write to BPLIM at the same time to ask about Quadros de Pessoal terms for outside researchers.

Interactive page: `/private/tmp/e-jvrm6C/home/cwd/dataset-shortlist.html` (data in `dataset-scout/shortlist.json`)

Sources: [MCVL portal](https://portaldatos.seg-social.gob.es/mcvl) · [FDZ access](https://fdz.iab.de/en/data-access/on-site-use/) · [FDZ locations](https://fdz.iab.de/en/appointment-locations-and-fdz-online-calendar/) · [SIAB](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/) · [SIAB guide](https://labourmarketresearch.springeropen.com/articles/10.1186/s12651-020-00275-9) · [BPLIM](https://bplim.bportugal.pt/content/access-0) · [FRDB VWH](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/) · [RAIS identified](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged) · [LEHD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html) · [FSRDC guidelines](https://www2.census.gov/adrm/FSRDC/Apply_For_Access/Research_Proposal_Guidelines.pdf) · [KRTK Admin3](https://adatbank.krtk.mta.hu/en/2020/02/) · [KRTK WP 2026/01](https://kti.krtk.hu/wp-content/uploads/2026/02/KRTKKTIWP202601.pdf) · [FIONA](https://stat.fi/en/services/services-for-researchers/instructions-for-researchers/using-the-datasets/fiona-remote-access-system) · [pytwoway](https://github.com/tlamadon/pytwoway) · [Puga MCVL code](https://diegopuga.org/data/mcvl/) · [Nada es Gratis](https://nadaesgratis.es/dolado/pesadilla-con-el-pet)