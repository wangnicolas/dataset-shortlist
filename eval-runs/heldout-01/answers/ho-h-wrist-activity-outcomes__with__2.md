## What I assumed you need

- **R1 (must):** a wrist-worn device worn for several days to a week or more.
- **R2 (must):** at least a few thousand adults.
- **R3 (must):** linked follow-up outcomes (hospital records, diagnoses or death registration).
- **R4 (must):** wrist placement, so results are comparable with other wrist-based studies.
- **Constraint:** you can wait for an application, and you are at a US university.

I checked on 12 November 2026. The registries I could search (Zenodo, DataCite, OpenAIRE, Hugging Face, PhysioNet) only returned paper supplements and code. The real cohorts came from web search and the literature. Several key sites blocked my tools (UK Biobank, China Kadoorie Biobank, the sleep-data site NSRR, MrOS Online), so some access details below are marked as unconfirmed.

## Shortlist

| # | Dataset | Access | Licence / terms | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES 2011–14 with NCHS linked mortality | Open download | Public-use; no registration mentioned | Several thousand adults (exact N not confirmed) | Strong on R1, R4. Death only, no hospital records. | Today |
| 2 | All of Us (Fitbit plus health records) | Institutional agreement plus researcher registration, about weeks | All of Us data use agreement; analysis only in their cloud workbench | About 59,000 with Fitbit data; about 22,000 with health records and 6+ months of data | Partial: a consumer tracker, not a research-grade accelerometer | Today |
| 3 | UK Biobank (Axivity AX3 wrist) | Application and fee, **applications reported paused** | Material transfer agreement; analysis on their platform | About 100,000 | Strongest scientific fit, but not available now | Partly (search results only) |
| 4 | MrOS Sleep Study (older US men) and SOF (older US women) | Request via MrOS Online / SOF Online, about weeks | Not confirmed | About 3,000 each | Partial: 3–5 days of wear, older adults, single sex | Partly |
| 5 | MESA Sleep (NSRR) | NSRR account plus data access request, about weeks | NSRR data use agreement | 2,156 | Partial: under "a few thousand", outcome availability unconfirmed | Partly |
| 6 | China Kadoorie Biobank | Registration plus application, about months | Agreement with Oxford; £2,500 per approved request outside China | About 20,000 | Partial: release to overseas researchers not confirmed | Partly |

## Details

**1. NHANES 2011–14 (start here).**
- **Device:** an ActiGraph GT3X+ on the non-dominant wrist for 7 days. Documentation is at [CDC PAXHD_G](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXHD_G.htm).
- **Outcomes:** deaths come from the [NCHS public-use linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm). The CDC page confirms a CDC FTP download and no registration.
- **Follow-up end date:** the page says the files were updated through 31 December 2022, but it doesn't give the end date for the public-use version. One paper cites follow-up through 2019, so check this.
- **Limit:** no hospital or diagnosis outcomes. Restricted files, which include more detail, need an application to the NCHS Research Data Center.
- **Steps:** download the accelerometer files and the mortality file, merge them, and apply the survey weights.
- **Used in:** [NHANES 2011–2014: Objective Physical Activity is the Strongest Predictor of All-Cause Mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/). One analysis used 3,032 adults aged 50 or older.

**2. All of Us.**
- **Data:** participants' own Fitbit data linked to health records, so you can study incident diagnoses.
- **Access:** per the [Researcher Workbench page](https://www.researchallofus.org/data-tools/workbench/), your institution must have signed a Data Use and Registration Agreement. You then register, verify your identity, complete Responsible Conduct of Research training and sign a code of conduct. Access to the workbench is free, with a $300 starting credit.
- **Comparability:** consumer-device metrics are not directly comparable with accelerometer outputs, so weigh this against your goal of matching other wrist-based studies. Users are also a self-selected group.
- **Used in:** [step counts and chronic disease](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9671804/).

**3. UK Biobank.**
- **Data:** about 100,000 people wore an Axivity AX3 on the wrist for 7 days, with linked hospital, cancer and death records ([documentation](https://biobank.ndph.ox.ac.uk/ukb/ukb/docs/PhysicalActivityMonitor.pdf)). Most of the published literature on your question uses it, for example [this PLOS Medicine study](https://doi.org/10.1371/journal.pmed.1005213).
- **Pause:** search results say UK Biobank paused new applications after an April 2026 incident involving exported data. They give a plan to reopen in late 2026 and say the next data release is expected in the first half of 2027. UK Biobank's own pages returned HTTP 403 to my tools, so I could not confirm this. Check the application page before planning around it.
- **Fees (from search results, unconfirmed):** Tier 1 is £3,000 for 3 years plus VAT, with a £500 student rate. Platform compute costs extra. The historical average was about 15 weeks from application to data.

**4. MrOS Sleep and SOF.**
- **Device:** a SleepWatch-O on the non-dominant wrist for 3–5 days. MrOS has about 3,000 men and SOF about 3,000 women.
- **Outcomes:** mortality is well studied, for example [rest/activity rhythms and mortality](https://pubmed.ncbi.nlm.nih.gov/20370475).
- **Access:** the NSRR copy of MrOS has no actigraphy. Papers point to MrOS Online (mrosonline.ucsf.edu) and SOF Online (sofonline.ucsf.edu), which I could not read. The request process is unconfirmed.

**5. MESA Sleep.**
- **Device:** an Actiwatch Spectrum on the wrist for 7 days, per the [documentation](https://sleepdata.org/datasets/mesa/files/m/browser/documentation/MESA_Sleep_Data_Documentation_Guide.pdf).
- **Outcomes:** I could not confirm whether NSRR hosts the event and mortality data. They may need a proposal to the MESA Coordinating Center.
- **Used in:** [sleep and cardiovascular disease in MESA](https://www.ahajournals.org/doi/10.1161/JAHA.122.025252).

**6. China Kadoorie Biobank.**
- **Data:** the [published description](https://ijbnpa.biomedcentral.com/articles/10.1186/s12966-023-01537-8) covers 20,370 participants with 7-day wrist data.
- **Access (from search results):** register on their data access system and apply. Students apply with a supervisor. Outside China the fee is £2,500 per approved request.
- **Release:** the data may go first to collaborators in China and the UK. Follow-up for this resurvey is also short.

## Known, not confirmed

- **Whitehall II** (GENEActiv wrist, 9 days, 2012/13) and the **Rotterdam Study** (GENEActiv wrist, 7 days) both exist. Access is by request to the study teams, who are listed in the papers. I did not confirm their sample sizes or outcome linkage.
- **UK Biobank's pause** is from search results only.

## Not recommended, and why

- **Zenodo and Figshare hits** such as the NHANES sleep–mortality supplements are code and tables from papers, not cohort data.
- **Hip-worn cohorts** (NHANES 2003–06, WHI OPACH, Women's Health Study) fail the wrist requirement. This is from memory.

## What I could not find

- Confirmed access pages for UK Biobank, CKB, NSRR and MrOS Online.
- Whether MESA event and mortality data sit on NSRR.
- A confirmed end date for the public-use NHANES mortality follow-up.

## Next step

Start on NHANES today, since it needs no application. In parallel:
1. Ask your institution whether it already has an All of Us agreement.
2. Check the UK Biobank application page for reopening.
3. Email the MrOS and MESA teams to confirm outcome data.

Your institution may also want to confirm that the work counts as exempt from ethics review.

The interactive shortlist is at `/private/tmp/e-M9qMzZ/home/cwd/dataset-shortlist.html`.