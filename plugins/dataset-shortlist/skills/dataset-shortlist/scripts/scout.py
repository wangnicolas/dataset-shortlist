#!/usr/bin/env python3
"""dataset-shortlist command line.

    python3 scout.py sources
    python3 scout.py search "ICU mortality time series" --out candidates.json
    python3 scout.py search "critical care outcome" --out candidates.json      # adds to the same file
    python3 scout.py add candidates.json --title "Some dataset" --url https://...
    python3 scout.py show candidates.json --pick 3,7
    python3 scout.py verify candidates.json --pick 1,3,7 --out verified.json
    python3 scout.py lookup https://example.org/record/1          # or a bare DOI
    python3 scout.py read https://example.org/record/1/access     # what a page says about access and licence
    python3 scout.py papers --query "early sepsis prediction" --limit 10
    python3 scout.py render shortlist.json --out dataset-shortlist.html

Every command prints a short digest that is cheap to read; the complete records
go to the --out file (or to stdout with --json). Standard library only,
Python 3.8+. Run it from any directory; it finds its own package next to this file.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scoutlib import common  # noqa: E402
from scoutlib.sources import load_sources, source_for_url  # noqa: E402

TIER_WORDS = {
    "open": "open", "account": "free account", "gated": "application",
    "controlled": "institutional", "closed": "not obtainable", "unknown": "access unknown",
}


# ------------------------------------------------------------------ small helpers

def _load_records(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict) and "records" in data:
        return data, data["records"]
    if isinstance(data, list):
        return {"records": data}, data
    raise SystemExit("%s: expected a list of records or an object with `records`" % path)


def _pick(records, spec):
    """Select records by 1-based position or by id; `spec` is like "1,4,7" or "zenodo:123,2"."""
    if not spec:
        return list(records)
    chosen = []
    by_id = {rec.get("id"): rec for rec in records}
    for token in [t.strip() for t in spec.split(",") if t.strip()]:
        if token.isdigit():
            index = int(token)
            if not 1 <= index <= len(records):
                raise SystemExit("--pick %s: the file has %d records" % (token, len(records)))
            chosen.append(records[index - 1])
        elif token in by_id:
            chosen.append(by_id[token])
        else:
            raise SystemExit("--pick %s: no record with that position or id" % token)
    return chosen


def _licence_word(rec):
    lic = rec.get("licence")
    if not lic:
        return "no licence stated"
    return lic.get("id") or ("custom: %s" % common.truncate(lic.get("name") or "terms", 40))


def _record_line(index, rec):
    tier = (rec.get("access") or {}).get("tier", "unknown")
    mark = ""
    ver = rec.get("verification")
    if ver is not None:
        mark = "VERIFIED " if ver.get("verified") else "NOT VERIFIED "
    year = rec.get("year") or "-"
    return "%2d. %s[%s | %s | %s | %s] %s\n    %s" % (
        index, mark, rec.get("source", "?"), TIER_WORDS.get(tier, tier), _licence_word(rec), year,
        common.truncate(rec.get("title") or "(no title)", 110), rec.get("url") or "(no url)")


_ROUTINE_NOTE = re.compile(r"filled from |^confirmed by |read from the landing page's own metadata|"
                           r"^the DOI \S+ is registered|^doi \S* ?(filled|read) |^title set to |^the link redirects to")


def _print_records(records, offset=0):
    for position, rec in enumerate(records, 1 + offset):
        print(_record_line(position, rec))
        ver = rec.get("verification") or {}
        given = (rec.get("extra") or {}).get("given_title")
        if given and common.norm_title(given) != common.norm_title(rec.get("title")):
            print("    given as: %s" % common.truncate(given, 110))
        found = ver.get("found_title")
        if found and common.norm_title(found) not in (common.norm_title(rec.get("title")), common.norm_title(given)):
            print("    %s title: %s" % ("registry" if ver.get("method") == "registry-api" else "page",
                                      common.truncate(found, 110)))
        for problem in ver.get("problems", []):
            print("    problem: %s" % problem)
        access_text = ver.get("access_text") or {}
        for sentence in access_text.get("sentences", []):
            print("    access page says: \"%s\"" % sentence)
        if access_text.get("problem") and not access_text.get("sentences"):
            print("    access page not read: %s" % common.truncate(access_text["problem"], 150))
        # Access hints, conflicts and "access unknown" are always printed; only routine
        # bookkeeping ("filled from", "confirmed by") is capped.
        routine_left = 2
        for note in ver.get("notes", []):
            if _ROUTINE_NOTE.search(note):
                if routine_left <= 0:
                    continue
                routine_left -= 1
            print("    note: %s" % note)


# ----------------------------------------------------------------------- commands

def cmd_sources(args):
    sources = load_sources()
    errors = sources.pop("_errors", {})
    if args.json:
        common.emit({"sources": [{"name": n, "description": getattr(m, "DESCRIPTION", "")}
                                 for n, m in sorted(sources.items())], "import_errors": errors})
        return 0
    for name, module in sorted(sources.items()):
        print("%-12s %s" % (name, getattr(module, "DESCRIPTION", "")))
    for name, error in errors.items():
        print("%-12s FAILED TO LOAD: %s" % (name, error))
    return 0


SEARCH_BUDGET = 30.0   # seconds a registry may take to answer one search (env DATASET_SCOUT_SEARCH_BUDGET)


def _search_budget():
    try:
        return max(0.1, float(os.environ.get("DATASET_SCOUT_SEARCH_BUDGET") or SEARCH_BUDGET))
    except ValueError:
        return SEARCH_BUDGET


_SKIPPED = {}   # source NAME -> malformed items skipped in its last search


def _search_one(module, query, limit):
    try:
        found = module.search(query, limit=limit)
        if getattr(found, "skipped", 0):
            _SKIPPED[getattr(module, "NAME", "?")] = found.skipped
        return list(found), None
    except common.FetchError as exc:
        return [], "FetchError: %s" % exc
    except Exception as exc:  # an adapter bug must not hide the other sources
        return [], "%s: %s" % (type(exc).__name__, exc)


def _run_searches(sources, chosen, query, limit, parallel, budget):
    """{name: (records, error)} for each chosen source.

    Each search runs in a daemon thread, so a registry that accepts the connection and
    never answers costs at most `budget` seconds and does not keep the process alive.
    Side by side, all sources share one deadline; one after another (behind a proxy,
    see common.parallel_allowed) each source gets the whole budget, so a slow early
    registry does not use up the time of the later ones.
    """
    def start(name):
        box = {}

        def run():
            box["result"] = _search_one(sources[name], query, limit)

        worker = threading.Thread(target=run, name="scout-search-%s" % name)
        worker.daemon = True
        worker.start()
        return worker, box

    def collect(name, worker, box, wait):
        worker.join(max(0.0, wait))
        result = box.get("result")
        if result is None:
            return [], "no answer within %g s; the search went on without this registry" % budget
        return result

    results = {}
    if parallel:
        running = {name: start(name) for name in chosen}
        deadline = time.monotonic() + budget
        for name in chosen:
            worker, box = running[name]
            results[name] = collect(name, worker, box, deadline - time.monotonic())
    else:
        for name in chosen:
            worker, box = start(name)
            results[name] = collect(name, worker, box, budget)
    return results


def cmd_search(args):
    sources = load_sources()
    import_errors = sources.pop("_errors", {})
    chosen = args.source or sorted(sources)
    missing = [name for name in chosen if name not in sources]
    if missing:
        sys.stderr.write("unknown source(s): %s; available: %s\n" % (", ".join(missing), ", ".join(sorted(sources))))
        return 2
    found, counts, errors = [], {}, dict(import_errors)
    # Different hosts, so running the sources side by side stays polite; behind a proxy they
    # run one after another, because some proxies cut bodies when several transfers overlap.
    results = _run_searches(sources, chosen, args.query, args.limit, common.parallel_allowed(), _search_budget())
    for name in chosen:
        records, error = results[name]
        counts[name] = len(records)
        if error:
            errors[name] = error
        found.extend(records)

    previous, queries = [], []
    if args.out and os.path.exists(args.out) and not args.replace:
        data, previous = _load_records(args.out)
        queries = list(data.get("queries", []))
    known = len(previous)
    known_ids = set()
    for rec in previous:
        known_ids.add(rec.get("id"))
        known_ids.update(item.get("id") for item in rec.get("also_found_in") or [] if isinstance(item, dict))
    merged = common.dedupe(previous + found)
    skipped = {name: _SKIPPED[name] for name in chosen if _SKIPPED.get(name)}
    queries.append({"query": args.query, "sources": chosen, "counts": counts, "errors": errors,
                    "at": common.now_iso()})
    if skipped:
        queries[-1]["skipped_items"] = skipped
    result = {"generated_at": common.now_iso(), "queries": queries, "n_records": len(merged), "records": merged}

    if args.json:
        common.emit(result)
    else:
        new = merged[known:]
        print("query: %s" % args.query)
        print("found per source: %s" % ", ".join("%s=%d" % (n, counts[n]) for n in chosen))
        for name, error in errors.items():
            print("SOURCE FAILED %s: %s" % (name, common.truncate(error, 160)))
        for name, count in skipped.items():
            print("note: %s returned %d malformed item%s, skipped" % (name, count, "" if count == 1 else "s"))
        if args.out:
            again = sum(1 for rec in found if rec.get("id") in known_ids)
            print("%d new, %d already in the file, %d merged with another copy, %d total in %s" % (
                len(new), again, max(0, len(found) - len(new) - again), len(merged), args.out))
        _print_records(new if args.out else merged, offset=known if args.out else 0)
    if args.out:
        common.emit(result, args.out)
    return 0 if merged or not errors else 1


def cmd_add(args):
    data, records = ({"records": []}, [])
    if os.path.exists(args.file):
        data, records = _load_records(args.file)
    fields = {}
    if args.doi:
        fields["doi"] = args.doi
    if args.note:
        # where the agent found it: not the dataset's description, which verify fills from the page
        fields["extra"] = {"found_via": args.note}
    url = args.url or ("https://doi.org/%s" % common.norm_doi(args.doi) if args.doi else None)
    if not url:
        sys.stderr.write("give --url or --doi\n")
        return 2
    key = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")[:60] or "untitled"
    record = common.make_record("manual", key, args.title, url, **fields)
    merged = common.dedupe(records + [record])
    data["records"] = merged
    data["n_records"] = len(merged)
    common.emit(data, args.file)
    if len(merged) == len(records):
        print("already in %s (same id, DOI, landing page or title); nothing added" % args.file)
    else:
        print("added as record %d of %s (unverified until you run verify)" % (len(merged), args.file))
    return 0


def cmd_show(args):
    _, records = _load_records(args.file)
    chosen = _pick(records, args.pick)
    if args.json or args.pick:
        common.emit(chosen)
    else:
        _print_records(chosen)
    return 0


_DOI_TARGET_RE = re.compile(r"^(doi:)?10\.\d{4,9}/\S+$", re.I)


def _ask(module, target):
    """(record, error message) from one adapter's lookup."""
    try:
        return module.lookup(target), None
    except common.FetchError as exc:
        return None, ("could not ask the %s registry (%s); this says nothing about whether the record exists"
                      % (module.NAME, common.truncate(exc.reason or str(exc), 160)))


