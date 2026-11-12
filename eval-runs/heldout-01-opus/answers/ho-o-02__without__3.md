I answered this from what I already know and didn't check any of the providers' websites today. Access rules, fees and timelines change often, so confirm each one on the provider's site before you plan around it.

## The short answer

- **Easiest real data:** Portugal (*Quadros de Pessoal* through the Banco de Portugal's research lab) and Germany (the IAB's research data centre, the FDZ). Both regularly approve applications from academics at foreign universities. Expect roughly 2–6 months.
- **Hardest:** the US (LEHD), the Nordic registers and identified Brazilian RAIS. They're possible, but it takes a year or more, or a coauthor who already has access.
- **Nothing public works for AKM.** No freely downloadable dataset follows workers across firms with firm identifiers over 10+ years. What you can start on today is simulated data and test files that have the real structure but fake values (details at the end).

## The options, roughly from most to least accessible

### 1. Portugal: Quadros de Pessoal (QP)
- **What it is:** a mandatory annual census of essentially all private-sector employers and their employees, with worker and firm IDs. It runs from the mid-1980s to the present, with a couple of missing years (around 1990 and 2001). Card, Cardoso & Kline (2016, QJE) used it for exactly this kind of decomposition.
- **How to get it:** apply to **BPLIM** (the Banco de Portugal's Microdata Research Laboratory). You send a project proposal, sign confidentiality terms and then work on their remote server. Output is checked before you can take it out.
- **Realistic effort:** a moderate application. They're used to foreign academics, and I believe it's free for academic research (please confirm). Plan for weeks to a few months.
- **Fit:** excellent. It's the full population, so you get enough workers who switch firms to estimate firm effects well.

### 2. Germany: data from the IAB research data centre (FDZ)
- **Products:**
  - **SIAB:** a 2% sample of workers with their full employment histories.
  - **LIAB:** linked employer-employee data built around the IAB Establishment Panel.
  - **SIEED:** a sample of establishments with the complete employment histories of everyone who worked there.
  - Full administrative data (the IEB, which Card, Heining & Kline 2013 used): only by special arrangement.
- **How to get it:**
  - You need a non-commercial research institution and an approved project, then a usage contract.
  - Most linked data can only be used on-site, at FDZ locations in Germany or at partner sites abroad (several have been at US universities; check the current list), or by remote execution, where you send code and get back checked output.
  - A less detailed SIAB file can be used at your own university.
  - It's free for academics, and approval usually takes a few months.
- **Fit:**
  - SIEED and LIAB suit AKM much better than SIAB. In a 2% worker sample, most firms have too few movers, and the firm effects come out badly biased (limited-mobility bias).
  - The FDZ also offers **ready-made AKM worker and firm effects** estimated on the full administrative data (FDZ Method Report 01/2020, Bellmann et al.). You can merge these onto its other datasets, which partly gets around the sampling problem.

### 3. France: DADS / Panel Tous Salariés
- **How to get it:** through **CASD**. You first need accreditation from the *Comité du secret statistique*, and then you work remotely through a special access terminal (the SD-Box).
- **Realistic effort:**
  - There are real fees: CASD charges per project per year, and it's usually your institution that pays.
  - It's much easier from a French institution or with a French coauthor.
  - Plan for 6+ months.
- **Fit:** good, long history. The panel samples workers, so firm effects run into the same thin-sample issue as SIAB, though the full-population establishment files help.

### 4. Italy
- **INPS administrative data:** the VisitINPS Scholars programme takes competitive project applications, and you work on-site in Rome or remotely. It's a real option but selective.
- **Veneto Worker History (VWH, 1975–2001):** used by Card, Devicienti & Maida. It has historically been easier to get, on request from the University of Padova/Venice group, but I'm not sure of its current status. It ends in 2001 and covers only one region.

### 5. Austria: Austrian Social Security Database (ASSD)
Excellent data going back decades. In practice you usually get access by working with the labour economics group at JKU Linz, which is a coauthor route rather than an application.

### 6. UK: ASHE panel
- **What it is:** a 1% sample of workers, with employer identifiers and a long history (from 1975 if you include the earlier NES survey).
- **How to get it:** become an ONS Accredited Researcher (a training course plus a project application), then work through the ONS Secure Research Service or the UK Data Service SecureLab. It's easiest from a UK institution.
- **Fit:** the 1% sample makes firm effects weak.

### 7. US: LEHD
- **How to get it:** through a Federal Statistical Research Data Center. You submit a proposal through the Standard Application Process; Census reviews it, often for 6–12+ months; and you need Special Sworn Status, which includes a background check and residency requirements for non-citizens.
- **Other conditions:**
  - You must work physically at an RDC, and many charge fees unless your university is a member.
  - Every output goes through disclosure review.
  - Which states are covered depends on each state's approval.
- **Fit:** great, but it's a 1–2 year commitment. The SSA earnings data used in Song et al. (2019) is effectively unavailable.

### 8. Brazil: RAIS
- **Identified RAIS** has been the workhorse for this literature (e.g., Alvarez, Benguria, Engbom & Moser 2018). But it requires an agreement with the Ministry of Labour, and Brazil's data protection law (LGPD) has made that harder. In practice people mostly get in through existing agreements or coauthors.
- **The public RAIS microdata** are free to download, but they **don't include persistent worker identifiers**, so you can't follow movers. They're useless for AKM.

### 9. Nordic countries and Canada
- **Denmark, Sweden, Norway, Finland:** fantastic register data, but you generally need to be affiliated with an authorised institution in that country, and there are fees. It's realistic only with a local coauthor or a research visit.
- **Canada:** CEEDD through Statistics Canada's research data centres. Same story.

## What you can start this week

1. **Simulated data with known worker and firm effects.** `pytwoway` (Bonhomme, Lamadon et al.) has a simulator plus AKM, KSS-corrected and BLM estimators. For KSS there's also the authors' MATLAB code and a Julia package (`VarianceComponentsHDFE`); in Stata, `reghdfe`. Writing the full pipeline now means you can run it as soon as you get access. That matters most where you'll be working on a remote server or sending code by remote execution:
   - building the connected set (and the leave-one-out connected set)
   - estimation
   - the bias correction for limited mobility
   - the variance decomposition over time
2. **FDZ test files.** The FDZ publishes test versions of its datasets with the real structure and fake values. You can write your actual cleaning code against them.
3. **Start a proposal right away.** My recommendation is BPLIM (Portugal) as the main application, plus an FDZ application for SIEED or LIAB with the ready-made AKM effects. Both are realistic for a second-year student. Running them at the same time protects you against delays.
4. **Ask your advisor and department.** Find out whether anyone already has an LEHD, RAIS, CASD or Nordic project you could join. That's often the fastest way into the restricted datasets.

One last point that matters whichever dataset you use: with plain AKM, the share of wage variance attributed to firms is badly biased upward when firms have few movers. Use KSS or BLM corrections, and expect referees to ask for them.