# Blind audit instructions (given to the auditor agent, one case at a time)

You are auditing two answers to the same research question. Both answers
recommend datasets. Your job is to check every recommended dataset against its
official page and record what you find. You are not told how either answer was
produced, and you should not try to guess; judge only what is written.

## Inputs

In the folder you are given:

- `question.md`: the question a researcher asked.
- `answer_A.md` and `answer_B.md`: two answers.

## What to do

1. Read the question and write down its must-have requirements: what a dataset
   needs for this question (population, modality, the outcome or label, scale,
   and any access or licence constraint the researcher stated).
2. For each answer, list every dataset it presents as a candidate or
   recommendation. Leave out datasets the answer itself says are unsuitable or
   mentions only as a warning.
3. For each listed dataset, find its official page: the repository that hosts the
   data or the data owner's own site. Open it. Do not rely on memory for access
   conditions; they change.
4. Record, for each dataset:
   - `exists`: `true` if the dataset exists as the answer describes it; `false`
     if you cannot find any such dataset, or the name or link points to something
     else; `null` only if the site could not be reached at all.
   - `access_stated`: what the answer says about how the data is obtained, in a
     few words, or `"not stated"`.
   - `access_marked`: how the answer itself marked that statement: `"today"` if
     it says the fact was checked or confirmed in this session or cites a source
     for it, `"memory"` if it says the fact is recalled, from memory or not
     confirmed, `"none"` if the answer gives no indication either way.
   - `access_correct`: `true` if that statement agrees with the official page;
     `false` if it does not (for example the answer says or implies a free
     download and the page requires an application, training, a signed agreement
     or institutional approval, or the reverse); `null` if the answer made no
     statement or the page does not settle it.
   - `meets_must_haves`: `true` if, from the official documentation, the dataset
     satisfies every must-have of the question; `false` if it clearly misses one
     (say which in `note`); `null` if the documentation does not let you tell.
   - `official_url`: the page you used.
   - `note`: one sentence with the evidence, quoting the page where the answer
     was wrong.

Apply exactly the same standard to both answers. An answer is not better for
being longer, more confident or better formatted; only the facts count.

## Output

Write `audit.json` in the same folder:

```json
{
  "must_haves": ["..."],
  "A": [
    {"dataset": "...", "official_url": "https://...", "exists": true,
     "access_stated": "...", "access_marked": "today", "access_correct": true,
     "meets_must_haves": true, "note": "..."}
  ],
  "B": [ ]
}
```

Then reply with the number of datasets you audited in each answer and nothing
else about which answer seemed better.
