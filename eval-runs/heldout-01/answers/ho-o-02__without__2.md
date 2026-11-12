**Short answer:** nothing with real worker and employer IDs is freely downloadable today. The most realistic routes for a PhD student are Portugal, Spain, Italy (VisitINPS) and the Netherlands. The US and Nordic countries are much slower. I'm working from memory and haven't checked current rules, so confirm each one with the data provider before you plan around it. The timelines are rough estimates.

## Options with realistic access for a PhD student

| Data | Coverage | What access takes | Caveats |
|---|---|---|---|
| **Portugal, Quadros de Pessoal** (Banco de Portugal BPLIM) | Full population of private-sector firms and workers, 1980s to about 2020 | Apply with a project description, an institutional affiliation and a supervisor. You can work through BPLIM's remote-access system, and I believe non-Portuguese researchers are eligible. Expect weeks to a few months. | It's a well-studied AKM setting, which helps with benchmarking and referees. Check BPLIM's current fees and rules. |
| **Spain, MCVL** (Social Security sample) | 4% sample of Social Security affiliates, from 2004 | Apply to the Social Security ministry with a project description and institutional support. I believe it's free and the files are delivered to you, but I'm not certain. | A 4% sample means few co-workers per firm and a small connected set. That makes mobility bias worse and weakens the firm-level part of the decomposition. |
| **Italy, VisitINPS Scholars** | Full INPS matched employer-employee records | A competitive call. You work on-site at INPS in Rome for a fixed period, and the program is aimed at PhD students and early-career researchers. | You have to be physically present, and it depends on the call timing. |
| **Netherlands, CBS microdata** | Full population, including job spells linked to firms | Remote access through an authorized institution, usually via a supervisor's contract. Fees apply unless your institution is covered. | Can take months to set up. |
| **Germany, IAB** | SIAB: 2% sample. LIAB: linked establishment data. | The FDZ requires a data-use contract and, for some products, remote execution. Allow a few months. | SIAB has the same sampling problem as the Spanish data. The full-population versions are much harder to get. |

## Hard to get as an outsider

- **US LEHD / Census FSRDC:** You need a proposal, a Census benefit justification and Special Sworn Status with a background check. Expect 6 to 18 months, and it's only practical if your institution hosts an FSRDC. Some state UI wage-record data exist, but each state sets its own terms.
- **Denmark, Sweden, Norway, Finland:** The data are excellent. Access usually requires a local institution or co-author, and sometimes you must be physically in the country. Finland has been more open to remote access from abroad, but verify that.
- **France (DADS via CASD) and Brazil (RAIS):** Both are possible, but they involve long approval processes, and the identified RAIS data need an agreement with the ministry. The public RAIS files, as far as I know, don't have the worker and firm IDs you need.

## What you can start on this week

1. **Build and test the estimation pipeline on simulated data.** Use `pytwoway` (Python, from Bonhomme, Lamadon and Manresa). It simulates matched data and implements the AKM fixed-effects, bias-corrected and group-based estimators. Also look at the KSS leave-one-out code from Kline, Saggio and Sølvsten, and `reghdfe` or `fixest` for high-dimensional fixed effects.
2. **Write your decomposition code now.** Whatever data you end up with, you'll need within- versus between-firm variance by year, the variance of worker effects, firm effects and their covariance by period, and the connected-set restrictions. Debugging it on synthetic data saves months.
3. **Use public aggregate data for context.** LEHD's LODES and Job-to-Job Flows are free, but they have no worker IDs, so they can't support AKM. They are useful for motivating figures and for the descriptive between-firm story.
4. **Start the applications now.** I'd begin with Portugal and, in parallel, a Spanish MCVL request or a VisitINPS application. They have different timelines, so applying to several costs little.

## Methodological notes

- With sampled data (MCVL, SIAB), the connected set is small and the leave-one-out connected set is smaller. Plug-in AKM variance estimates are biased by limited mobility, so budget for bias correction.
- Your 10-year requirement is easy to meet with the full-population datasets above. Check that the sample period includes the inequality rise you care about. Portugal's data cover a long span, and the German and Italian data cover more than that.
- A pure within- versus between-firm variance decomposition doesn't need AKM. AKM is what lets you split the between-firm part into sorting and pay premiums. Your supervisor may want both.

I can look up the current application pages and deadlines for any of these if you tell me which two or three you want to pursue.