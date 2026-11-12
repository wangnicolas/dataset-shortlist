"""Hugging Face Hub adapter: machine-learning datasets.

The Hub search is a plain substring match on the repository id, so a natural
language query returns nothing. This adapter turns the query into up to three
short keyword searches, merges the hits and ranks them by how many of the
user's terms appear in the record plus popularity (downloads).

The `gated` flag says whether the Hub repository itself is gated; it is not proof
that the data can be downloaded from the Hub. Many repositories hold only a
loading script that fetches the data from somewhere else, often under an
agreement. So an ungated repository is called open (or a free-account one
"account") only with positive evidence that the Hub holds the data: the Hub's own
`format:` tag, or data files among the repository's files (`siblings`, returned
by the single-repository endpoint only). Otherwise the tier is `unknown`.

The licence comes from the `license:` tag, which the uploader declares: a mirror
of restricted data can carry a misleading licence, so the record says so in `extra`.
"""
from __future__ import annotations

import math
import re

from scoutlib import common

NAME = "huggingface"
DESCRIPTION = ("Hub for machine-learning datasets; substring search only (queries are split into "
               "keywords); explicit gated flag; licence is declared by the uploader.")
HOSTS = ("huggingface.co",)

API = "https://huggingface.co/api/datasets"
MAX_QUERIES = 3
PER_QUERY = 30

_STOP = set("""a an and are as at be by can do does for from has have how i in into is it its
of on or our that the their this to using use used via was were what when where which who
will with within without about across among between over under data dataset datasets
looking find need want study studying research disease diseases""".split())
_GENERIC = set("""time series prediction predict predicting recording recordings imagery image images
analysis model models learning classification detection forecasting forecast sample samples
collection database set open public""".split())


