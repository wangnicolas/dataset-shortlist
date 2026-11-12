---
name: dataset-shortlist
description: Find real, obtainable datasets for a research question. Searches dataset registries and the literature, verifies that every dataset exists, states exactly how it can be accessed (open download, free account, application, institutional agreement) and under which licence, checks the fit against the question, and renders an interactive shortlist page. Use this skill whenever the user asks what data exists or is available for a topic, where to get data for a study, thesis, paper, model or benchmark, whether a public or open dataset exists for something, for alternatives to a dataset, or how to get access to one, even if they never say "dataset" (for example "I want to study X, what could I use?"). Also use it before proposing datasets from memory in any research-planning conversation.
license: MIT
compatibility: Needs Python 3.9 or newer (standard library only) and outbound HTTPS. Web search and page fetching tools are used when available.
---

# dataset-shortlist

A researcher asks "I want to study X. What data can I actually get?" Your job is to
hand back a short list they can act on today: datasets that really exist, with the
truth about how to obtain each one, what its licence permits, and whether it
contains what the question needs.

## Why this skill exists

Answering this question from memory fails in five predictable ways, and each one
costs the researcher days or weeks:

1. **Datasets or links that do not exist.** A plausible name with a dead or
   invented URL.
2. **"Publicly available" that is not.** Much of the most valuable research data
   needs an application, training, a signed agreement or an institutional
   signature. Calling it public sends someone to plan a project around data they
   will not have for two months, or ever.
3. **Stopping at the famous five.** Memory returns the datasets everyone already
   knows. The well-fitting, less crowded dataset is usually one registry search
   away.
4. **Fit asserted, not checked.** A dataset about the right topic that lacks the
   one variable or label the question depends on is not a candidate.
5. **Stale facts.** Versions, licences and access rules change.

The answer to these is not to say less. An answer from memory already contains
most of the right names and many of the right facts; what it lacks is checking.
So this skill keeps everything you know, adds what the registries and the
literature know, and then marks every fact by how it is known: confirmed today
from a named source, or recalled and not confirmed. **Never drop something useful
because you could not confirm it. Say it, and say that it is unconfirmed.**

## Tools

The skill ships a small command line tool. Every call has this form, where
`<skill-dir>` is the directory that contains this file (write the full path each
time; shell variables do not survive between tool calls):

```bash
python3 <skill-dir>/scripts/scout.py <command> [arguments]
```

The commands, shown without that prefix:

```text
sources                                   the registries it can search
search "<short query>" --out dataset-shortlist/candidates.json
                                          repeat with other queries: results accumulate, duplicates merge
search "<short query>" --source <registry> --out dataset-shortlist/candidates.json
add dataset-shortlist/candidates.json --title "<name>" --url <landing page>
                                          a dataset you know, or found in a paper or on the web
papers --query "<topic>"                  papers on the question, with abstracts (three sources, tried in turn)
papers --dataset "<dataset name>"         papers that use a dataset
papers --doi <dataset doi>                works that cite a dataset
show dataset-shortlist/candidates.json        numbered digest of all candidates
verify dataset-shortlist/candidates.json --pick 2,5,9,14 --out dataset-shortlist/verified.json
verify --url <url> --url <url>            quick check of one or two pages
lookup <landing page or DOI>              one registry record in full
read <url> [<url> ...]                    what a page says about access and licence, as quotable sentences
render dataset-shortlist/shortlist.json --out dataset-shortlist.html
```

Each command prints a short numbered digest (registry, access condition, licence,
year, title, link); the complete records are in the `--out` file. Use
`show <file> --pick 3,7` when you need every field of particular records. Keep
working files in a `dataset-shortlist/` folder inside the user's current working
directory. Do not write inside the skill directory.

The tool needs only Python and network access. If a command fails, read the error:
one registry being down is normal and the others still answer. A registry that
does not answer in time is reported as such and skipped. Behind an HTTP proxy the
registries are searched one after another, which is slower but complete. If the tool cannot
run at all, carry on with web search and page fetching and apply the same rules by
hand, and tell the user that the registry search was skipped.

## Workflow

### 1. Write down what the question needs

Before searching, turn the request into a short requirement list, because every
later step is checked against it:

- the unit of observation and the population or setting
- the modality (tabular, time series, images, text, audio, ...)
- the variables that must be present, above all the **outcome or label**
- scale: rough minimum size, time span, geography
- constraints: must it be downloadable today, or can the user wait for an
  application? commercial use? redistribution? credentials they already hold?

Mark each requirement as must-have or nice-to-have and give it an id (R1, R2, ...).
Infer what you can from the request and state your assumptions in the answer. Ask
the user a question only when the answer would change which datasets qualify and
you cannot reasonably assume it; one question, not an interview.

### 2. Collect candidates by four routes

Aim for twenty or more raw candidates before judging any of them. Each route
finds datasets the others miss, so use all four. The registry tool alone misses
whatever lives on a project site, in a code repository or in a field portal,
which is where many well-used datasets are published.

