No public dataset lets you follow workers across employers for 10+ years with real firm identifiers. Every dataset that fits an AKM design is restricted. Some are much easier to get than others, and you can build and test your whole pipeline before you have any of them.

I wrote this from what I know, not from checking each provider's current rules today. Access rules change, so check the details on each provider's website before you plan around them.

## A point about your design

The within/between decomposition (as in Song et al. 2019) only needs firm IDs in each year's cross-section. AKM needs a lot of **movers** inside a connected set, and with few movers per firm you get serious limited-mobility bias in the variance components. So:
- Small worker samples (1–2% of workers) are weak for AKM, because most firms show up with one or two sampled workers.
- Plan to use a bias correction from the start: Kline–Saggio–Sølvsten (2020) leave-out, or the Bonhomme–Lamadon–Manresa clustering approach. Reviewers will expect it.

## The main options, from most to least realistic for a PhD student

**1. Portugal: Quadros de Pessoal (via BPLIM, Banco de Portugal)**
- Mandatory annual census of private-sector employers from the mid-1980s on (a few years are missing). It has worker and firm IDs, which makes it ideal for AKM. Card, Cardoso & Kline (2016, QJE) used it.
- Access: send a project proposal to BPLIM. If approved, you work on their remote server; output is checked before release, and you usually get test data to write code against. It is open to researchers outside Portugal.
- Realistic timeline: a few months from proposal to access. For a non-Portuguese student this is probably the most accessible full-census option.

**2. Germany: IAB data (via the FDZ, the IAB's research data centre)**
- **LIAB** (linked establishment survey and worker records) and **BHP** (establishment panel). The **AKM firm effects estimated by the IAB on the full employment register (IEB)** can be merged onto SIAB/BHP. That means you can study firm effects without estimating AKM on a 2% sample yourself.
- **SIAB** is a 2% worker sample covering decades. It's great for long careers but thin for estimating AKM yourself.
- Access: contract with the FDZ and a short project description. Work is done on-site at FDZ locations (in Germany, plus some at US universities) or by remote execution (JoSuA). You write code against **structure-identical test data you can get early**, then send it to run on the real data.
- Timeline: usually a few months. There is also a scientific-use file (SIAB-R) you can use at your own institution, but check whether it includes establishment IDs and whether your institution qualifies.

**3. Italy: Veneto Worker History (VWH) and INPS**
- VWH covers all private-sector employment in Veneto from the mid-1970s to around 2001 and was used by Card, Devicienti & Maida (2014). It has historically been available through the University of Padova with a signed agreement, which is fairly easy. Check its current status.
- Full national INPS data goes through the VisitINPS program: competitive proposals, with access on-site or remote. It's slower.

**4. Austria: Austrian Social Security Database (ASSD)**
- Full-population employment histories from 1972 with employer IDs. Access usually goes through a collaboration with a University of Linz / Vienna-based project, not an open application. You'd likely need a coauthor or advisor connection.

**5. US: LEHD (Census, via FSRDC)**
- Excellent data, but the hardest route: a full proposal to Census, a background check for Special Sworn Status, work only in an FSRDC, and disclosure review. Expect 6–18 months before you have access. State coverage depends on which states have agreed, and foreign nationals face extra residency requirements. The SSA data Song et al. used is basically not accessible.

**6. Nordic registers (Denmark IDA, Sweden, Norway, Finland FLEED) and the Netherlands (CBS)**
- These are top quality, but access usually has to go through an **authorized domestic institution**. For you that means a coauthor or visiting position there. Finland and the Netherlands (CBS Remote Access) are somewhat more open to foreign institutions, but charge fees.

**7. France (DADS / Panel tous salariés via CASD), UK (ASHE via ONS SRS / UKDS Secure Lab), Canada (CEEDD via StatCan RDCs)**
- All of these are possible. France usually needs a French partner institution, and CASD charges fees. ASHE is a 1% sample, so it's thin for AKM. Canadian access works best if you're at a Canadian university.

**Brazil: RAIS.** The free public RAIS microdata has **no worker or firm identifiers**, so it can't support AKM. The identified version needs an agreement with the Labor Ministry, which is now hard to get.

## What you can start right away

1. **Simulated data.** Build your full pipeline on synthetic worker–firm panels: connected set, AKM, KSS bias correction, decomposition over time. Two packages to look at:
   - `pytwoway` (Lamadon et al.) simulates AKM-type data and implements AKM, the KSS/homoskedastic corrections and the BLM approach.
   - The Kline–Saggio–Sølvsten `LeaveOutTwoWay` code (MATLAB) is the reference implementation of the leave-out correction.
   
   This is real progress on the project, not a placeholder. You'll learn how limited-mobility bias behaves at sample sizes like the ones you'll actually get.
2. **Test data from providers.** The IAB FDZ and BPLIM both give out test or dummy data with the same structure as the real files. Once your application is moving, your code can be ready the day access opens.
3. **Apply now.** I'd send a BPLIM (Portugal) proposal and an FDZ (Germany) application in parallel. Both are realistic within your PhD timeline, both have strong AKM literatures to benchmark against, and Germany's ready-made AKM effects give you a fallback if your own estimation gets slow.

## Practical advice

- Ask your advisor whether anyone in your department already has a data contract, an FSRDC project, or a Nordic or Austrian coauthor. Joining an existing project is often the fastest route by far.
- Write your proposals around the specific variables you need: the years, a firm ID that stays the same across years, a consistently defined earnings measure, and the topcoding rules. German earnings are censored at the social security ceiling, so you'll need imputation.

I can also set up a working simulation and AKM/KSS pipeline in Python in this directory so you have something running this week.