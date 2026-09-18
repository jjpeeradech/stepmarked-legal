#!/usr/bin/env python3
"""Generate the served HTML in public/ from the Markdown sources.

The sources use a flat house style rather than full Markdown:
    Last updated: <date>     -> dateline, rendered under the title
    N. Section Title         -> <h2>
    • bullet                 -> <li>
    anything else            -> <p>
"""

import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

PAGES = [
    ("privacy", "Privacy Policy"),
    ("terms", "Terms of Use"),
]

SITE = "StepMarked"
SECTION_RE = re.compile(r"^\d+\.\s+\S")

STYLE = """
:root {
  color-scheme: light dark;
  --bg: #fbfaf8;
  --fg: #1c1b19;
  --muted: #6b675f;
  --rule: #e2ded6;
  --link: #9a5b2c;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #171614;
    --fg: #ece8e1;
    --muted: #9c968b;
    --rule: #33302b;
    --link: #d99a63;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  -webkit-text-size-adjust: 100%;
}
main { max-width: 42rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }
h1 { font-size: 1.9rem; line-height: 1.2; margin: 0 0 .35rem; letter-spacing: -.01em; }
h2 { font-size: 1.1rem; margin: 2.2rem 0 .6rem; letter-spacing: -.005em; }
p, li { margin: .7rem 0; }
ul { padding-left: 1.2rem; margin: .7rem 0; }
a { color: var(--link); }
.dateline { color: var(--muted); font-size: .9rem; margin: 0 0 2rem; }
.masthead { color: var(--muted); font-size: .8rem; letter-spacing: .09em;
  text-transform: uppercase; margin: 0 0 1.5rem; }
footer { margin-top: 3.5rem; padding-top: 1.25rem; border-top: 1px solid var(--rule);
  color: var(--muted); font-size: .9rem; }
footer a { margin-right: 1rem; }
"""


def shell(title, body, *, dateline=""):
    dateline_html = f'<p class="dateline">{html.escape(dateline)}</p>\n' if dateline else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {SITE}</title>
<meta name="robots" content="index, follow">
<style>{STYLE}</style>
</head>
<body>
<main>
<p class="masthead">{SITE}</p>
<h1>{html.escape(title)}</h1>
{dateline_html}{body}
<footer>
<a href="./privacy.html">Privacy Policy</a><a href="./terms.html">Terms of Use</a>
</footer>
</main>
</body>
</html>
"""


def linkify(text):
    """Escape, then turn bare email addresses into mailto links."""
    escaped = html.escape(text)
    return re.sub(
        r"([\w.+-]+@[\w-]+(?:\.[\w-]+)+)",
        r'<a href="mailto:\1">\1</a>',
        escaped,
    )


def render(source):
    dateline = ""
    out = []
    bullets = []

    def flush():
        if bullets:
            items = "\n".join(f"  <li>{b}</li>" for b in bullets)
            out.append(f"<ul>\n{items}\n</ul>")
            bullets.clear()

    for raw in source.splitlines():
        line = raw.strip()
        if not line:
            flush()
            continue
        if line.startswith("Last updated:") and not dateline and not out:
            dateline = line
        elif line.startswith("•"):
            bullets.append(linkify(line.lstrip("•").strip()))
        elif SECTION_RE.match(line):
            flush()
            out.append(f"<h2>{linkify(line)}</h2>")
        else:
            flush()
            out.append(f"<p>{linkify(line)}</p>")
    flush()
    return dateline, "\n".join(out)


def build_index(dateline):
    body = (
        "<p>Legal documents for the StepMarked iOS app.</p>\n"
        "<ul>\n"
        '  <li><a href="./privacy.html">Privacy Policy</a></li>\n'
        '  <li><a href="./terms.html">Terms of Use</a></li>\n'
        "</ul>"
    )
    return shell("Legal", body, dateline=dateline)


def main():
    last_dateline = ""
    for slug, title in PAGES:
        source = (PUBLIC / f"{slug}.md").read_text(encoding="utf-8")
        dateline, body = render(source)
        last_dateline = dateline or last_dateline
        (PUBLIC / f"{slug}.html").write_text(
            shell(title, body, dateline=dateline), encoding="utf-8"
        )
        print(f"wrote public/{slug}.html")

    (PUBLIC / "index.html").write_text(build_index(last_dateline), encoding="utf-8")
    print("wrote public/index.html")

    # Serve the files verbatim instead of running them through Jekyll.
    (PUBLIC / ".nojekyll").write_text("", encoding="utf-8")
    print("wrote public/.nojekyll")


if __name__ == "__main__":
    main()
