from __future__ import annotations

import scout


def _rec(tier, url, verified=True):
    return {"id": "x:1", "source": "x", "title": "Example", "url": url,
            "access": {"tier": tier, "evidence": "policy"},
            "verification": {"verified": verified, "final_url": url, "problems": [], "notes": []}}


def test_access_sentences_are_attached_to_records_that_need_more_than_a_download():
    pages = {
        "https://a.example.org/gated": {"matches": [
            "The cohort was recruited between 2015 and 2019 from registered clinics.",
            "To be granted access, the user must sign the data use agreement and submit a research proposal.",
            "Download the documentation here.",
            "Requests are reviewed by the data access committee within four weeks."], "problem": None},
    }
    seen = []

    def reader(url):
        seen.append(url)
        return pages[url]

    gated = _rec("gated", "https://a.example.org/gated")
    opened = _rec("open", "https://b.example.org/open")
    unverified = _rec("gated", "https://c.example.org/x", verified=False)
    assert scout._access_texts([gated, opened, unverified], reader=reader) == 1
    assert seen == ["https://a.example.org/gated"]            # open and unverified records are not read
    sentences = gated["verification"]["access_text"]["sentences"]
    assert any("sign the data use agreement" in s for s in sentences)
    assert any("data access committee" in s for s in sentences)
    assert not any("Download the documentation" in s for s in sentences)   # no access word that decides anything
    assert "access_text" not in opened["verification"]


def test_a_page_that_cannot_be_read_is_reported_not_hidden():
    rec = _rec("unknown", "https://blocked.example.org/data")
    scout._access_texts([rec], reader=lambda url: {"matches": [], "problem": "the site refused an automated client (HTTP 403)"})
    assert rec["verification"]["access_text"]["sentences"] == []
    assert "refused" in rec["verification"]["access_text"]["problem"]


def test_a_reader_that_raises_does_not_break_the_run():
    rec = _rec("gated", "https://odd.example.org/data")

    def reader(url):
        raise RuntimeError("boom")

    assert scout._access_texts([rec], reader=reader) == 0
    assert "boom" in rec["verification"]["access_text"]["problem"]
