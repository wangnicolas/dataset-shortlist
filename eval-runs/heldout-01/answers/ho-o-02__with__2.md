There's no open-download worker-firm panel I could find, so nothing you can use for AKM today. All the real options need an application. The fastest ones to get are probably Spain's MCVL and a German SIAB download, and the best long-term fit is German IAB data, if you can get there.

I checked this on 2026-11-12. Registry searches (DataCite, OpenAIRE, Zenodo, Hugging Face) mostly returned noise. The access facts come from web pages I read, and I mark below what I couldn't confirm.

## Options, in the order I'd pursue them

| # | Dataset | Access | Time to access | Fit |
|---|---|---|---|---|
| 1 | **Spain – MCVL** (4% sample of Social Security records, with tax earnings) | Paper application to the national Social Security administration, free, no on-site visit | Weeks (my estimate) | Strong, but a small-ish sample |
| 2 | **Germany – SIAB** (2% worker sample, from 1975) | Your institution signs a data use agreement. The downloadable file is the "Regional File". | Weeks to months (my estimate) | Uncertain: I couldn't confirm it carries an establishment ID |
| 3 | **Germany – LIAB / full IAB data** (workers linked to establishments, 1975–2024) | Project proposal, then on-site or remote access only | Months | Strongest for your question |
| 4 | **Italy – INPS** via VisitINPS | 3-month funded visit to Rome | Months | Strong, but the call is competitive |
| 5 | **UK – ASHE** (panel back to 1997, with employer identifiers) | Accredited-researcher route | Months | Good, but survey-based and about 1% of workers |
| 6 | **US – LEHD** | Proposal to a Census Research Data Center | 4–7+ months, longer for non-citizens | Strong, but slowest |
| 7 | **Brazil – RAIS (identified)** | Application to the labor ministry plus an institutional agreement | Unknown | Strong |
| 8 | **Italy – Veneto Worker Histories (VWH)** | Sign a form and email it to the foundation that hosts it | Weeks | Limited: two provinces, 1975–2001 |

**Spain – MCVL.** It has firm identifiers and tax-based earnings that aren't top-coded. Social Security earnings are top- and bottom-coded for about 13% of observations. The process is a stack of Spanish-language forms signed by your institution and sent to the Social Security administration. One replication site (Diego Puga's, [diegopuga.org/data/mcvl](https://diegopuga.org/data/mcvl/)) counted 11 forms, and mentions no fee. I confirmed the process from [the official portal summary](https://portaldatos.seg-social.gob.es/mcvl) and that site, but not the form count today. Puga's page also has code you could reuse.

**Germany – SIAB.** [The FDZ page](https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/) confirms that the "factually anonymous" version can be downloaded by applying institutions. The more detailed version is only available during research visits or remote access. You can't use both in one project. A 2023 guide to preparing the SIAB mentions an establishment ID (`betnr`) that is sometimes missing. Check FDZ-Datenreport 07/2023 before you commit.

**Germany – LIAB.** Access is by research visit or remote access only. The 1975–2024 longitudinal model ([DOI](https://doi.org/10.5164/iab.liablm7524.de.en.v1)) provides full employment biographies only for establishments with up to 49 employees. The cross-sectional model may suit you better. Your institution signs a data use agreement, and you must report publications to the FDZ. Foreign researchers are supported (the FDZ has an international access network), but I couldn't confirm PhD-student eligibility.

**Italy – INPS.** [The list of available data](https://www.inps.it/content/dam/inps-site/pdf/datiebilanci/visitinps-scholars/documents/Banche_dati_disponibili-EN.pdf) includes private-sector employer-employee data, annual 1974–2024. Under the Type B call, advanced PhD students (all exams done, thesis pending) can apply. I didn't confirm the current deadline.

**UK – ASHE.** The [UK Data Service secure-access study (SN 6689)](https://datacatalogue.ukdataservice.ac.uk/studies/study/6689) covers 1997–2025. The ONS Secure Research Service also holds ASHE linked to PAYE tax data. I couldn't verify the catalogue page automatically, and I haven't confirmed the employer-ID variable name or whether your institution qualifies.

**US – LEHD.** [The Census page](https://lehd.ces.census.gov/data/) confirms that the microdata are restricted to approved projects at Census Research Data Centers. The timeline comes from older RDC slides. Employer-level tax identifiers need extra IRS approval.

**Brazil – RAIS.** The identified version isn't public. Researchers email the labor ministry (`observatoriotrabalho@mte.gov.br`, per the Engbom–Moser replication README). The application needs a project description, a justification for needing person and employer IDs, and an institution that can sign legal agreements.

**Italy – VWH.** [The FRDB page](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/) says to sign the attached form and email it to info@frdb.org. The data end in 2001, and I couldn't confirm a wage variable. It's useful for learning, not for recent inequality trends.

## Known, not confirmed
- **Denmark, Norway and Sweden** have excellent registers. Foreign researchers generally need an affiliation with an approved institution in that country, so a foreign PhD student normally can't apply directly. This is from web summaries, some old.
- **Austria, France (DADS via CASD), Portugal (Quadros de Pessoal), Netherlands (CBS) and Canada (CEEDD)** are from memory only. Each is restricted, and I didn't check them.
- **WHIP (Italy)** is a 1-in-15 sample, 1985–2019, linked to firm data. I couldn't find how to apply.

## Not recommended
- **Arizona UI claimant records** (open, Zenodo) contain unemployment claimants, not an employer-employee wage panel.
- **LODES and QWI** (US Census) are open but aggregated. You can't estimate worker fixed effects from them.
- **Linked Personnel Panel (Germany)** is open to researchers but survey-based and not a wage panel.

## What you can do right now
- Read [*The ABC of AKM*](https://arxiv.org/pdf/2603.17034), a recent user's guide that came up in my search.
- Practise the estimator on simulated data. I believe the `pytwoway` Python package can do this, but I haven't checked it.
- Lock down your cheapest route first (MCVL or SIAB), then ask your advisor which of these your department already has agreements for.

## Next step
A short email to your advisor (do they have contacts at IAB, INPS or Spain's Social Security?) will probably decide this faster than anything else. If you tell me your institution's country and whether you'd travel for a visit, I can narrow this to two options.

The interactive companion page covers only the four sources I formally verified (LIAB, SIAB, VWH, LEHD), not the rest above: `/private/tmp/e-Y0nqy3/home/cwd/dataset-shortlist.html`