def cmd_lookup(args):
    target = args.target.strip()
    sources = load_sources()
    sources.pop("_errors", None)
    is_doi = bool(_DOI_TARGET_RE.match(target))
    module = sources.get("datacite") if is_doi else source_for_url(target, sources)
    if module is None or not callable(getattr(module, "lookup", None)):
        sys.stderr.write("no registry adapter understands this; use `verify --url` for a generic check\n")
        return 1
    record, error = _ask(module, target)
    if error:
        sys.stderr.write(error + "\n")
        return 1
    if record is None:
        if module.NAME == "datacite":
            doi = re.sub(r"^doi:", "", target, flags=re.I) if is_doi else target
            sys.stderr.write("DataCite has no record for this DOI. It may be registered with another agency (Crossref, "
                             "mEDRA, ...), so this does not mean it does not exist: run `verify --url %s`\n"
                             % (doi if doi.startswith("http") else "https://doi.org/" + doi))
        else:
            sys.stderr.write("the %s registry has no public record for this address (it may not exist, or it may be "
                             "private); run `verify --url` to check the page itself\n" % module.NAME)
        return 1
    # A DOI record from DataCite: the registry that hosts its landing page knows the access rules.
    landing = (record.get("extra") or {}).get("landing_page") if module.NAME == "datacite" else None
    host = source_for_url(landing, sources) if landing else None
    if host is not None and host is not module:
        hosted, error = _ask(host, landing)
        if error:
            sys.stderr.write("note: %s; showing DataCite's record\n" % error)
        elif hosted is not None:
            for key in ("doi", "licence", "description", "creators", "year", "version", "size", "subjects"):
                if hosted.get(key) in (None, "", [], {}) and record.get(key) not in (None, "", [], {}):
                    hosted[key] = record[key]
            hosted.setdefault("extra", {})["datacite_access"] = record.get("access")
            sys.stderr.write("record from the %s registry, which hosts the DOI's landing page %s\n" % (host.NAME, landing))
            record = hosted
    common.emit(record, args.out)
    return 0


