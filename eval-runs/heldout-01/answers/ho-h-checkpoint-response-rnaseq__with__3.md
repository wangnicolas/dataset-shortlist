I found about five cohorts you can download today and several larger ones that need an application. I couldn't build the interactive shortlist page. The registry tool doesn't index GEO, EGA or dbGaP, so it produced none of the verification records the page needs.

Searches and cohort checks were run on 2026-11-12. GEO and PMC pages blocked my fetcher, which says nothing against the datasets. I confirmed the GEO series through NCBI's API instead. I did not check anything else on GEO, so response labels and per-patient details are marked "from memory" below.

## What I assumed you need
- **R1 (must):** patients treated with anti-PD-1, anti-PD-L1 or anti-CTLA-4.
- **R2 (must):** pre-treatment bulk tumour RNA-seq.
- **R3 (must):** a recorded RECIST or clinical-benefit label.
- **R4:** several independent cohorts, any cancer type.
- **R5:** I've separated what you can download now from what needs an application.

## Shortlist
| # | Cohort | Access | Licence | Size | Checked |
|---|---|---|---|---|---|
| 1 | Gide 2019, melanoma, anti-PD-1 ± anti-CTLA-4 (ENA PRJEB23709) | Open download | No licence stated; public ENA record | ~90 patients (memory) | Public status today |
| 2 | Riaz 2017, melanoma, nivolumab (GSE91061) | Open download | GEO, no per-dataset licence | 109 samples | Series today; labels from memory |
| 3 | Hugo 2016, melanoma, anti-PD-1 (GSE78220) | Open download | GEO, no per-dataset licence | 28 pre-treatment samples | Series today; labels from memory |
| 4 | Auslander 2018, melanoma (GSE115821) | Open download | GEO, no per-dataset licence | 37 samples | Series today; drugs from memory |
| 5 | Kim/Jung, NSCLC, anti-PD-1 (GSE135222) | Open download | GEO, no per-dataset licence | 27 samples | Series today; drug and response from memory |
| 6 | Cho, NSCLC, anti-PD-1 (GSE126044) | Open download | GEO, no per-dataset licence | 16 samples | Series today |
| 7 | Kim 2018, gastric cancer, pembrolizumab (ENA PRJEB25780) | Open download | No licence stated | 61 patients | Public status today; RNA-seq coverage unconfirmed |
| 8 | IMvigor210, bladder cancer, atezolizumab | Processed data open; raw reads need an application | Processed data reported as CC-BY; raw reads under DAC terms | 348 pre-treatment RNA samples | Raw-data record today; package route from search results |
| 9 | Braun 2020, kidney cancer, CheckMate 009/010/025 | Processed data open; raw reads need an application | Not stated | ~300 patients (memory) | Search results only |
| 10 | Liu 2019 / Van Allen 2015, melanoma (dbGaP phs000452) | Application to dbGaP | Controlled access | ~150 melanomas in the study | Study page today |

## Details

**Download today**
- **Gide (#1):** the ENA project is public, with the last update in 2020, and compares anti-PD-1 alone with anti-PD-1 plus anti-CTLA-4. You get raw reads, so you'll need to run your own alignment and quantification. The response labels are in the paper's supplement.
- **Riaz (#2):** the 109 samples include on-treatment biopsies, so keep only the pre-treatment ones. Many patients had already progressed on ipilimumab (memory).
- **Hugo (#3):** a small cohort, useful as a validation set.
- **Auslander (#4), Kim/Jung (#5), Cho (#6):** small. For #5, the GEO page I could retrieve shows a methylation paper's RNA-seq series. Check which patients have response labels before you rely on it.
- **GEO licensing:** from memory, GEO data is free to reuse, but submitters can claim copyright, so cite each paper.
- **Kim gastric (#7):** the ENA project is public, but its description centres on tissue and ctDNA sequencing. Confirm that RNA-seq is included before counting it.

**Open processed data, raw reads by application**
- **IMvigor210 (#8):** Genentech distributes the processed counts and clinical response in the `IMvigor210CoreBiologies` R package. Two sources describe its licence as CC-BY, but they conflict on the version and the package points to a LICENSE file, so read that file. I could not open the Genentech page to confirm.
- **IMvigor210 raw reads:** the raw RNA is EGAD00001003977 on the European Genome-phenome Archive (EGA). You click "Request Access", and the IMvigor210 Data Access Committee (EGAC00001000945) decides. I couldn't find a timeline, so assume weeks to months.
- **Braun (#9):** search results report a supplementary Excel file in Nature Medicine with the processed RNA-seq and clinical data. They also report EGA accessions EGAS00001004290–92 for the raw data. I did not open either.

**Application required**
- **dbGaP phs000452 (#10):** the page includes RNA-seq and directs you to "Request access via Authorized Access" with a Data Use Certification. You'll need an institutional signing official, and approval typically takes weeks. The v3 page is marked as superseded, so request the current version.

## Known, not confirmed (from memory)
- **Aggregated resources:** TIDE (998 tumours from 12 ICB studies), TIGER (18 bulk transcriptome datasets), and ICBatlas (29 datasets, 5 cancer types) have already collected and harmonised many of these cohorts. Reviews describe them as freely accessible. I could not reach their download pages, so check their terms. These are the fastest route to a multi-cohort matrix.
- **Roche trials:** IMmotion150 and IMmotion151 (kidney cancer, atezolizumab) are on EGA with a Data Access Committee. This is from memory.
- **Other trials:** CheckMate 214 (EGAS00001005501) needs an application, per search results. The Zhao glioblastoma anti-PD-1 cohort is not confirmed.

## Not recommended
- **TCGA:** none of its patients received checkpoint inhibitors.
- **Registry hits from Zenodo and OpenAIRE:** these were mostly single-cell, mouse, CyTOF, or supplements with no bulk RNA-seq and response pairing.

## What I could not find
- I could not confirm response labels, sample counts or licences for most GEO series. I also could not reach any of the three aggregator download pages.
- I did not check pre-treatment status or patient overlap between cohorts.

## Next step
1. Pull Gide, Riaz, Hugo and Auslander, plus IMvigor210 via its R package, and restrict to pre-treatment samples. That gives melanoma and bladder cohorts today.
2. Start the dbGaP request now if you need the Liu cohort.
3. Check patient overlap between Riaz, Hugo, Liu and Van Allen before treating them as independent. TIDE and TIGER flag some of this.
4. The cohorts differ in sequencing protocol and in how response is defined, so build cross-cohort validation around that.

I can now fetch the GEO sample annotations and report the response labels per cohort.