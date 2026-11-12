"""Source adapters: one module per dataset registry.

Each adapter module in this package defines:

    NAME         short lower-case identifier, e.g. "datacite"
    DESCRIPTION  one line: what the registry covers and when to use it
    search(query, limit=20) -> list of records (scoutlib.common.make_record)

and may define:

    HOSTS                 tuple of host names whose landing pages it understands
    lookup(url_or_id)     -> one record with the registry's own metadata, or None

Adapters are discovered automatically; adding a file here is enough.
"""
from __future__ import annotations

import importlib
import pkgutil


def load_sources():
    """Return {NAME: module} for every adapter that imports cleanly.

    A broken adapter must not take the others down, so import errors are
    collected under the key "_errors" instead of being raised.
    """
    sources = {}
    errors = {}
    for info in pkgutil.iter_modules(__path__):
        if info.name.startswith("_"):
            continue
        try:
            module = importlib.import_module("%s.%s" % (__name__, info.name))
        except Exception as exc:  # pragma: no cover - defensive
            errors[info.name] = "%s: %s" % (type(exc).__name__, exc)
            continue
        name = getattr(module, "NAME", None)
        if name and callable(getattr(module, "search", None)):
            sources[name] = module
    if errors:
        sources["_errors"] = errors
    return sources


def source_for_url(url, sources=None):
    """Return the adapter that understands this landing-page URL, or None."""
    from urllib.parse import urlsplit

    host = urlsplit(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    for name, module in (sources or load_sources()).items():
        if name == "_errors":
            continue
        for known in getattr(module, "HOSTS", ()):
            if host == known or host.endswith("." + known):
                if callable(getattr(module, "lookup", None)):
                    return module
    return None