def cmd_read(args):
    from scoutlib import pageread

    status = 0
    for url in args.url:
        result = pageread.read_page(url, find=args.find)
        print(pageread.format_page(result))
        print("")
        if result.get("problem"):
            status = 1
    return status


_STRONG_ACCESS = re.compile(
    r"request|appl(?:y|ication|icant)|credential|agreement|\bDUA\b|approv|sign(?:ed|ing)?\b|training|committee|"
    r"restrict|regist|licen[cs]e|permission|\bfee\b|eligib|ethic|\bIRB\b|enclave|embargo|subscription|"
    r"freely|open access|without (?:registration|restriction)", re.I)
_ABOUT_OBTAINING = re.compile(r"\baccess\b|download|obtain|\bfiles?\b|\busers?\b|available (?:to|for|upon|on)|"
                              r"data use|terms of use|commercial", re.I)
_ABOUT_THE_STUDY = re.compile(r"approved (?:the|this) (?:study|project|protocol)|(?:study|project|protocol) was approved|"
                              r"ethical approval|ethics approval|informed consent|review board|helsinki", re.I)
ACCESS_TEXT_LIMIT = 8      # landing pages read per verify run
ACCESS_TEXT_SENTENCES = 4  # sentences kept per dataset


def _access_texts(records, reader=None):
    """Attach what each landing page says about access to the records that are not a plain download.

    The registry record says that a condition exists; the sentences that decide a
    project (who approves, what must be signed, what a free tier covers) are on
    the page. Reading them here means the agent sees them without a further step.
    Records that are open by their registry's own statement are left alone.
    """
    from concurrent.futures import ThreadPoolExecutor

    from scoutlib import pageread

    reader = reader or pageread.read_page
    todo = []
    for rec in records:
        ver = rec.get("verification") or {}
        tier = (rec.get("access") or {}).get("tier", "unknown")
        if not ver.get("verified") or tier == "open":
            continue
        url = ver.get("final_url") or rec.get("url")
        if url and url.startswith("http"):
            todo.append((rec, url))
        if len(todo) >= ACCESS_TEXT_LIMIT:
            break
    if not todo:
        return 0

    def one(item):
        rec, url = item
        try:
            return reader(url)
        except Exception as exc:      # reading a page must never break a verification run
            return {"problem": "%s: %s" % (type(exc).__name__, exc), "matches": []}

    workers = 4 if common.parallel_allowed() else 2
    with ThreadPoolExecutor(max_workers=min(workers, len(todo))) as pool:
        pages = list(pool.map(one, todo))
    attached = 0
    for (rec, url), page in zip(todo, pages):
        ver = rec.setdefault("verification", {})
        sentences = [m for m in page.get("matches") or [] if _STRONG_ACCESS.search(m)]

        def weight(text):
            # A sentence about obtaining the data outranks one about how the study itself was approved.
            score = len(_STRONG_ACCESS.findall(text))
            if _ABOUT_OBTAINING.search(text):
                score += 3
            if _ABOUT_THE_STUDY.search(text):
                score -= 4
            return score

        scored = sorted(enumerate(sentences), key=lambda pair: (-weight(pair[1]), pair[0]))
        keep = [text for _, text in sorted(pair for pair in scored[:ACCESS_TEXT_SENTENCES] if weight(pair[1]) > 0)]
        if keep:
            ver["access_text"] = {"url": url, "sentences": [common.truncate(text, 360) for text in keep]}
            attached += 1
        elif page.get("problem"):
            ver["access_text"] = {"url": url, "sentences": [], "problem": page["problem"]}
    return attached


