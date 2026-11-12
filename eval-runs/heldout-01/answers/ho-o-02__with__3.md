## What I assumed you need

- **R1 (must):** worker-level earnings followed over 10 or more years.
- **R2 (must):** an employer ID on each job spell, so job movers can be tracked. AKM needs a connected set of firms linked by movers.
- **R3 (must):** a long span that covers the rise in inequality.
- **R4 (nice to have):** a real wage measure (daily or annual earnings), not just contribution bases.
- I assumed you can wait weeks to months, and that you may be outside the country whose data you use. That second point matters a lot for access.

I checked on 2026-11-12. I also ran registry searches on DataCite, OpenAIRE, Zenodo and Hugging Face.

## Shortlist

| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | Germany: IAB SIAB (2% sample of social-security biographies, 1975 on) | Data Use Agreement. The scientific-use file (Regional File 7523) is downloadable by applying institutions. The less anonymised version is on-site or remote only. About weeks. | FDZ terms; you must report publications within one month | Strong | FDZ page today; establishment ID in the SUF not confirmed |
| 2 | Germany: IAB LIAB longitudinal model 1975–2024 | Application, Data Usage Agreement, on-site or remote use. About months. | FDZ terms | Strong | Today |
| 3 | Spain: MCVL (4% sample, firm contribution-account IDs) | Request forms approved by the social security directorate (DGOSS). No fee reported. About weeks. | Accessibility agreement | Strong | Search summary and portal link; forms not read |
| 4 | Italy: Veneto Workers Histories (VWH), 1975–2001 | Signed form emailed to info@frdb.org. | Must cite the source | Partial | Page read today |
| 5 | US: LEHD microdata | Federal Statistical Research Data Center proposal. About 6–12+ months. | Census Special Sworn Status | Strong | Search summary |
| 6 | Germany: SIAB Campus File (7508) | Free after registering and accepting the terms. Minutes. | Teaching use only | Weak, for practice only | Today |

## Details

**1. SIAB** ([FDZ page](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/))
- **Contents:** a 2% random sample of the IEB, German social-security employment records from 1975.
- **Why it fits:** it is the standard scientific-use dataset for AKM-type work on Germany. Sample size is thinner than LIAB or the full IEB.
- **Gaps:**
  - A guide to the 7519 version names the establishment variable `betnr`. I could not confirm that the Regional File (the downloadable version) keeps it, so check its data report before applying.
  - Wages are top-coded at the social-security ceiling, from memory.
  - The weakly anonymous and Regional File versions cannot both be used in one project.
- **If you are in the US:** FDZ says extra restrictions apply to access from the US. The page I read did not say what they are. Check the IDAN (International Data Access Network) page.

**2. LIAB** ([FDZ record](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2024-version-1/))
- **Contents:** employee histories linked to the IAB Establishment Panel survey.
- **Limits:** the page says full employment biographies are provided only for establishments with up to 49 employees. It covers establishments in the survey panel, not all firms.
- **Best use:** if you want firm covariates (collective bargaining, investment) next to the decomposition.

**3. MCVL** ([portal](https://portaldatos.seg-social.gob.es/mcvl))
- **Contents:** a 4% sample of everyone with a Social Security relationship in the reference year, with full histories.
- **Access:** you download the request form and a researcher form, and DGOSS approves. One researcher page mentions about 11 forms when tax data are included, and an older source says files were sent on DVD. Both may be outdated.
- **Gaps:** earnings are contribution bases with top and bottom coding, from memory. A usable code reference is [Puga's MCVL code](https://diegopuga.org/data/mcvl/).

**4. VWH** ([FRDB](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/))
- **Access:** fill in a form and email it to info@frdb.org. The page does not say who is eligible, the conditions or the time to access, and it does not mention a wage variable.
- **Limits:** it ends in 2001 and covers one region, so it is useful for method work but not for recent inequality trends.

**5. LEHD**
- **Access:** you need a proposal through a Federal Statistical Research Data Center (FSRDC), Special Sworn Status, and in some cases SSA and IRS approval.
- **Timing:** proposal development takes 6–12 months or more. Output must come from a sample of at least three states.
- **Public alternatives:** QWI, J2J and LODES are public but aggregated, so they cannot support AKM.

**6. SIAB Campus File** ([FDZ page](https://fdz.iab.de/en/pd_hd/campus-file-sample-of-integrated-labour-market-biographies-siab-cf-7508/))
- It is "specifically designed for the purpose of academic teaching". FDZ says only the scientific-use file supports real analysis. Use it to build your pipeline, not to produce results.

## Known, not confirmed

- **Denmark, Norway and Sweden** have the best-known worker-firm registers. A search summary says Statistics Denmark authorises research environments rather than individuals. Non-residents need a link to an approved Danish institution, and work happens on its servers. Norway and Sweden are similar, with some older sources. Check each statistics office's current rules.
- **Brazil's RAIS** (the Ministry of Labor's annual worker-firm register) has identified microdata. A 2026 PNAS paper says you apply to the Ministry. Non-identified microdata are public. I recall the public version lacks a usable worker ID, but I did not verify that.
- **Portugal (Quadros de Pessoal), France (DADS panel) and Canada (CEEDD)** are used in published AKM work. I did not check any of their access terms.

## Not recommended

- **US QWI, J2J and LODES:** public but aggregated, with no worker IDs, so they cannot support AKM.
- **The registry hits for "linked employer-employee" apart from IAB:** these were replication files and unrelated records.

## What I could not find

I found no open download that has both worker IDs and employer IDs over 10 or more years. If one exists, it is not in the registries I searched. Everything usable for real estimates needs a signed agreement or an application.

## Next step

**Today:**
- Register for the SIAB Campus File and build your AKM pipeline on it: connected set, a high-dimensional fixed effects estimator, and a bias correction for limited mobility.
- Read the Regional File data report to confirm the establishment ID.
- Email info@frdb.org for VWH.

**Parallel track:**
- If you are at a German or other institution with a FDZ-IAB agreement, start the SIAB application.
- If Spain or Italy fits your question, request the MCVL.
- Ask your advisor which datacentre arrangements your department already has. That often decides between the national datasets above.

Interactive page: `/private/tmp/e-gs6Cnn/home/cwd/dataset-shortlist.html`

Sources: [FDZ SIAB](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/), [FDZ LIAB](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2024-version-1/), [MCVL portal](https://portaldatos.seg-social.gob.es/mcvl), [FRDB VWH](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/), [LEHD data](https://lehd.ces.census.gov/data/), [FSRDC guidelines](https://www2.census.gov/adrm/FSRDC/Apply_For_Access/Research_Proposal_Guidelines.pdf), [Statistics Denmark access](https://www.dst.dk/ext/5452354440/0/israel2016/Annex-B5-15-Introduction-to-the-Danish-system-for-access-to-microdata--pdf).