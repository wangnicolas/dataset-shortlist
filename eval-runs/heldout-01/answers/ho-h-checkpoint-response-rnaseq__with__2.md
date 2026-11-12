Several well-used cohorts are open downloads, and the largest trial cohorts need a controlled-access application. Access terms below are as of 2026-11-12. I checked most of them through web search and the COMPASS portal. I could not open GEO, PMC or the ENA browser from here, because they returned bot challenges, so I never saw those records directly.

## What I assumed you need
- **R1 (must):** patients treated with anti-PD-1, PD-L1 or CTLA-4, with a pre-treatment bulk tumour RNA-seq sample.
- **R2 (must):** a response label (RECIST responder vs non-responder, or clinical benefit).
- **R3 (must):** several independent cohorts, so you can train on some and validate on others.
- **R4 (nice):** a download you can start today. Any cancer type is fine.

## Shortlist
Sizes are responders/non-responders (R/NR) as listed on COMPASS, a portal that curates these cohorts. The "Checked" column says how I know the access condition.

| # | Cohort | Cancer / drug | n (R/NR) | Access | Checked |
|---|---|---|---|---|---|
| 1 | Hugo 2016, GSE78220 | Melanoma, anti-PD-1 | 26 (14/12) | **Open** (GEO) | COMPASS and a paper's data statement; GEO page not opened |
| 2 | Riaz 2017, GSE91061 / PRJNA356761 | Melanoma, nivolumab | 51 (10/41) | **Open** (GEO/SRA) | Same as above |
| 3 | Gide 2019, PRJEB23709 | Melanoma, anti-PD-1 ± CTLA-4 | 73 (40/33) | **Open** (ENA) | Same as above |
| 4 | Kim 2018, PRJEB25780 | Gastric, pembrolizumab | 45 (12/33) | **Open** (ENA) | Same as above |
| 5 | Rose 2021, GSE176307 | Bladder, ICI | 89 (16/73) | **Open** (GEO) | COMPASS only |
| 6 | Zhao 2019, PRJNA482620 | Glioblastoma, anti-PD-1 | 25 (11/14) | **Open** (SRA) | COMPASS only |
| 7 | Snyder 2017 | Bladder, atezolizumab | 21 (7/14) | **Open** (Zenodo 10.5281/zenodo.546110) | Conflict, see below |
| 8 | IMvigor210 | Bladder, atezolizumab | 298 (68/230) | **Open processed data**, controlled raw data | Confirmed by search |
| 9 | Liu 2019 and Van Allen 2015, dbGaP phs000452 | Melanoma, anti-PD-1 and anti-CTLA-4 | ~107 and ~39 | **Controlled** (dbGaP) | Confirmed by search |
| 10 | Braun 2020 (CheckMate 025), Miao 2018 (CheckMate 009) | Kidney, nivolumab | ~17 for Miao; Braun larger | **Controlled** (EGA / dbGaP phs001493) | Accessions confirmed; Braun access terms not confirmed |
| 11 | Ravi 2023 (SU2C-MARK), dbGaP phs002822 | NSCLC, ICI | 102 LUAD and 25 LUSC | **Controlled** (dbGaP) | COMPASS only |
| 12 | IMmotion150, EGAS00001002928 | Kidney, atezolizumab ± bevacizumab | 165 (48/117) | **Controlled** (EGA) | COMPASS only |

## Details
**Open and ready now (rows 1–7).**
- These are raw reads or counts in GEO, SRA, ENA or Zenodo, with response labels in the paper supplements.
- **Riaz and Gide** include on-treatment biopsies as well as baseline ones. Filter to pre-treatment samples, or your "pre-treatment" classifier will leak.
- **Gide** mixes monotherapy and combination arms.
- **Hugo** is small, and I did not check how many of its samples are pre-treatment.
- **COMPASS** (immuno-compass.com/download) lists 23 cohorts with clinical TSVs. For the open cohorts, its mRNA links point to a `data_request.md` file. I could not tell whether that means a request step, so treat COMPASS expression data as unconfirmed.
- **Snyder conflict:** COMPASS attributes Zenodo 546110 to Snyder. A separate paper's data statement attributes that DOI to the IMvigor210 RNA-seq. Check the Zenodo record before you rely on it.

**IMvigor210 (row 8).**
- **Raw data:** controlled access at EGA, study EGAS00001002556. You request access through the EGA study page.
- **Processed data:** Genentech distributes the `IMvigor210CoreBiologies` R package, with counts and clinical data for 348 patients. Response is available for 298 of them. The package is at `research-pub.gene.com/IMvigor210CoreBiologies/`, and it is how most papers use this cohort. I have not confirmed its licence.
- **Other atezolizumab data:** IMvigor211 and OAK appear on EGA (EGAD00001007703, EGAD00001008391, EGAS50000000497), also controlled. I did not check what response data they carry.

**Controlled cohorts (rows 9–12).**
- **dbGaP:** you need an eNRA account, a data access request, and institutional signing-official approval. Expect weeks to months.
- **EGA:** you submit a request to the study's Data Access Committee, and it needs a signed agreement. Expect weeks to months, from memory.
- **Braun 2020:** a later paper reports that CheckMate 025 normalised RNA-seq is at EGAS00001004290, EGAS00001004291 and EGAS00001004292. I did not confirm who approves access.
- **Fallback for processed data:** check each paper's supplement for processed tables. Several of these studies publish normalised expression there. I haven't confirmed this for any of the controlled cohorts.

## Known, not confirmed
- **Compilation portals:** TIDE (tide.dfci.harvard.edu), CRI iAtlas, ICBatlas, Cancer-Immu and ICBcomb all curate ICI cohorts. The web search described them, but I did not open them or check their terms. They are worth trying because they can save you the harmonisation work. Whatever they redistribute cannot be more open than the original source.
- **Other cohorts:** COMPASS lists Freeman (MGH, melanoma, dbGaP phs002683) and Choueiri (kidney, via CRI iAtlas, n=16). I have not verified either.
- **Cohorts I know of but did not search for:** Auslander 2018 (melanoma, possibly GSE115821), and a few NSCLC cohorts. Their accessions are from memory, so confirm them before use.

## Not recommended, and why
- **TCGA** has no checkpoint-treatment or response labels.
- **Microarray or NanoString cohorts**, such as Prat 2017 and Cristescu 2018, are not bulk RNA-seq. They would complicate cross-platform validation.
- **Scripta/single-cell ICI datasets** (the Curated Cancer Cell Atlas, for example) are single-cell, not bulk.

## What I could not find
- I did not check each cohort's response definition (RECIST vs clinical benefit). It differs between papers, so harmonise it before pooling.
- The registry search in the skill's tool (Zenodo, DataCite, OpenAIRE) returned mostly noise, because these cohorts live in GEO, ENA, EGA and dbGaP, which that tool doesn't cover. This list is therefore built from the literature and web search, and it may be incomplete.
- I did not build the interactive shortlist page, because I ran out of reliable registry data to put in it.

## Next step
1. **Today:** download rows 1–6 (melanoma ×3, gastric, bladder, GBM) and filter to baseline samples. That gives you about 300 patients across three cancers.
2. **Start the dbGaP and EGA requests now** (rows 8–12), since they run in the background for weeks. IMvigor210 is the highest value, because the processed R package gives you ~300 patients with no wait.
3. **Pick a validation strategy:** train on melanoma and validate on bladder and gastric. Also consider leaving one cohort out at a time, since cohorts differ by cancer type and by whether the antibody targets PD-1, PD-L1 or CTLA-4.