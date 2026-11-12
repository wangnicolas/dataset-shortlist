**Short answer:** the only data you can realistically be working with within days to weeks is the Veneto Worker History (VWH) file from Italy. The best data you can get on a PhD timeline is the German IAB data, which takes a few months. I checked the VWH and IAB access pages today; everything else below is from memory and should be confirmed with the provider.

## Start right away

**Veneto Worker History (Italy, 1975–2001)**
- **What it is:** matched worker-firm panel built from social security records, with every worker followed across their whole career. It is the dataset used in Card, Devicienti and Maida (2014) and in Kline, Saggio and Sølvsten (2020), so replication code exists.
- **Access:** sign a one-page form and email it to the Fondazione Rodolfo Debenedetti (info@frdb.org). The page lists no fee and no eligibility conditions.
- **Limits:** one region, the series ends in 2001, and earnings are annual with no hours. The distributor's page describes coverage as Treviso and Vicenza provinces, while papers using it describe all of Veneto, so ask which version you are getting.

**IAB test data (Germany)**
- The IAB's research data centre lets you write and debug code against artificial test data before you have real access.
- This is only for building the pipeline; the numbers are meaningless.

## Feasible in months

| Data | What it takes | Catch |
|---|---|---|
| **Germany: SIAB / LIAB** (1975 onward) | Your supervisor's chair must submit the request, as a Word form. Review takes up to a month, then your institution signs a use agreement. You then submit code for remote execution or work on-site. I recall no fee. | Earnings are top-coded and need imputation. From outside the EU, use remote execution: on-site use in the US, Canada or UK needs a stay of nine months or more and extra anonymisation. |
| **Spain: MCVL** (4% sample, 2004 onward plus retrospective histories) | Institutional request form to Social Security. Free, and I recall turnaround in weeks. | The sample is small for AKM. I could not confirm whether institutions outside Spain qualify. |
| **Italy: LoSaI** (roughly 6.5% sample, 1985 onward) | Project-based request to the Ministry of Labour. | I could not confirm the current procedure or the firm identifier; check before counting on it. |
| **France: DADS panel / Base Tous Salariés** | Approval by the statistical secrecy committee, then a paid secure-access box through CASD. Expect several months and a few thousand euros a year. | The long panel is a sample of roughly 1 in 12; the full file does not link workers across years directly. |

## A year or more, or needs an insider

- **US LEHD:** proposal through a Federal Statistical Research Data Center, with Census and state approvals and Special Sworn Status. Expect a year or more, and non-citizens face a residency requirement. This is realistic only if your university has a centre and a faculty member already has a project.
- **US Social Security data (Song et al.):** effectively closed to outsiders.
- **Brazil RAIS (identified):** requires a cooperation agreement between an institution and the Ministry of Labour, in practice through a Brazilian partner or a faculty member who already holds it. The public RAIS files have no worker identifiers, so they cannot be used for AKM.
- **Portugal (Quadros de Pessoal), Denmark, Sweden, Norway, Netherlands:** excellent data, but access runs through an accredited local institution, often with fees. The usual route is a coauthor or a research visit.

## Two method points that affect the choice

- The basic within/between-firm variance decomposition needs only firm identifiers and wages, not worker mobility. You can produce it on VWH on day one.
- AKM variance components are biased when few workers move between firms, which is worst in small samples like MCVL or LoSaI. Plan on a leave-out correction (Kline, Saggio and Sølvsten) or firm clustering (Bonhomme, Lamadon and Manresa).

## What I would do

Request VWH this week and ask your advisor to submit the IAB request in parallel. Build and validate the whole pipeline on VWH, then port it to the German data.

Which country is your institution in? That decides whether the US data centre route or the European sample files are worth pursuing as well.

Sources:
- [fRDB: Veneto Workers Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- [Arellano-Bover: VWH additional resources](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources)
- [FDZ IAB: on-site use and remote data access](https://fdz.iab.de/en/data-access/on-site-use/)
- [FDZ IAB: scientific use files](https://fdz.iab.de/en/data-access/scientific-use-files/)
- [FDZ IAB: data products](https://fdz.iab.de/en/our-data-products/overview-of-available-data/central-fdz-data-products/)
- [Seguridad Social: MCVL portal](https://portaldatos.seg-social.gob.es/mcvl)
- [gov.br: identified RAIS/CAGED request](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)
- [INPS: VisitINPS database annex](https://www.inps.it/content/dam/inps-site/pdf/gare/avvisi/visitinps-scholars/4848KEY-all-a_banche_dati_visitinps_scholars_iselezione.pdf)