def cmd_verify(args):
    from scoutlib import verify

    records = []
    if args.input:
        _, all_records = _load_records(args.input)
        records = _pick(all_records, args.pick)
    if args.url:   # with a file too: both are checked, nothing is dropped silently
        records = records + [{"title": None, "url": url} for url in args.url]
    result = verify.verify_records(records)
    if not args.no_read:
        _access_texts(result.get("records", []))
    if args.json:
        common.emit(result)
    else:
        checked = result.get("records", [])
        good = sum(1 for rec in checked if (rec.get("verification") or {}).get("verified"))
        print("verified %d of %d (checked %s)" % (good, len(checked), result.get("checked_at", "")))
        _print_records(checked)
    if args.out:
        common.emit(result, args.out)
        print("full records written to %s" % args.out)
    return 0


def _print_works(result):
    print("source: %s" % result.get("source"))
    for name, error in (result.get("errors") or {}).items():
        print("note (%s): %s" % (name, common.truncate(str(error), 200)))
    for position, work in enumerate(result.get("works", []), 1):
        link = ("https://doi.org/%s" % work["doi"]) if work.get("doi") else (work.get("url") or "")
        print("%2d. [%s | cited %s | %s] %s\n    %s" % (
            position, work.get("year") or "-", work.get("cited_by") if work.get("cited_by") is not None else "?",
            work.get("type") or "work", common.truncate(work.get("title") or "(no title)", 130), link))
        if work.get("abstract"):
            print("    abstract: %s" % common.truncate(work["abstract"], 600))