**What you already know.** Start by writing down every dataset you can recall
that might fit, including the ones you suspect are a poor match. Memory is a good
source of names and a weaker source of facts: use it to make sure nothing the
user would expect is missing, and treat what it says about access, licence and
contents as unconfirmed until a source agrees. Find each one's official home (a
registry search by name, then a web search) and `add` it.

**Registries.** Run `search` with four to six different short queries. Registries
match keywords literally, so a full sentence finds nothing; vary the task name,
the modality, the population and synonyms ("intensive care", "ICU", "critical
care"). Use `--source` to go deeper in a registry that fits the field; see
`references/sources.md` for what each one covers.

**Literature.** Run `papers --query` for the research question, favouring
reviews, benchmarks and recent work, and read the abstracts for the datasets
those papers used. What published researchers managed to obtain and use is the
best evidence of what is usable, and this is the route that finds the datasets
you have never heard of. Do it even when the first two routes already produced a
list. Then find each named dataset's home page and add it as a candidate.

**Web.** Search for the repositories and portals of the field that the registry
tool does not cover: statistics offices, domain archives, consortium data portals,
challenge and competition pages, project sites and code repositories. Ask "which
organisation would hold this kind of data?" rather than only "which dataset?".
`references/repositories-by-field.md` lists them by field with their usual access
pattern.

Everything you find goes into the candidates file with `add` and through the same
verification.

Expect noise in registry results: paper supplements filed as datasets, software
packages, records that only share a keyword. Skim the digest and carry forward
the candidates that could plausibly meet the must-haves.

### 3. Verify every candidate

Run `verify` on the candidates you intend to consider (`--pick` takes their
numbers from the digest). It confirms each dataset through its registry's own
record where it can, resolves DOIs, and otherwise checks the landing page, and it
fills in licence, version, size and access condition from the registry.

Never give a URL you built by guessing its pattern; a guessed address that
happens to look right is how dead links get into answers. Give links that the
tool or a fetch returned.

**Find the original before you give up on a dataset.** When a dataset turns up
only as a third-party copy, or has no registry record, its home is somewhere
else: the project page, the code repository, the publisher's portal. Search the
web for it and run `verify --url` on that page.

**A dataset that fits stays in the answer whether or not it verified.** If it
was confirmed, say so. If it was not, list it under "Known, not confirmed" with
what you know about it, what you tried, and what the user should check. Leaving
out a dataset the user would expect, without a word, is as unhelpful as
recommending one that does not exist.

Read what the verifier says about each record, because it corrects three
things silently otherwise:

- **A different name.** "Describes a different resource" means the link exists
  but the registry calls it something else; use the registry's title shown in
  the digest, or drop the name. A record listed under the registry's title keeps
  the name you gave in its notes.
- **A disagreement about access.** When the registry that hosts the data and
  another record disagree, the host's statement is used and the other claim is
  kept as a conflict. Mention the conflict if it matters to the user.
- **An old version.** A link to an old version is answered with that version's
  access policy and licence, and the digest names the latest version and its
  terms. Recommend the latest unless the user needs the old one.

"Could not check" and "does not exist" are different findings. Some sites refuse
automated clients; the verifier reports that as blocked. That is not evidence
against the dataset.

### 4. Establish how the data is actually obtained

This is the part researchers most need and most often get wrong. For every
dataset in the answer, state:

- **the access condition**, in plain words: direct download; free account or
  click-through terms; application, credentialing or training with approval by the
  data owner; institutional agreement, ethics approval, access committee, fee or
  secure environment; or not obtainable
- **the concrete steps** and a realistic **time to access** (minutes, days, weeks,
  months)
- **the licence** and what it means for this user: commercial use, redistribution,
  derived works, attribution, and any special clause
- **how you know**: confirmed today, with the source, or from memory

The registry record tells you that a condition exists. The details that decide a
project are on the access page: who approves a request, what training is
required, whether each study needs its own approval, what a free tier covers,
which countries or institutions are eligible. For every dataset that is not a
plain direct download, and for any whose record is silent, work down this list
until you have them:

1. the registry record (`verify`, `lookup`). For every dataset that is not a
   plain download, `verify` also prints what its landing page says about access
   ("access page says: ..."). Quote those sentences.
2. a separate access, terms or licence page, when the landing page points to
   one: `read <url>` prints its sentences about access and licence
3. your own page-fetching tool, when `read` is refused
4. a web search for the owner's access instructions, frequently asked questions,
   the repository's record of the dataset, or the data availability statement of
   the paper that describes it
5. what you remember, stated plainly and labelled "from memory, not confirmed
   today"

Step 5 matters. When a site cannot be read, do not replace what you know with
"not confirmed". Write the access condition you believe applies, mark it as
recalled, and tell the user where to confirm it. A researcher can act on "an
application form and a signed agreement, from memory" and cannot act on a blank.

Read `references/access-and-licences.md` for how to tell the conditions apart and
for the traps, in particular:

- An open-access *paper* does not make its *data* open.
- A copy of restricted data on a sharing site does not change the original terms.
  Point to the official source and do not recommend unofficial mirrors.
- "Available on request from the authors" is not a public dataset.
- For data about people, the agreement may forbid passing records to third-party
  services, which can include online AI tools. If the user plans that, check the
  agreement and say what you found. See `references/health-data.md` for health and
  biomedical data.

Do not present a recalled access condition as confirmed, and do not call data
open on the strength of memory alone when the stakes are a planned project: say
"open, from memory" and let the user see the difference.

### 5. Check the fit, requirement by requirement

For each candidate, look at its documentation (variable list, data dictionary,
README, the describing paper; `read <url> --find "<word>"` helps) and judge every
requirement: met, partly met, not met, or unknown, each with the evidence. Pay
most attention to the outcome or label, the population and the sample size.

Three cases need care:

- **Different releases of one dataset.** An open release may lack something that
  a restricted release contains, such as raw recordings behind a derived-feature
  release. That dataset is still a candidate: say what each release contains and
  what the fuller one requires.
- **Well-known datasets that do not fit.** Put them under "Not recommended" with
  the reason. "You would think X fits, but it has no Y" saves the user the detour,
  and they will otherwise wonder why it is missing.
- **Fit you could not check.** Say "unknown" and what to look at; do not assume
  from the title.

### 6. Find evidence of use

For the top candidates run `papers --dataset` or `papers --doi` and pick one to
three papers that used the dataset for a similar purpose. This shows the data is
workable, gives the user a baseline and a citation, and reveals whether the
dataset is saturated or under-used. Report only papers the tool or a fetch
returned in this session.

### 7. Rank and answer

Rank by: meets the must-haves, then how soon the user can have the data, then
size, quality and evidence of use. Give the user the full picture: every dataset
that fits, in order, usually five to ten. Do not trim away fitting datasets to
keep the list short, and make sure it is not only the famous ones when good
lesser-known candidates exist. Always point out what the user could start on
today if anything qualifies, and say clearly when nothing does.

**Build the interactive page first, then reply.** Write the shortlist as JSON
following `references/shortlist-schema.md` and run `render`. The page lets the
user filter, compare, tick datasets and export an access plan. Doing this before
you write the reply means the reply is your last message and can point to the
page.

**The reply must stand on its own** and must be the last thing you write: the
user may read only that message. Everything they need to decide goes in it; the
page is a companion, not a substitute. Use this structure:

```markdown
## What I assumed you need
(the requirement list, with assumptions marked)

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
(one row per dataset that fits; Access in plain words, e.g. "application required, ~2 weeks";
 Checked is "today" or "from memory")

## Details
(per dataset: link, what it contains, why it fits, what is missing,
exact access steps, licence in one line, one to three papers that used it)

## Known, not confirmed
(datasets that fit as far as you know but whose record, access terms or contents
you could not confirm today: what you know, what you tried, what to check)

## Not recommended, and why
## What I could not find
## Next step
```

Every row of the shortlist states an access condition. "Not confirmed" alone is
never an entry; write what you believe and how you know it. State the date of
the check, because access rules and licences change, and end with the path of
`dataset-shortlist.html`.

## Budget

A full scout takes roughly twenty-five to forty tool calls: recalling what you
know, four to six searches, two or three literature queries, one or two
verification runs, a page read for each dataset that needs its access terms, the
page, the reply. If you are well past that, stop widening the search and answer
with what you have, saying what you did not get to. A complete answer about
eight datasets is worth more than an unfinished survey of thirty.

Independent steps do not depend on each other's output, so issue them together
when your environment allows several tool calls at once: the search queries of
step 2, the page reads of steps 4 and 5, the paper lookups of step 6.

## A quick pass for small questions

For "is there an open dataset of X?" or "where does dataset Y live?", do a light
version: two or three searches, verify the hits, state the access condition, and
answer in a few lines. Skip the page unless the user wants it.

## Honesty rules

- Mark every fact by how you know it: confirmed today from a named source, or
  recalled. Both belong in the answer; neither may pose as the other.
- Say what you searched and what you did not. If a registry was down or a route
  was skipped, the user should know the list may be incomplete.
- If nothing fits, say so, and offer the closest alternatives: a dataset that
  covers part of the need, a way to combine sources, or what collecting the data
  would take.
- Do not present a dataset as a recommendation only because it is famous, and do
  not leave one out only because you could not open its page.

## Reference files

- `references/sources.md` - what each registry in the tool covers and how to
  write queries that find things. Read it when choosing where to search.
- `references/repositories-by-field.md` - which repositories, portals and
  archives hold data in nineteen fields, with their usual access pattern. Read
  the sections for the fields your question touches before the web route.
- `references/access-and-licences.md` - how to determine and describe access
  conditions and licences. Read it before writing the access facts.
- `references/health-data.md` - extra rules for health and biomedical data. Read
  it whenever the data is about patients or human subjects.
- `references/shortlist-schema.md` - the JSON format for the interactive page.
  Read it before writing the shortlist file.
