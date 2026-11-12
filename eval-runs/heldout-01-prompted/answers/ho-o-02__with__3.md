Short version: I found one dataset you can request today (Veneto, Italy), but it only covers part of Italy and stops in 2001. The other options are restricted, and the pages I checked didn't give me eligibility rules, fees or timelines.

## Start now

**Veneto Workers Histories (VWH), Italy**
- **What it is:** INPS social-security records, 1975–2001, with linked person, firm and contract files. This is the structure AKM needs, and the FRDB notes that it's commonly used for that.
- **Coverage caveat:** The FRDB page says the data cover all private-sector firms in the provinces of Treviso and Vicenza and every worker those firms employed. Other sources describe it more broadly as workers who ever worked in Veneto. Read the [data description PDF](https://www.frdb.org/wp-content/uploads/2015/03/Description_database_VWH.pdf) before you rely on it. Agriculture and public administration are excluded.
- **Access:** You fill in and sign a form on the [FRDB page](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/) and email it to info@frdb.org. You must cite Università Ca' Foscari Venezia and Giuseppe Tattara as the source. I didn't find eligibility conditions or a turnaround time, so ask them. [Arellano-Bover's page](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources) has extra notes for users.
- **Fit for your question:** It spans 27 years, so it fits a ten-year panel. But it's one region, and it ends in 2001, so it can't speak to recent inequality trends. It's best for learning the method and building a pipeline, or for a first-year paper.

**Teaching and test files**
- The IAB Campus File (SIAB CF 7508) is free after registering, but it's for teaching only. It's a 20% sample of one cohort of unemployment-benefit entrants, and it has no establishment ID, so it can't support AKM.
- The IAB also posts [random test data](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/) for the LIAB. It's meant for writing and debugging code and isn't suitable for analysis.

**Public tabulations**
- The Census [Job-to-Job Flows](https://lehd.ces.census.gov/data/j2j_subsector_research.html) tables are public but aggregate. They are useful for context, not for AKM.

## Restricted options, ranked by realism

1. **Germany: IAB LIAB** (linked employer-employee data, longitudinal model 1975–2024 is the newest version I saw).
   - **Access:** On-site use at the research data centre in Nuremberg, which includes remote access after you've used it on-site. The [FDZ page](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/) notes that person and establishment AKM effects are available on request.
   - **Gaps:** There is no scientific use file for LIAB, and the establishment sample comes from a stratified survey panel. The page didn't state the fees, eligibility or application steps. Start with [fdz.iab.de/en/data-access](https://fdz.iab.de/en/data-access) and iab.fdz@iab.de.
   - **Also:** The full SIAB (a 2% sample of individual employment histories) has the establishment ID, but only the on-site version. The public SIAB-Regionalfile doesn't have it. The guides I found describe on-site use in Nuremberg or at partner sites in Germany, France, Luxembourg, Poland and Spain, plus an application and a contract.

2. **US: LEHD through a Federal Statistical Research Data Center (FSRDC).**
   - **Access:** You need an approved project, and some files need extra IRS approval because they contain federal tax information. Only a subset of states is available, and the data generally run from 2000. See the [Census page](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html). Expect a long approval process.
   - **Gap:** LEHD records quarterly earnings, so you don't observe wages directly.

3. **Brazil: identified RAIS.**
   - **Access:** It's not public. You request it from the Ministry of Labour through the gov.br service "Solicitar acesso aos dados identificados RAIS e CAGED", and sign a confidentiality agreement. I couldn't confirm the exact requirements or timing. See the [PDET microdata page](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/estatisticas-trabalho/microdados-rais-e-caged-e-caged) and the [service link](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged). This is plausibly the most accessible option for a foreign researcher, but I haven't verified that.
   - **Gap:** I didn't check whether the public, non-identified RAIS files can link workers across years, so don't assume they can.

4. **Denmark: IDA.**
   - **Access:** The sources I found are old (about 2010–2011). They say access goes to permanent research environments, and foreign researchers generally need a tie to a Danish institution. Remote access exists. See [this IDA description](https://wp.druid.dk/wp/20100016.pdf). Check Statistics Denmark's current rules, since this may have changed.

5. **Portugal (Quadros de Pessoal), Norway, Sweden.** Papers use these data, but my searches found nothing on access. I'm not recommending them, and I couldn't verify that any fixed-effects estimates are publicly posted for these or any other country.

## Suggested path

1. Email FRDB for VWH now, and build your AKM pipeline on it. Look at the connected-set restriction and limited-mobility bias, which matter a lot in AKM work.
2. In parallel, ask your advisor about a data-access route. Having a co-author or a host at the data custodian's institution is often what unlocks LIAB, FSRDC or Danish access.
3. Contact the IAB FDZ and the Brazilian PDET with a short project description.

I can draft the VWH request or the IAB inquiry if you'd like. I can also search for Norway, Sweden or Portugal in more detail.

Sources:
- [IAB FDZ: LIAB longitudinal model](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)
- [IAB FDZ: SIAB Campus File](https://fdz.iab.de/en/pd_hd/campus-file-sample-of-integrated-labour-market-biographies-siab-cf-7508/)
- [FRDB: Veneto Workers Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- [Census LEHD restricted-use data](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/lehd-data.html)
- [LEHD J2J data](https://lehd.ces.census.gov/data/j2j_subsector_research.html)
- [Brazil MTE RAIS/CAGED microdata](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/estatisticas-trabalho/microdados-rais-e-caged)
- [DRUID: Danish IDA](https://wp.druid.dk/wp/20100016.pdf)