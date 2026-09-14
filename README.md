# StepMarked Legal

Public legal pages for the StepMarked iOS app.
The app source code lives in a separate private repository.

## Structure

```
public/
  privacy.md    <- source content (paste here)
  terms.md      <- source content (paste here)
  privacy.html  <- generated, this is what gets served
  terms.html    <- generated
```

## Live URLs

- Privacy policy: `https://<domain>/privacy.html`
- Terms: `https://<domain>/terms.html`

The privacy URL is submitted to App Store Connect under
App Privacy > Privacy Policy URL. It must be publicly reachable
with no login.

## Deploy

**Cloudflare Pages** — connect this repo, build command: none,
output directory: `public`

**GitLab Pages** — uncomment `.gitlab-ci.yml`, then set
Settings > General > Visibility > Pages to **Everyone**
so the site is public even though the repo is private.
