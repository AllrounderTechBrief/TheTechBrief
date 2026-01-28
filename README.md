# Tech Brief (GitHub Pages + RSS + Free Summaries)

A modern, elegant static site that fetches trusted RSS feeds per category and publishes short AI-generated (TextRank) summaries without any paid APIs.

## Features
- Categories: AI News, Broadcast Tech, Enterprise Tech, Cybersecurity Updates, Mobile & Gadgets
- Free summarization: extractive TextRank via `sumy`
- Scheduled builds: GitHub Actions every 3 hours
- Automatic deployment to `gh-pages` (GitHub Pages)
- Brand kit (colors, fonts) and cookie banner
- GDPR-friendly legal pages

## Quick Start
1. Create a new GitHub repo and push this project.
2. Enable **Pages**: Settings → Pages → Branch: `gh-pages`.
3. The Action will run on schedule (or trigger via **Run workflow**). After it completes, your site is live at `https://<username>.github.io/tech-brief/`.

## Local Development
```bash
python -m venv .venv && source .venv/bin/activate
pip install feedparser beautifulsoup4 sumy python-slugify jinja2
python scripts/build.py
```
Open `site/index.html` locally to preview.

## Custom Domain (optional)
Later, point `thetechbrief.in` to GitHub Pages and add a `CNAME` file in `site/` with your domain.

## Notes
- Some RSS feeds may change paths; update `data/feeds.json` as needed.
- Image extraction is heuristic; not all feeds provide images.
- Summaries are extractive and may vary in quality; consider manual curation for featured posts.
