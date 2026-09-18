# StepMarked Legal

Public legal pages for the StepMarked iOS app.
The app source code lives in a separate private repository.

## Structure

```
public/
  privacy.md    <- source content (edit this)
  terms.md      <- source content (edit this)
  privacy.html  <- generated, this is what gets served
  terms.html    <- generated
  index.html    <- generated, links to both
tools/
  build.py      <- regenerates the HTML from the Markdown
```

Edit the `.md` files, then run:

```
python3 tools/build.py
```

Commit both the `.md` and the generated `.html`. CI regenerates them on
deploy as well, so the two can never drift apart.

## Live URLs

GitHub Pages serves this repo at:

- Privacy policy: `https://jjpeeradech.github.io/stepmarked-legal/privacy.html`
- Terms: `https://jjpeeradech.github.io/stepmarked-legal/terms.html`

The privacy URL is submitted to App Store Connect under
App Privacy > Privacy Policy URL. It must be publicly reachable
with no login.

## Deploy

**GitHub Pages** (current setup) — `.github/workflows/pages.yml` builds
`public/` and deploys it on every push to `main`. One-time setup in the
repo: Settings > Pages > Build and deployment > Source = **GitHub Actions**.
The repo must stay public, or Pages needs a paid plan.

**Cloudflare Pages** (alternative) — connect this repo, build command
`python3 tools/build.py`, output directory `public`.
