No country lets you just download an identified, full-population panel of workers and their employers. Every real option needs an application. Two are close to immediate: the **Veneto Worker Histories** need only a signed form, and **Portugal's Quadros de Pessoal** (via the Banco de Portugal lab) is free and open to researchers anywhere, though approval takes longer. I checked access pages on 12 Nov 2026; where something is from memory, I say so.

## What I assumed you need
- **R1 (must):** worker and firm IDs, with enough job movers per firm for AKM. A thin random sample of workers gives few workers per firm, which makes firm effects noisy.
- **R2 (must):** at least 10 years of panel data.
- **R3 (must):** earnings, ideally with hours or days worked so you can build a wage rate.
- **R4 (nice to have):** close to the full population, so the connected set (firms linked through movers) is representative.
- **Assumption:** you're at a university outside the countries below. Your location changes who is eligible, so check that column first.

## Shortlist
| # | Dataset | Access | Time | Fit | Checked |
|---|---|---|---|---|---|
| 1 | Veneto Worker Histories (Italy, 1975–2001) | Signed form emailed to fRDB | Days | Strong (regional, ends 2001) | Today |
| 2 | Quadros de Pessoal via BPLIM (Portugal, mid-1980s on) | Application and confidentiality agreement; free; open to any country | Weeks to months | Strong: the canonical AKM dataset | Today (years from memory) |
| 3 | MCVL (Spain, 4% sample, full careers) | Request form; Social Security ministry (DGOSS) approves; free; files sent to you | Weeks | Strong, but a sample | Today |
| 4 | SIAB (Germany, 2% sample, 1975–2023) | Application; download only for institutions in Germany or the EU, otherwise on-site or remote execution | Weeks | Partial: sparse firms, wages capped | Today |
| 5 | LIAB longitudinal model 1975–2024 (Germany) | Application; on-site or remote | Months | Partial: firms are a sample | Today |
| 6 | Panel tous salariés (France, since 1976) | CASD secure access; secrecy committee approval and fees | Months | Strong | Page today, process from memory |
| 7 | ASHE (UK, 1% panel, 1997–2025) | Accredited researcher and Secure Lab project | Months | Partial | Via search |
| 8 | Identified RAIS (Brazil, every formal job) | Request to the labour ministry and a confidentiality agreement | Months, uncertain | Strong data, hard access | Today |
| 9 | LEHD (US) | Census research centre (FSRDC) proposal | 6–12+ months | Strong | Today |
| 10 | Finnish registers via FIONA (FOLK/FLEED; Nordic route) | Must be tied to a Finnish organisation; fees | Months | Strong | Via search (site blocked) |
| — | PyTwoWay simulated data; SIAB test data | Open download | Minutes | Pipeline building only | Today |

