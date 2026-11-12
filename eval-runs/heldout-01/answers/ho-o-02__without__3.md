I answered this from memory without checking live sources, and access rules change often. Confirm each item on the data provider's page before you plan around it.

## Short answer

Nothing is both usable for AKM and downloadable today without an application. Linked employer-employee data with worker-level job histories is essentially always restricted. The realistic fast options need an application that takes weeks to a few months, not years.

## Accessible to an individual PhD student (weeks to months)

| Data | Country, years | What it takes | Main limitation |
|---|---|---|---|
| **SIAB** (IAB, FDZ) | Germany, 1975 to about 2020 | Application and data-use contract with FDZ-IAB. Academic use is cheap. Access is by remote execution or a scientific-use file, depending on the version. | It's a 2% sample of workers, so you get thin mobility per firm and a smaller connected set. **LIAB** (linked to the establishment survey) is better for firms but more restricted. |
| **MCVL** (Social Security) | Spain, 2005 to present, with histories back further | Application to the Spanish Social Security administration with a research justification. I believe it's open to foreign academics, but check. | It's a 4% sample, so the same thin-mobility issue. Earnings are based on contribution bases, which are capped. |
| **Admin3** (KRTK Databank) | Hungary, 2003 to 2017 | Request through the Databank. This is often the easiest full-population-style linked dataset for outsiders. | Hungary is a less standard setting for the inequality question, and I'm unsure about current access terms. |
| **VisitINPS Scholars / Veneto Workers History** | Italy | VisitINPS is a competitive program that is aimed partly at PhD students and involves visiting INPS. VWH is a regional dataset obtained by agreement with its custodians. | Selective, and the visit may require relocation. |

Germany is probably the best first target. It has the longest panel, a large AKM literature (Card, Heining and Kline 2013) to benchmark against, and a clear process. Mobility bias is the issue to plan around with a sample that thin.

## Needs a local institution, a coauthor, or a long process

- **Nordic countries (Denmark, Norway, Sweden, Finland):** These have excellent full-population data. Access usually requires affiliation with an authorized domestic institution or a local coauthor, plus fees and a project approval. A visiting-researcher stay or a coauthor makes this feasible.
- **Netherlands (CBS), France (DADS via CASD), Austria, Portugal (Quadros de Pessoal):** These are all possible but typically need a national partner and ethics or secrecy-committee approval. Expect months.
- **United States (Census LEHD via FSRDC):** This takes a proposal, Special Sworn Status and a background check. It can take a year or more from proposal to data, and the project must fit Census's benefit criteria. State UI wage records are sometimes more tractable through a faculty member's existing agreement. Several landmark within/between papers use restricted US data.
- **UK (ONS Secure Research Service, ASHE linked to firm identifiers):** This requires researcher accreditation and project approval, and the data is sample-based.
- **Brazil (RAIS):** I recall the worker-identified file being restricted. Check whether the public version on Base dos Dados has a usable worker ID. I suspect it doesn't.

## What you can do right now

1. **Ask your advisor and department.** Faculty or senior students often already hold access or agreements, and a coauthor with data is often the fastest route.
2. **Build the pipeline on simulated data.** Writing it while your application is pending avoids dead time. Use Python `pytwoway` (Bonhomme–Lamadon–Manresa and AKM tools), Stata `reghdfe`, or R `lfe`/`fixest`.
3. **Learn the bias corrections now.** Limited-mobility bias inflates the firm-effect variance and distorts the covariance in AKM variance decompositions. Kline–Saggio–Sølvsten leave-out estimators and BLM grouped fixed effects are standard fixes, and they matter more with sampled data like SIAB or MCVL.
4. **Replicate the method from replication packages.** Many papers post code even when the data is restricted.
5. **Use aggregate public data for context only.** US LODES, QWI and J2J are not usable for AKM because they have no individual worker histories.

## My suggestion

Apply to FDZ-IAB for SIAB and to Spain's MCVL in parallel, since both are real, relatively fast paths. At the same time, ask your advisor about a Nordic coauthor or visit if you want full-population data. Start with Germany for the first draft. If you tell me which country or institution you're based in, I can narrow this down. I can also look up current application pages if you want them verified.