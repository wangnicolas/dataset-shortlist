**Nothing fully suitable is a one-click download, but three datasets are reachable in weeks rather than years: Veneto Worker Histories (Italy), MCVL (Spain), and the German SIAB with pre-estimated AKM effects.** I have not checked provider pages today, so confirm current terms, fees, and coverage years before you plan around any of them.

## Quickest to get

| Data | What it is | Access | Main catch |
|---|---|---|---|
| **Veneto Worker Histories (Italy)** | Universe of private-sector workers and firms in the Veneto region, about 1975–2001, from social security records | Free on request from the economics department at Ca' Foscari University of Venice; a short signed agreement, typically days to weeks | One region, ends 2001 |
| **MCVL (Spain)** | 4% sample of everyone with a social security relationship, annual editions since 2004 with retrospective job histories and firm identifiers | Free application to the Spanish Social Security administration; typically weeks; foreign researchers have obtained it | It is a sample of workers, so you do not see whole firms |
| **SIAB (Germany, IAB)** | 2% sample of workers, 1975 onward, with establishment identifiers | Application to the IAB research data centre; the scientific use file has location restrictions, otherwise remote execution or guest stays, including at some US universities; allow a few months | 2% sample; earnings top-coded |
| **Chile unemployment insurance sample** | Public sample of monthly earnings records from 2002 | I recall it is downloadable from the pensions regulator, with anonymised employer identifiers | Verify the employer identifier is there before counting on it; I am least sure of this one |

The Veneto data is the one I would start with. It is a true universe, so both the firm-level decomposition and AKM work properly. It has been used in published AKM work (Card, Devicienti and Maida; Kline, Saggio and Sølvsten), so you can benchmark your code against known results.

For SIAB, the IAB distributes pre-estimated AKM worker and establishment effects, computed on the universe, that can be merged into its data. This sidesteps the sample problem for the fixed effects themselves.

## Full-population data, slower to get

- **Germany, LIAB or the full employment histories (IAB):** project proposal, then on-site or remote execution. A few months, no nationality barrier, and the most realistic "serious" option for a foreign PhD student.
- **France, DADS panel (via CASD):** approval by the statistical confidentiality committee, then a paid secure remote terminal. About 6 months, with fees in the low thousands of euros per year. The long worker panel is a sample; the universe files link workers only across adjacent years, though people have chained them.
- **Portugal, Quadros de Pessoal:** excellent for AKM because it has hours and occupation. Access runs through Statistics Portugal or the Bank of Portugal's microdata lab, and in practice usually needs a Portuguese affiliation or host.
- **Italy, INPS universe:** through the competitive VisitINPS programme, on site in Rome.
- **Brazil, identified RAIS:** by agreement with the Ministry of Labour, in practice through a Brazilian institution or a coauthor who already has it. The public de-identified RAIS has no worker identifiers, so it will not work.
- **US, LEHD:** a proposal through a Federal Statistical Research Data Center, plus Census and state approvals and a security clearance. Expect 1–2 years, and there are no hours, only quarterly earnings. Only worth it if your advisor already has a project.
- **Nordics and the Netherlands:** superb data, but Denmark, Sweden and Norway effectively require a local institutional affiliation or coauthor. The Netherlands (CBS) allows foreign institutions via paid remote access.
- **Others:** Hungary (administrative panel, a 50% sample, relatively welcoming), Austria (social security data through the Austrian Micro Data Center), Canada (on site in Ottawa), Mexico (through the central bank's lab) and South Africa (on site at the Treasury).

## Two things that should drive your choice

1. **Samples break the simple decomposition.** A within-firm versus between-firm split in the style of Song et al. needs every worker in the firm. With a 2–4% worker sample you cannot compute firm means reliably.
2. **Limited-mobility bias is severe in samples.** The variance of firm effects is biased upward and the sorting covariance downward when few movers connect firms. Plan on the Kline–Saggio–Sølvsten leave-out correction or Bonhomme–Lamadon–Manresa firm clustering.

## What I would do

1. Request the Veneto data this week and build your full pipeline on it: connected set, AKM, the bias correction, and the decomposition.
2. In parallel, apply to the IAB, or to CASD if you prefer France, for the paper's main data.
3. Ask your advisor and department who already has an approved project on LEHD, RAIS or Nordic data. Being added to an existing project is by far the fastest route into the restricted sources.