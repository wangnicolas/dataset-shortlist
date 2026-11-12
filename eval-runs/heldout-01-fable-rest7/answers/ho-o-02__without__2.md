**Nothing fully suitable is a same-day download, but one real dataset is close.** The Veneto Workers Histories (Italy) needs only a signed form emailed to a foundation, and it is a full-population panel you run on your own laptop. I checked the access pages for the first four options below today; the rest is from memory and flagged as such.

## Ranked by how fast you can realistically start

| Data | What it is | What access takes | Fit for AKM |
|---|---|---|---|
| **Veneto Workers Histories (VWH)** | All private-sector workers and firms in the Veneto region, 1975–2001, with worker and firm IDs | Fill in and sign a form, email it to info@frdb.org. The page states no fee, eligibility rule or turnaround time. | Good. It ends in 2001 and has missing-data issues before the mid-1980s, so 1984–2001 is the usable window. |
| **Spain MCVL** | 4% random sample of people in Social Security records, with firm and establishment IDs and full work histories | Free application to Spain's Social Security directorate (about 11 forms in an older guide); approved users work on their own computers. | Feasible but thin. A 4% worker sample means few movers per firm, so limited-mobility bias is severe. |
| **Germany IAB (SIAB, LIAB)** | SIAB is a 2% worker sample; LIAB links establishments to their workers | Free. Request form, up to a month for document checks, then an institutional use agreement. Analysis is by remote job submission or on-site visits. For a dissertation, your faculty must submit the request. | Very good. IAB also supplies pre-estimated AKM worker and establishment effects (1985–2023) to merge in. |
| **US LEHD** | Near-universe quarterly earnings records | Proposal through a Federal Statistical Research Data Center, plus background clearance and state sign-offs. Centres quote 6–12 months or more, and your advisor is expected to be co-PI. | Excellent data, but only realistic if your university has a centre and your advisor is on board. |
| **France (panel via CASD)** | Long worker panel from 1976, a sample of workers | Statistical confidentiality committee approval plus a paid secure-access box. I could not confirm current fees or rules for foreign institutions. | Good, but months and money. |
| **Brazil RAIS (identified)** | Universe of formal jobs | Requires a formal cooperation agreement between your institution and the Ministry of Labour. | Excellent data, but hard without a Brazilian co-author or institution. |

From memory, not checked today:
- **Portugal (Quadros de Pessoal), Denmark, Sweden, Norway:** these generally require affiliation with a domestic institution or a local co-author.
- **Austria and the Netherlands:** open to foreign institutions, for a fee.
- **Italy LoSaI:** a roughly 7% worker sample available from the Ministry of Labour on a project application. I could not confirm that it carries a firm identifier.

## Traps to avoid

- **Public RAIS microdata** downloads freely but is de-identified, so you cannot follow workers. It is useless for AKM.
- **The German Scientific Use File** is the downloadable version of SIAB, but the pre-estimated AKM effects appear restricted to on-site or remote-execution use.
- **PSID, NLSY and SIPP** follow workers but do not link coworkers at the same firm, so firm effects are not identified.

## What I would do

1. **This week:** send the VWH form, and start the German application through your advisor in parallel, since it has the longest paperwork chain of the realistic options.
2. **While waiting:** build the full pipeline on simulated data: connected set, AKM estimation, variance decomposition, and a limited-mobility bias correction (leave-out, as in Kline, Saggio and Sølvsten). The `pytwoway` Python package includes a simulator for this, as I recall. Kline, Saggio and Sølvsten ran their correction on VWH, so their published numbers give you a benchmark.
3. **Ask your advisor** whether anyone in the department has an existing LEHD or IAB project you could join. That is the usual shortcut around the longest queues.

One caveat on VWH: Italian inequality over 1984–2001 has been studied on this exact dataset, so it is better as a training ground and first chapter than as a novel contribution on its own.

Sources:
- [fRDB: Veneto Workers Histories](https://www.frdb.org/en/dati/dati-inps-carriere-lavorative-in-veneto/)
- [Arellano-Bover: VWH additional resources](https://www.jarellanobover.com/veneto-workers-histories-dataset-additional-resources)
- [Seguridad Social: MCVL portal](https://portaldatos.seg-social.gob.es/mcvl)
- [Diego Puga: MCVL code and access notes](https://diegopuga.org/data/mcvl/)
- [FDZ-IAB: on-site use and remote access](https://fdz.iab.de/en/data-access/on-site-use/)
- [FDZ-IAB: Scientific Use Files](https://fdz.iab.de/en/data-access/scientific-use-files/)
- [FDZ-IAB: AKM effects 1985–2023](https://doku.iab.de/fdz/reporte/2025/MR_03-25_EN.pdf)
- [Census: restricted-use application process](https://www.census.gov/topics/research/guidance/restricted-use-microdata/standard-application-process.html)
- [Census: FSRDC proposal guidelines](https://www2.census.gov/adrm/FSRDC/Apply_For_Access/Research_Proposal_Guidelines.pdf)
- [CASD: Panel tous actifs](https://www.casd.eu/source/panel-tous-actifs/)
- [MTE Brazil: requesting identified RAIS](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/estatisticas-trabalho/solicitar-bases-de-dados-identificados)