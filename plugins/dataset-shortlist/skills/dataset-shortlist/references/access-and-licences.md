# Access conditions and licences

How to find out, and how to say, what a researcher must do to obtain a dataset
and what they may do with it. Read this before writing the access facts of an
answer.

## Contents

1. The five access conditions
2. Where the evidence comes from
3. Words that signal an approval step
4. Mirrors and derived copies
5. Licences in one line each
6. What to write for each dataset

## 1. The five access conditions

| Condition | What you will see | What to tell the user | Typical time |
|---|---|---|---|
| **Open** | Files download from the landing page with no login. Registry flags such as `access_right=open`, `gated=false` with the data files on the Hub, access policy "Open". | "Download directly", with the link. | minutes |
| **Free account** | A login, or terms accepted online with no human review. Flags such as `gated=auto`, or a policy that says any logged-in user who accepts the agreement may download. | Create the account, accept the terms, download. | minutes to an hour |
| **Application** | A request reviewed by the data owner, credentialing of the researcher, a required training certificate, a named reference or supervisor. Flags such as `gated=manual`, `access_right=restricted`, "credentialed", "contributor review", "request access". | The steps in order, who approves, which documents are needed. | days to weeks |
| **Institutional** | An agreement signed by the institution's legal signatory, ethics approval, a data access committee, a fee, analysis only inside a secure environment, or limits on country or type of institution. | That a supervisor or the institution must be involved, and to start early. | weeks to months |
| **Not obtainable** | Embargoed, withdrawn, "available on request from the authors", or metadata only. | That it is not a dependable source, and why. | n/a |

The tool reports these as `open`, `account`, `gated`, `controlled`, `closed`,
plus `unknown` when the registry does not say. Use the plain words above when
writing to the user.

When one dataset has parts under different conditions (an open subset and a
restricted full version, or open metadata with restricted files), describe each
part. The open part is often enough to start with.

## 2. Where the evidence comes from

In order of trust:

1. The registry's own record: the `access.tier` and `access.evidence` fields in
   the verifier output name the field and value they were read from.
2. The landing page's access, files or terms section. Quote the sentence.
3. The data use agreement or licence text itself.
4. The data availability statement of the paper that describes the dataset. It
   can be out of date; prefer the landing page when they disagree.

Never infer the access condition from any of these:

- the describing paper being open access
- the dataset being widely used or famous
- a copy existing on a code or dataset sharing site
- a download button that is visible before logging in
- the licence alone: an open licence on a record whose files are restricted
  still means the files are restricted

If none of the four sources settles it, state the condition you believe applies,
mark it "from memory, not confirmed today", and say what you checked and where
the user can confirm it. A blank helps nobody; a recalled fact presented as
checked misleads.

## 3. Words that signal an approval step

Finding any of these on a landing page means the data is not a direct download,
even if the page also says "publicly available": request access, apply, data use
agreement, DUA, credentialed, required training, ethics approval, IRB, data
access committee, DAC, controlled access, managed access, safe haven, secure
enclave, bona fide researcher, institutional signing official, signed by your
institution, available upon reasonable request.

"Publicly available" in a paper often means "available to researchers who
apply". Report what the process is, not the adjective.

## 4. Mirrors and derived copies

- A copy uploaded by a third party does not change the terms set by the data
  owner, and the licence shown on the copy is whatever the uploader typed.
  Recommend the official source. Mention a mirror only to warn about it.
- Preprocessed or benchmark versions built from a restricted source inherit its
  restrictions. Usually the user needs access to the source first; say so.
- When the same dataset appears in several registries, describe it once and use
  the record from the repository that actually hosts the files.

## 5. Licences in one line each

| Licence | What it means for the user |
|---|---|
| CC0, PDDL, public domain | Any use, no conditions. |
| CC BY, ODC-By | Any use, including commercial, with attribution. |
| CC BY-SA, ODbL | Any use with attribution; derived data must carry the same licence. |
| CC BY-NC (and NC-SA) | No commercial use. Flag this for anyone in or working with a company. |
| CC BY-ND (and NC-ND) | No distribution of modified versions. Flag this for anyone who would publish a derived dataset. |
| MIT, Apache, BSD on data | Permissive; treat like CC BY. |
| Custom agreement (the tool shows `licence.id` as null) | Read it. Look for: permitted purposes, redistribution, sharing with third parties and online services, publication or acknowledgement duties, expiry and deletion clauses. Do not summarise it from its name. |
| None stated | Reuse rights are unclear; by default nothing is granted. Say so and suggest asking the owner. |

The version number in a licence id from the tool is a best guess; the original
name is kept beside it. A licence chosen by an uploader, as on general
repositories and model hubs, is a claim, not a guarantee.

## 6. What to write for each dataset

One or two sentences that a researcher can act on, for example:

> Access: application required. Create an account, complete the required
> training, and submit the request with a description of your project; approval
> by the data owner usually takes one to two weeks. Licence: custom data use
> agreement; no redistribution, and results must cite the dataset paper.

> Access: direct download, no account. Licence: CC BY 4.0, commercial use
> allowed with attribution.

Give time estimates as typical ranges, not promises, and add the date you
checked.
