I checked the access rules for Germany, Portugal, and Brazil online this session. Everything else below comes from what I already know, so confirm details with each data provider before you plan around them.

## Short answer

You can't legally get worker-level linked employer-employee wage data with firm IDs immediately anywhere. Every dataset good enough for AKM needs an application. What you can do right away is build and test your whole pipeline on test data and simulated data, so you're ready to run it the day access comes through.

## Main options, roughly from most to least feasible for a PhD student

**1. Germany: IAB/FDZ (LIAB longitudinal model, or the full-population establishment and worker data behind Card–Heining–Kline 2013)**
- **Why it fits:** It's the standard AKM dataset. The latest longitudinal model covers 1975–2021 ([FDZ](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)).
- **What access takes:**
  - Your institution has to do independent scientific research and sit in the EU or a country with GDPR "adequacy" status. You can't apply as a freelancer.
  - LIAB is not distributed as a file. You work on-site, then usually move to remote access, or you use remote execution: you send Stata scripts and FDZ checks the output before releasing it ([FDZ access](https://fdz.iab.de/en/data-access/on-site-use/), [MIT handbook chapter](https://admindatahandbook.mit.edu/book/v1.1/iab.html)).
  - FDZ also has guest workplaces in the US, Canada, and the UK, which helps if you're based outside Europe.
  - Access is free. Approval typically takes a few months, though that's my estimate.
- **Caveat:** SIAB, the easier-to-get 2% worker sample, is too sparse within firms for credible firm effects (limited mobility bias). For AKM you want LIAB or the larger custom extracts.

**2. Portugal: Quadros de Pessoal**
- **Why it fits:** It's a near-census of private-sector employees with worker and firm IDs from the mid-1980s on, and it's used widely in AKM papers.
- **What access takes:**
  - The usual route is Banco de Portugal's BPLIM lab. Access is free. You apply with a project description, a CV, and a confidentiality agreement.
  - You write code on modified, non-valid data, and BPLIM staff run it on the real data and email you the outputs ([BPLIM access](https://bplim.bportugal.pt/content/access-0)).
  - An older BPLIM guide (2018) said QP was limited to Bank researchers and their co-authors. Ask BPLIM directly whether a solo external researcher can get it now. If not, the alternative is applying to the Labour Ministry's statistics office (GEP/MTSSS), or finding a co-author.

**3. Brazil: RAIS**
- **Why it fits:** It's a huge formal-sector census, popular for AKM and inequality work (e.g., Alvarez et al. 2018).
- **What access takes:**
  - The public RAIS downloads (and the Base dos Dados BigQuery mirror) have no worker identifiers, so you **can't follow workers or run AKM with them**.
  - The identified RAIS requires a formal application to the Labour Ministry (MTE) under Portaria 671/2021. You need an official letter from your institution and a CPF or foreign ID, and you sign a cooperation agreement ([gov.br service](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)).
  - People report it's possible but slow and unpredictable, and it has gotten harder since Brazil's data protection law (LGPD).

**4. United States: LEHD, through the Census secure research centers (FSRDCs)**
- **What access takes:**
  - You write a full proposal that has to show a benefit to Census, get Special Sworn Status (background check), and work at or through a secure research center.
  - For LEHD, the states that supply the data also have to approve the project.
  - Approval commonly takes 6–12 months or more, and you can't export anything without a disclosure review.
- **Verdict:** It works if your university has a center and your advisor or a co-author already has a project you can join. It's risky as a solo second-year route.

**5. Nordic registers (Denmark, Sweden, Norway, Finland)**
- **Why they fit:** The data are excellent: full population, long panels.
- **What access takes:** You almost always need to be affiliated with an authorized institution in that country, such as a university or central bank. In practice you get in through a local co-author or a research visit.

**6. Others**
- **France:** DADS / Panel Tous Salariés via CASD. You need committee approval, and there are fees.
- **Austria:** ASSD, accessed through Austrian university contacts.
- **Italy:** INPS through VisitINPS, which requires an on-site stay. Also the Veneto Worker History, which is older (roughly 1975–2001) but historically easier to request.
- **Canada:** CEEDD through Statistics Canada's research data centres.
- **UK:** ASHE via the ONS Secure Research Service. It's a 1% worker sample, which is thin for firm effects, and access is easiest from a UK institution.

## What you can start on right away

1. **IAB test data.** FDZ publishes Stata test datasets that have the same structure as SIAB and LIAB. You can write and debug your full sample construction (spells, connected set, AKM, variance decomposition) on them now. They're built so you can prepare remote-execution code.
2. **Simulated data.** The `pytwoway` package (Lamadon and co-authors) simulates worker–firm networks and estimates AKM, KSS leave-out bias correction, and the Bonhomme–Lamadon–Manresa (BLM) model. In Stata, `reghdfe` handles the two-way fixed effects. With these you can learn how limited mobility bias behaves and validate your decomposition code before you see real data.
3. **Replicate published decompositions** from public results tables, such as Song et al. 2019 "Firming Up Inequality" and Card–Heining–Kline 2013. Then you'll know exactly which outputs you need cleared for release.
4. **Avoid commercial career-history data** (Revelio, LinkedIn-type) for this. The wages are imputed from job titles and firms, so the decomposition you get back is partly built into the imputation.

## My recommendation

1. **Ask your advisor and department first.** Find out who already holds an approved project with IAB, BPLIM, RAIS, LEHD, or Nordic data. Joining an existing project is by far the fastest path for a second-year.
2. **Apply to IAB (LIAB) and BPLIM (QP) now, in parallel.** Both are free, both accept foreign researchers in some form, and both work through remote execution, so you don't have to relocate.
3. **Build your pipeline on the IAB test data and `pytwoway` simulations while you wait.**

Expect several months before you can work with real data. Plan your second-year paper timeline around that.

Sources:
- [FDZ LIAB LM 7521](https://fdz.iab.de/en/int_bd_pd/linked-employer-employee-data-of-the-iab-liab-liab-longitudinal-model-1975-2021-version-1/)
- [FDZ on-site and remote access](https://fdz.iab.de/en/data-access/on-site-use/)
- [MIT Admin Data Handbook, IAB chapter](https://admindatahandbook.mit.edu/book/v1.1/iab.html)
- [BPLIM access](https://bplim.bportugal.pt/content/access-0)
- [BPLIM Guide for Researchers (2018)](https://cicee.autonoma.pt/wp-content/uploads/2024/03/BPlim_Guide_for_Researchers_v2018sep26.pdf)
- [MTE RAIS/CAGED microdata](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/estatisticas-trabalho/microdados-rais-e-caged)
- [Identified RAIS application](https://www.gov.br/pt-br/servicos/solicitar-acesso-aos-dados-identificados-rais-e-caged)
- [RAIS pública overview](https://marianahaase.substack.com/p/rais-publica-que-os-micridados-permitem)