def cmd_papers(args):
    from scoutlib import literature

    if args.doi:
        result = literature.papers_citing(args.doi, limit=args.limit)
    elif args.dataset:
        result = literature.papers_mentioning(args.dataset, limit=args.limit)
    elif args.query:
        result = literature.search_papers(args.query, limit=args.limit, year_from=args.year_from)
    else:
        sys.stderr.write("give --query, --dataset or --doi\n")
        return 2
    if args.json:
        common.emit(result)
    else:
        _print_works(result)
    if args.out:
        common.emit(result, args.out)
    return 0


def cmd_render(args):
    from scoutlib import render

    with open(args.input, encoding="utf-8") as handle:
        shortlist = json.load(handle)
    path = render.render_report(shortlist, args.out)
    print("interactive shortlist written to %s" % path)
    for line in render.access_notes(shortlist):
        print(line)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="scout.py", description="Find, verify and present research datasets.")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("sources", help="list the registries this tool can search")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_sources)

    p = sub.add_parser("search", help="search registries; with --out, results accumulate in one candidates file")
    p.add_argument("query", help="short keyword query (registries match words literally)")
    p.add_argument("--source", action="append", help="restrict to this registry (repeatable); default: all")
    p.add_argument("--limit", type=int, default=12, help="max records per registry (default 12)")
    p.add_argument("--out", help="candidates file; new results are merged into it")
    p.add_argument("--replace", action="store_true", help="overwrite --out instead of merging")
    p.add_argument("--json", action="store_true", help="print complete records instead of the digest")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("add", help="add a dataset you found in a paper or on the web to a candidates file")
    p.add_argument("file")
    p.add_argument("--title", required=True, help="the dataset's name as its owner writes it")
    p.add_argument("--url")
    p.add_argument("--doi")
    p.add_argument("--note", help="where you found it, in a few words")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("show", help="print records from a file (digest, or full JSON with --pick or --json)")
    p.add_argument("file")
    p.add_argument("--pick", help="positions or ids, comma separated, e.g. 2,5,9")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("lookup", help="fetch a registry's own record for a landing-page URL or a DOI")
    p.add_argument("target")
    p.add_argument("--out")
    p.set_defaults(func=cmd_lookup)

    p = sub.add_parser("read", help="fetch a landing or access page and list what it says about access and licence")
    p.add_argument("url", nargs="+")
    p.add_argument("--find", help="also list sentences matching this regular expression, e.g. 'label|annotation'")
    p.set_defaults(func=cmd_read)

    p = sub.add_parser("verify", help="check that datasets really exist and fill in registry facts")
    p.add_argument("input", nargs="?", help="candidates file")
    p.add_argument("--pick", help="verify only these positions or ids, e.g. 1,3,7")
    p.add_argument("--url", action="append", help="verify this landing page (repeatable) instead of a file")
    p.add_argument("--no-read", action="store_true",
                   help="do not read the landing pages of datasets that need more than a download")
    p.add_argument("--out", help="write the verified records here")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("papers", help="papers on a topic, or papers that use a dataset")
    p.add_argument("--query", help="topic search")
    p.add_argument("--dataset", help="dataset name: papers that mention it")
    p.add_argument("--doi", help="dataset DOI: works that cite it")
    p.add_argument("--year-from", type=int, default=None)
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--out")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_papers)

    p = sub.add_parser("render", help="turn a shortlist JSON into an interactive HTML page")
    p.add_argument("input")
    p.add_argument("--out", default="dataset-shortlist.html")
    p.set_defaults(func=cmd_render)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    if args.command == "verify" and not args.url and not args.input:
        parser.error("verify needs a candidates file or --url")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
