from __future__ import annotations

from scoutlib import common, pageread

PAGE = """<!doctype html><html><head><title>Example Cohort Data | Example Archive</title>
<style>.x{color:red}</style><script>var license = "should not appear";</script></head>
<body><nav>Home Search Login</nav>
<h1>Example Cohort Data</h1>
<p>Hourly measurements from 4,812 participants collected between 2015 and 2019.</p>
<h2>Access</h2>
<p>Access to the files requires a signed data use agreement. Applications are reviewed by the data access committee within four weeks.</p>
<p>The metadata are released under the Creative Commons Attribution 4.0 licence.</p>
<p>Contact the archive for questions.</p>
</body></html>"""


def test_reads_title_and_access_sentences(fake_http):
    fake_http({"archive.example.org/cohort": (200, PAGE)})
    result = pageread.read_page("https://archive.example.org/cohort")
    assert result["status"] == 200 and result["problem"] is None
    assert result["title"] == "Example Cohort Data | Example Archive"
    joined = " ".join(result["matches"])
    assert "requires a signed data use agreement" in joined
    assert "data access committee within four weeks" in joined
    assert "Creative Commons Attribution 4.0 licence" in joined
    assert "should not appear" not in joined and "should not appear" not in result["start"]
    assert "Hourly measurements" in result["start"]


def test_extra_pattern_is_listed_too(fake_http):
    fake_http({"archive.example.org/cohort": (200, PAGE)})
    result = pageread.read_page("https://archive.example.org/cohort", find="participants")
    assert any("4,812 participants" in sentence for sentence in result["matches"])


def test_refused_client_is_not_reported_as_missing(fake_http):
    fake_http({"blocked.example.org": (403, "<html><title>Forbidden</title></html>")})
    result = pageread.read_page("https://blocked.example.org/data")
    assert result["status"] == 403
    assert "refused an automated client" in result["problem"] and "may exist" in result["problem"]
    assert result["matches"] == []


def test_no_answer_is_not_reported_as_missing(fake_http):
    fake_http({})
    result = pageread.read_page("https://unreachable.example.org/data")
    assert result["status"] is None and "not evidence that the page does not exist" in result["problem"]


def test_javascript_shell_is_flagged(fake_http):
    fake_http({"spa.example.org": (200, "<html><head><title>Portal</title></head><body><div id='root'></div></body></html>")})
    result = pageread.read_page("https://spa.example.org/dataset/1")
    assert "JavaScript" in result["problem"]


def test_format_page_quotes_the_sentences(fake_http):
    fake_http({"archive.example.org/cohort": (200, PAGE)})
    text = pageread.format_page(pageread.read_page("https://archive.example.org/cohort"))
    assert "Sentences about access, licence and terms" in text
    assert "  - Access to the files requires a signed data use agreement." in text
