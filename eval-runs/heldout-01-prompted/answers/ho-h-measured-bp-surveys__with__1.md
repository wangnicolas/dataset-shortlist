I'd use NHANES as the main US dataset, with HRS as a US older-adult option. ELSA, LASI and CHARLS are the comparable non-US surveys. Each has measured BP and a doctor-diagnosis question, and each is free and open to registered researchers. I found all of them through web searches. I haven't opened every data portal, so the details marked "check" below are things to confirm.

## US

**1. NHANES (CDC/NCHS), the main choice**
- **Design:** It is nationally representative of the civilian non-institutionalised population, with an examination component.
- **Measured BP:** Examiners take the readings in the mobile exam centre. This is the BPX file (or BPXO in recent cycles, which switched to an oscillometric device). Check the device and protocol for each cycle you use.
- **Diagnosis question:** BPQ020 asks, "Have you ever been told by a doctor or other health professional that you had hypertension, also called high blood pressure?" BPQ040A covers current medication.
- **Access:** There is no application. Download the .xpt files and documentation for each cycle from the [CDC data pages](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/), for example [BPQ_L for 2021–2023](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm). [NBER mirrors the codebooks](https://data.nber.org/nhanes/2013-2014/BPQ_H.htm).
- **Analysis notes:** You must use the design variables and weights. Merging the interview questionnaire with exam data calls for the exam (MEC) weights. The survey includes adults aged 16 and over, so restrict to your age range.

**2. Health and Retirement Study (HRS, University of Michigan), for ages 50+**
- **Design:** It is a panel of Americans aged 50 and over.
- **Measured BP:** Respondents in the enhanced face-to-face interview, which alternates halves of the sample every two waves, consent to physical measures that include BP. These sit in the public-use files, as far as I could tell from the search results. Check this against the codebook.
- **Diagnosis question:** The core interview asks whether a doctor has ever told the respondent they have high blood pressure. I'm confident of this from background knowledge but did not confirm the variable name in this search.
- **Access:** Register for free on the [HRS Data Portal](https://hrsdata.isr.umich.edu/). Public files download right after registration. The dried-blood-spot and venous-blood biomarkers are [Sensitive Health Data](https://hrsdata.isr.umich.edu/data-products/sensitive-health). You'd only need those if you wanted lab values, and they require a separate order form and use agreement. Start with the [New User Guide](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf).

## Non-US

**3. English Longitudinal Study of Ageing (ELSA), England, ages 50+**
- **Measured BP:** Nurse visits have BP at Waves 2, 4, 6, 8 and later, and Wave 0 comes from the Health Survey for England. The [nurse visit user guide](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/5050_waves_2-4-6-8_nurse_data_user_guide_v01_0.pdf) has a blood pressure section.
- **Diagnosis question:** The main interview has a doctor-diagnosed hypertension item. Check the exact variable names in the wave documentation.
- **Access:** Data are held at the UK Data Service as [SN 5050](https://datacatalogue.ukdataservice.ac.uk/studies/study/5050). Register with UKDS, which is free through institutional login for UK academics and for many others. Then accept the End User Licence. Some files need a Special Licence.
- **Contacts:** elsadata@natcen.ac.uk for data questions.

**4. Longitudinal Ageing Study in India (LASI) Wave 1 (2017–18), ages 45+**
- **Measured BP:** Three readings were taken, and the mean of the last two is provided.
- **Diagnosis question:** The survey asks about a doctor's diagnosis of hypertension.
- **Fit:** It has been used for hypertension awareness work, for example in [this analysis](https://link.springer.com/article/10.1186/s41043-023-00404-3).
- **Access:** It's free on request through [IIPS](https://www.iipsindia.ac.in/content/LASI-data) (see also the [catalog entry](https://www.iipsdata.ac.in/datacatalog_detail/5)). A harmonised version is available through [Gateway to Global Aging](https://g2aging.org).

**5. CHARLS (China Health and Retirement Longitudinal Study), ages 45+**
- **Measured BP:** BP and pulse were measured three times, per the [2011 user guide](https://charls.pku.edu.cn/en/data/User2011.pdf). Per the Gateway to Global Aging, non-blood biomarkers including BP were collected in Waves 1–3. There is also BP content in the 2020 wave.
- **Diagnosis question:** The health module asks whether a doctor has diagnosed hypertension.
- **Access:** Register on the CHARLS site at charls.pku.edu.cn and sign the user agreement. Data are free to registered researchers. Harmonised files are also on the [Gateway to Global Aging](https://g2aging.org/additional-resources/gateway-blog/05a8df66-b9ab-47de-879e-b0bde672798d).

## Suggestions
- **Harmonisation:** HRS, ELSA, LASI and CHARLS are all part of the Gateway to Global Aging family. Harmonised files there would save you recoding time and make cross-country comparison cleaner.
- **Awareness definition:** Define it as the share of people with measured hypertension (usually 140/90 or above, or on medication) who report a prior diagnosis. Use the same cut-offs in every survey.
- **Comparability:** Devices, number of readings and sampling frames differ between surveys. Note this in your methods.
- **Citations:** Take the exact version and wave-level documentation from each portal before you cite.

Sources:
- [NHANES BPQ 2021 documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm)
- [NBER NHANES mirror](https://data.nber.org/nhanes/2013-2014/BPQ_H.htm)
- [HRS sensitive data](https://hrsdata.isr.umich.edu/data-products/sensitive-health)
- [HRS New User Guide](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf)
- [ELSA at UKDS](https://datacatalogue.ukdataservice.ac.uk/studies/study/5050)
- [ELSA nurse visit guide](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/5050_waves_2-4-6-8_nurse_data_user_guide_v01_0.pdf)
- [LASI data at IIPS](https://www.iipsindia.ac.in/content/LASI-data)
- [LASI hypertension paper](https://link.springer.com/article/10.1186/s41043-023-00404-3)
- [CHARLS 2011 user guide](https://charls.pku.edu.cn/en/data/User2011.pdf)
- [Gateway to Global Aging, CHARLS](https://g2aging.org/additional-resources/gateway-blog/05a8df66-b9ab-47de-879e-b0bde672798d)