def keywords(query):
    """Distinct lower-case content words, most specific first."""
    words = []
    for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9\-]*(?:'s)?", query or ""):
        tok = re.sub(r"'s$", "", tok).lower().strip("-")
        if len(tok) > 1 and tok not in _STOP and tok not in words:
            words.append(tok)
    return words


def build_queries(query):
    """Up to three short search strings: specific words first, generic ones last."""
    words = keywords(query)
    if not words:
        return [(query or "").strip()] if (query or "").strip() else []
    specific = [w for w in words if w not in _GENERIC]
    generic = [w for w in words if w in _GENERIC]
    # longer words are rarer, so they are tried first; ties keep the user's order
    order = sorted(specific, key=lambda w: -len(w))
    if len(order) < MAX_QUERIES:  # generic words only fill spare slots
        order += generic
    return order[:MAX_QUERIES]


def _access(gated):
    if gated is False:
        return "open", "gated=false"
    if gated == "auto":
        return "account", 'gated="auto" (login and automatic acceptance of terms)'
    if gated == "manual":
        return "gated", 'gated="manual" (owner approves each request)'
    if gated is None:
        return "unknown", "gated flag missing"
    return "unknown", "gated=%r (unrecognised value)" % (gated,)


def _tags(tags, prefix):
    return [t[len(prefix):] for t in tags if t.startswith(prefix)]


# File types that hold data rather than documentation or code. Formats the Hub
# parses itself (csv, json, parquet, text, images, audio) also give a `format:` tag.
_DATA_EXT = set("""csv tsv json jsonl parquet arrow feather xlsx xls zip tar gz tgz bz2 xz zst 7z h5 hdf5 nc
mat npy npz nii dcm edf bdf fif set pkl pickle pt safetensors wav flac mp3 ogg m4a opus png jpg jpeg tif
tiff bmp webp mp4 avi mov mkv webm txt sqlite db""".split())


def _is_data_file(name):
    name = str(name or "")
    lower = name.lower()
    if lower.startswith("dummy/") or "/dummy/" in lower or "dummy_data" in lower:
        return False          # sample files that loading scripts ship for their own tests
    base = lower.rsplit("/", 1)[-1]
    if "." not in base or base.startswith("."):
        return False
    return base.rsplit(".", 1)[1] in _DATA_EXT and base not in ("requirements.txt", "license.txt", "readme.txt")


def _hosting(item, tier, evidence, tags):
    """Check an open or free-account tier against evidence that the Hub holds the data.

    Returns (tier, evidence, extra facts). `gated=false` only says the repository is
    not gated; a repository with nothing but a loading script gets `unknown`.
    """
    if tier not in ("open", "account"):
        return tier, evidence, {}
    formats = _tags(tags, "format:")
    siblings = item.get("siblings")
    names = None
    if isinstance(siblings, list):
        names = [s.get("rfilename") for s in siblings if isinstance(s, dict) and s.get("rfilename")]
    if formats:   # the Hub parsed data files in the repository itself
        return tier, "%s; the Hub detected data files (format:%s)" % (evidence, formats[0]), {}
    if names is None:
        return "unknown", ("%s, but the search listing does not show that the repository holds the data (no format: "
                           "tag); look the repository up before calling it %s" % (evidence, tier)), {}
    repo = str(item.get("id") or "").rsplit("/", 1)[-1].lower()
    scripts = sorted((n for n in names if n.lower().endswith(".py") and "/" not in n),
                     key=lambda n: n[:-3].lower() != repo)      # the script named after the repository first
    data = [n for n in names if _is_data_file(n)]
    stored = item.get("usedStorage")
    if scripts:
        facts = {"loading_script": scripts[0]}
        if not data or stored == 0:
            facts["loader_only"] = True
            return "unknown", ("%s, but the repository holds only a loading script (%s) and no data files; the script "
                               "fetches the data from elsewhere, where other terms may apply" % (evidence, scripts[0])), facts
        return "unknown", ("%s, but the repository holds a loading script (%s) and the Hub detected no data files; the "
                           "script may fetch the data from elsewhere, where other terms may apply"
                           % (evidence, scripts[0])), facts
    if data and stored != 0:
        return tier, "%s; the repository holds data files (%s)" % (evidence, data[0]), {}
    return "unknown", "%s, but the repository holds no data files (only %s)" % (
        evidence, ", ".join(names[:4]) or "no files"), {"no_data_files": True}


def _record(item):
    rid = item.get("id") or ""
    tags = [t for t in (item.get("tags") or []) if isinstance(t, str)]
    card = item.get("cardData") or {}
    tier, evidence = _access(item.get("gated"))
    tier, evidence, hosting = _hosting(item, tier, evidence, tags)
    lic = (_tags(tags, "license:") or [None])[0]
    if lic is None and isinstance(card.get("license"), str):
        lic = card["license"]
    if lic is None and isinstance(card.get("license"), list) and card["license"]:
        lic = str(card["license"][0])
    licence = common.normalise_licence(lic) if lic else None
    extra = {"gated": item.get("gated"), "repo_id": rid,
             "licence_declared_by": "uploader" if lic else None}
    if not lic:
        extra.pop("licence_declared_by")
        extra["licence_note"] = "no licence declared on the Hub"
    for key in ("disabled", "private"):
        if item.get(key):
            extra[key] = True
    extra.update(hosting)
    created = item.get("createdAt") or ""
    modified = item.get("lastModified") or ""
    size_cats = _tags(tags, "size_categories:")
    size = {"text": size_cats[0]} if size_cats else None
    subjects = (_tags(tags, "task_categories:") + _tags(tags, "task_ids:")
                + _tags(tags, "language:"))
    formats = _tags(tags, "modality:") + _tags(tags, "format:")
    usage = {}
    if item.get("downloads") is not None:
        usage["downloads"] = item["downloads"]
    if item.get("likes") is not None:
        usage["likes"] = item["likes"]
    desc = item.get("description") or ""
    desc = re.sub(r"Dataset Card for\s*\"[^\"]*\"", " ", desc)
    desc = re.sub(r"See the full description on the dataset page:.*$", "", desc)
    return common.make_record(
        NAME, rid, rid, "https://huggingface.co/datasets/%s" % rid,
        access_tier=tier, access_evidence=evidence,
        description=desc,
        publisher="Hugging Face Hub",
        creators=[item["author"]] if item.get("author") else [],
        year=int(created[:4]) if re.match(r"^\d{4}", created) else None,
        version=(item.get("sha") or "")[:10] or None,
        updated=modified[:10] or None,
        licence=licence, size=size, formats=formats, subjects=subjects,
        usage=usage, extra=extra,
    )


def _score(rec, words, rank_in_query):
    """Relevance first: covering more of the query's words beats popularity, which only
    orders repositories that match equally well (it is capped and weighs half)."""
    haystack = " ".join([rec["title"], rec["description"], " ".join(rec["subjects"])]).lower()
    id_text = rec["title"].lower()
    def weight(w):
        return 0.4 if w in _GENERIC else 1.0
    covered = sum(weight(w) for w in words if w in haystack)
    match = covered + sum(0.5 * weight(w) for w in words if w in id_text)
    downloads = (rec.get("usage") or {}).get("downloads") or 0
    return covered * 6.0 + match * 3.0 + 0.5 * min(math.log10(downloads + 1), 6.0) - 0.02 * rank_in_query


def search(query, limit=20):
    limit = max(1, int(limit))
    words = keywords(query)
    found = {}
    skipped = 0
    for kw in build_queries(query):
        data = common.get_json(API, params={"search": kw, "limit": PER_QUERY, "full": "true",
                                            "sort": "downloads", "direction": "-1"})
        if not isinstance(data, list):
            raise common.FetchError(API, None, "unexpected response shape")
        good = [(pos, item) for pos, item in enumerate(data)
                if isinstance(item, dict) and not item.get("private") and not item.get("disabled")]
        records = common.convert_items([item for _, item in good], _record, API)
        skipped += records.skipped
        positions = {item.get("id"): pos for pos, item in good}
        for rec in records:
            if rec["id"] not in found:
                found[rec["id"]] = (rec, positions.get(rec["title"], 0))
    specific = [w for w in words if w not in _GENERIC]
    if specific:  # substring hits such as "icu" inside "icub" are dropped
        pats = [re.compile(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(w)) for w in specific]
        found = {k: v for k, v in found.items()
                 if any(p.search(" ".join([v[0]["title"], v[0]["description"],
                                           " ".join(v[0]["subjects"])]).lower()) for p in pats)}
    scored = sorted(found.values(), key=lambda rp: -_score(rp[0], words, rp[1]))
    out = common.Results([rec for rec, _ in scored][:limit])
    out.skipped = skipped
    return out


def _repo_id(url_or_id):
    text = str(url_or_id or "").strip()
    m = re.search(r"huggingface\.co/(?:api/)?datasets/([^/\s?#]+(?:/[^/\s?#]+)?)", text, re.I)
    if m:
        return m.group(1)
    if re.fullmatch(r"[\w.\-]+(?:/[\w.\-]+)?", text):
        return text
    return None


def lookup(url_or_id):
    rid = _repo_id(url_or_id)
    if rid is None:
        return None
    try:
        item = common.get_json("%s/%s" % (API, rid))
    except common.FetchError as exc:
        # For a repository that does not exist (or is private) the Hub answers 401
        # "Invalid username or password", not 404: no public record, not a login problem.
        if exc.status in (401, 404):
            return None
        raise
    return _record(item)