## Details
1. **[Veneto Worker Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)**
   - **What it covers:** all private-sector firms in Treviso and Vicenza, 1975–2001, plus the complete careers of everyone those firms employed.
   - **What you get:** a worker ID (`cod_pgr`) and a firm ID (`matr_az`), with annual earnings and days worked. There are no hours.
   - **Access:** the page says to "fill and sign the attached form and send it to info@frdb.org". You must cite Ca' Foscari / Tattara.
   - **Who used it:** [Card, Devicienti & Maida, ReStud 2013](https://doi.org/10.1093/restud/rdt030), with firm effects estimated on this data.
   - **Limits:** one region, and the data stop before 2001, so it can't track recent inequality. Still, it's the quickest real data for building and running your full pipeline.

2. **[Quadros de Pessoal via BPLIM](https://bplim.bportugal.pt/content/access-0)**
   - **What it covers:** a mandatory annual census of private employers and their employees.
   - **Access:** submit the application form. You and your supervisor sign the confidentiality agreement (the page says so explicitly for PhD projects). It's free.
   - **How you work:** on the lab's external server, or by sending code to run on the real data, written against practice datasets (not valid for research). You can't move files on or off the server; results come back by email after a check.
   - **Who used it:** Card, Cardoso & Kline (QJE 2016), from memory.
   - **Check:** the exact years (from memory, 1990 and 2001 are missing), and whether outside researchers get remote login or only remote execution.

3. **[MCVL](https://portaldatos.seg-social.gob.es/mcvl)**
   - **What it covers:** a 4% sample of everyone in Spanish Social Security, with complete careers and monthly contribution bases.
   - **What you get:** an employer account code for each job spell, and the data are delivered to you.
   - **Limits:** contribution bases are capped at the top and bottom; the version linked to tax data helps with that. A 4% sample means few workers per firm, so you'd need leave-out or KSS bias corrections.
   - **Access:** request form plus a form identifying each researcher, approved by DGOSS. Rejections do happen.
   - **Check:** I couldn't confirm whether institutions outside Spain are eligible; ask DGOSS directly.

4. **[SIAB scientific use file 7523](https://fdz.iab.de/en/pd_hd/factually-anonymous-version-of-the-sample-of-integrated-labour-market-biographies-siab-regionalfile-version-7523-v1/)**
   - **What it covers:** a 2% worker sample from the German social-security records, with establishment IDs. Daily wages are capped at the contribution ceiling, so you'd need to impute above it.
   - **Access:** a 2018 source says the downloadable file goes to institutions in Germany or the EU (§282(7) SGB III). Elsewhere, you'd use on-site access points (including in the US, UK and Canada) or remote execution.
   - **Note:** Card, Heining & Kline (2013) used the full records, which needs a dedicated project with the IAB.

5. **[LIAB 1975–2024](https://doi.org/10.5164/iab.liablm7524.de.en.v1)**
   - **What it covers:** links the IAB Establishment Panel to workers' employment histories.
   - **Limits:** the page says full worker histories are provided "only for establishments with up to 49 employees", and the firms are a sample, not the whole population.

6. **[Panel tous salariés (CASD)](https://www.casd.eu/en/source/all-employee-panel/)**
   - **What it covers:** employees since 1976, about 1 in 24 until 2001 and twice that from 2002.
   - **Access:** foreign institutions do get CASD projects; a Bocconi-hosted project uses this panel.
   - **Not confirmed today:** the process is from memory. Approval by France's statistical secrecy committee, institutional fees of several thousand euros a year, and remote work through a secure CASD terminal.

7. **[ASHE SN 6689](https://datacatalogue.ukdataservice.ac.uk/studies/study/6689)**
   - **What it covers:** a 1% panel by National Insurance number, with employer-reported pay and hours (very good wage quality) and business identifiers.
   - **Limits:** firm effects will be sparse at 1%.
   - **Access:** usually needs UK affiliation (from memory).

8. **[Identified RAIS](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)**
   - **What it covers:** every formal job in Brazil, with worker and firm IDs.
   - **Access:** you must sign a confidentiality agreement. In practice it usually goes through a Brazilian coauthor (from memory).

9. **[LEHD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)**
   - **Access:** an approved FSRDC project, with IRS and/or SSA approval for some files.
   - **Eligibility:** Census security clearance requires US citizenship, or 3 of the past 5 years in the US, plus a US affiliation.
   - **Limits:** results must use at least 3 states.

10. **Finland ([FIONA](https://stat.fi/en/services/services-for-researchers/instructions-for-researchers/using-the-datasets/fiona-remote-access-system))**
    - **Access:** "access agreement is always made with a Finnish organisation", and use is charged.
    - **Other Nordic countries:** Denmark (IDA) works the same way: access through an authorised Danish institution. From memory, Sweden and Norway are similar. The realistic route is a visiting position or a local coauthor.

## What you can start on today
- **[PyTwoWay](https://tlamadon.github.io/pytwoway/notebooks/fe_example.html):** simulates firm–worker networks and estimates AKM with the HO/HE bias corrections. Use it to build your connected-set, leave-out and decomposition code now.
- **SIAB test data:** Stata test files on the [weakly anonymous SIAB page](https://fdz.iab.de/en/pd_hd/weakly-anonymous-version-of-the-sample-of-integrated-labour-market-biographies-siab-version-7521-v1/). The values are random, but the structure is real, so your cleaning code will be ready when access comes through.
- **Veneto Worker Histories:** send the form this week. It's the only real data likely to arrive within days.

## Known, not confirmed
These weren't checked today, but the same kinds of routes exist (from memory):
- Austria: the Austrian Social Security Database.
- Italy: full INPS records through the VisitINPS Scholars programme (on-site in Rome), and the LoSaI sample. I found no official LoSaI access page.
- Canada: CEEDD, through Statistics Canada research centres.
- Australia: BLADE/PLIDA.
- New Zealand: IDI/LEED.

## Not recommended
- **Public RAIS:** has no worker ID, so you can't follow movers.
- **SIAB Campus File:** I mentioned it earlier as a quick option, but it's teaching data limited to people who started receiving unemployment benefit in 2005.
- **ASHE synthetic pilot (SN 9045):** going by its title it seems to cover only 2020; I couldn't open its contents.
- **PSID, NLSY, SOEP:** surveys with no shared firm IDs.

## Next step
1. Send the Veneto form, and start your pipeline on PyTwoWay simulated data.
2. Apply to BPLIM for Quadros de Pessoal. It's free, open to any country, has the best fit and the standard AKM literature, and your advisor's signature is part of the application anyway.
3. If you're at an EU institution, also apply for the SIAB file or the MCVL. Otherwise, look for a coauthor or visiting position for Nordic, French or Brazilian data.

Search coverage: the dataset registries found little beyond the German LIAB records, so most candidates came from memory plus web search, then were checked. The Finnish statistics site, ICPSR and the UK Data Service catalogue blocked the automated checks.

The interactive shortlist, with filtering and an exportable access plan, is at `/private/tmp/e-gDF6oE/home/cwd/dataset-shortlist.html`.