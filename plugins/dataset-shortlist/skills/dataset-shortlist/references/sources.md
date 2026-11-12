# Where to search

Read this when choosing where to look. Part 1 covers the registries the command
line tool searches directly. Part 2 covers the literature route. Part 3 maps
research fields to the repositories that hold their data, for the web route.

## Contents

1. The five registries in the tool
2. The literature route
3. Writing queries that find things
4. Repositories by field

## 1. The five registries in the tool

`search` queries all five side by side unless you pass `--source`.

| Registry | What it covers | Access and licence information | How to query it | Watch out for |
|---|---|---|---|---|
| `openaire` | An aggregator of datasets from thousands of repositories, in every field. Usually the most relevant results for a topical query. | Access flag is an aggregated claim and is often missing, which shows as "access unknown". Licence is given per copy when known. | Topic words work well. | Landing links are DOI links. Some records are papers filed as datasets. Clinical-trial registrations appear as datasets; they hold no data and show as access unknown. |
| `datacite` | The DOI registry behind most data repositories. Best used to confirm that a DOI exists and to read its publisher, licence and version (`lookup <doi>`). | Almost never states access; only standard open or restricted rights statements count. Licence from the record. | Words are combined with AND, so use two or three words, not a sentence. | Supplementary files of papers ("Additional file 3 of ...") appear as datasets. |
| `zenodo` | A general repository used in every field, including many small and recent datasets. | Explicit access flag (open, restricted, embargoed, closed), licence and file sizes. | Topic words; it tightens and loosens the query itself. | The licence is the uploader's choice. Paper supplements and software are mixed in. About 30 searches a minute without an account. |
| `huggingface` | Machine-learning datasets, strongest for text, speech, vision and benchmarks. | The gated flag says whether the Hub repository is gated, not where the data are. Not gated means direct download only when the Hub holds the data files; a repository with only a loading script shows "access unknown", because the script fetches the data from elsewhere, often under an agreement. Automatic gating means a free account and accepting terms; manual gating means the owner approves each request. | It matches names only. Search single distinctive words ("parkinson", "sentinel", "ecg"). | The licence is declared by the uploader. Copies of restricted datasets are sometimes uploaded by third parties; find and cite the official source instead. |
| `physionet` | Physiological signals and clinical research data: databases, challenges, models. | Explicit access policy for every project: open; logged-in users who sign the agreement; credentialed users with training and an agreement; approval by the contributor. | The tool ranks the whole catalogue by word overlap, so try the registry's own vocabulary and synonyms. | Ranking is by words, not meaning; weak matches appear when few projects fit. Custom agreements show as a licence with no id. |

A registry that fails prints `SOURCE FAILED`; the others still answer. Say in your
answer when a registry was unavailable.

The access condition shown as "access unknown" means the registry did not say. It
is not a finding about the dataset. Open the landing page and read it.

## 2. The literature route

`papers --query "<topic>"` returns papers with abstracts. Reviews, surveys and
benchmark papers are the most useful because they list many datasets at once.
Read the abstracts for dataset names, then find each dataset's official page.

- About one paper in five comes back without an abstract. Open the paper when it
  looks central.
- `papers --dataset "<name>"` ranks by citations, so the first hit is often the
  paper that introduced the dataset, and errata can appear. Skip those and pick
  papers that used the data for a purpose close to the user's.
- `papers --doi <doi>` needs a dataset that has a DOI and whose citations are
  indexed; an empty result is not evidence that nobody used it.
- Citation counts are those of the day you ran the command.
- Report only papers that the tool or a fetch returned in this session.

## 3. Writing queries that find things

- Keep queries to two to four words. Registries match words, not meaning.
- Search each of these angles separately: the task ("sleep staging"), the signal
  or modality ("polysomnography", "EEG"), the population or setting
  ("paediatric", "intensive care"), and the outcome or label ("apnea events").
- Use the vocabulary of the field as well as plain words, and both spellings
  where they differ ("paediatric" and "pediatric", "anaesthesia" and
  "anesthesia").
- When you know one fitting dataset, search for its name: neighbours, newer
  versions and derived collections often mention it.
- Search for the kind of collection, not only the topic: "challenge",
  "benchmark", "cohort", "registry", "survey", "corpus", "atlas".
- If the first queries return only famous names, the search is not finished.
  Change angle.

## 4. Repositories by field

The five registries above do not hold everything. Clinical records, genomic
data, survey archives, official statistics, earth observation, speech corpora
and many other kinds of data live in repositories of their own, often with their
own access process.

`repositories-by-field.md` (next to this file) maps nineteen fields to the
repositories, portals and archives that researchers in each field use, with the
usual access pattern and whether there is a search page or an API. Open its
contents list, then read only the sections for the fields your question touches,
and search those repositories with web tools. Datasets you find there go into
the candidates file with `add` and through `verify` like any other.
