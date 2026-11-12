I haven't checked any of the access terms below against current websites. Application rules and fees change, so confirm each one with the data provider before you plan around it.

## Access options, from most to least realistic for a PhD student

| Source | Coverage | What access takes | Realistic timeline |
|---|---|---|---|
| **Portugal: Quadros de Pessoal** (via Banco de Portugal's BPLIM) | Annual census of private-sector employers and employees, with worker, firm and wage data. Hours are included, and it has been used for well-known AKM papers. | Project proposal and institutional affiliation. Work runs in a remote environment. As I remember it, BPLIM is open to external and foreign academics, but check this. | Weeks to a few months |
| **Germany: IAB (SIAB, LIAB, full IEB)** | Social security records going back decades. | The SIAB scientific-use file (a 2% sample of individuals) needs a data-use contract signed by your institution. LIAB and the full data need remote execution (JoSuA) or an on-site visit in Nuremberg. | SIAB: weeks to months. Full data: months |
| **France: DADS (via CASD)** | Matched employer-employee panel. | The statistical-secrecy committee approves your project. Access is through a secure physical terminal or remote box, and there are fees. Foreign researchers are eligible. | 3–6+ months |
| **Italy: INPS (VisitINPS Scholars)** | Social security worker-firm data. | Competitive program aimed at PhD students and early-career researchers. The program has historically involved a stay at INPS. | One application cycle, then the program length |
| **US: Census LEHD** (through an FSRDC) | Quarterly earnings, linked workers and employers. | Proposal approval, Special Sworn Status and a background check. Residency and citizenship rules can be a barrier for non-US persons. Earnings are quarterly, with no hours. | 6–12+ months |
| **US: state UI wage records** | Same structure as LEHD, for one state. | In practice this means a coauthor with an existing agreement with the state agency. | Depends entirely on the relationship |
| **Denmark, Sweden, Norway, Finland** | Excellent, near-complete registers, which are the gold standard. | Access is generally through a national institution. This usually means a Danish, Swedish or Norwegian affiliation or a local coauthor, and it is much harder as a foreign student. | Months, with the affiliation as the real barrier |
| **Brazil: RAIS identified, Hungary: Admin3** | Both have been used for AKM work. | Both are access-by-agreement. For Brazil, I'm unsure what is public and what isn't. | Unclear |

Two data caveats matter for your question:
- **Germany:** wages are top-coded at the social security ceiling. This directly affects inequality measures, so you would need an imputation step, as Card, Heining and Kline did. The SIAB is a worker sample, so it covers few workers per firm. Firm effects will be noisy and the connected set thin. The full data or LIAB are better for AKM.
- **US:** LEHD has no hours, so you can't separate wage rates from hours.

## What you can start on now

I don't know of any open dataset with real linked worker-firm histories. Here is what you can do in the meantime:

1. **Build and test your pipeline on simulated data.** You can write and debug the whole estimation and decomposition code now:
   - Estimate with `reghdfe` (Stata), `pyfixest` or `lfe`.
   - Use `pytwoway` (Python), which includes a data simulator and bias-correction tools.
   - Correct for limited-mobility bias with Kline-Saggio-Sølvsten leave-one-out code.
   - Restrict to the largest connected set.
   - Decompose the change in wage variance into worker, firm and sorting terms, plus the within/between split.
2. **Read the replication packages.** These include Card-Heining-Kline (Germany), Song et al. "Firming Up Inequality" (US), and the Brazil and Portugal papers. They show the exact sample restrictions and decomposition formulas.
3. **Use public aggregates for preliminary descriptives.** US QWI and LODES can't support AKM. They can give you rough between-industry or between-firm-size patterns while you wait.
4. **Look at the Veneto Workers History (Italy).** I believe it has been shared with researchers on request, with much lighter access requirements. I'm not sure it's currently available, so email the maintainers.

## What I'd do

1. Ask your advisor whether the department already has a data agreement, or whether any coauthor does. This is often faster than any application.
2. Apply to **BPLIM (Portugal)** and the **IAB SIAB** in parallel. They are the most accessible for a foreign student, and both have long panels. Add the **VisitINPS** program if the cycle fits.
3. Build your pipeline on simulated data while you wait.

If you'd like, I can write the simulated-data pipeline (AKM estimation, connected set, KSS correction, variance decomposition) in Python or Stata. I can also pull current application pages for BPLIM and IAB, if web access works in this session.