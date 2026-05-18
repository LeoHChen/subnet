# Poseidon Subnet Design

This repo keeps the CPVSS subnet design in Markdown and generates shareable HTML.

## Everyday Edits

Edit the source document:

```bash
docs/cpvss-subnet-design.md
```

Then regenerate the current HTML page:

```bash
make html
```

This updates `index.html` only. Use this for normal minor edits.

The generated HTML includes:

- `Export PDF`, which opens the browser print/PDF flow.
- `Copy to Notion`, which copies clean HTML plus Markdown to the clipboard for pasting into a Notion page.
- An interactive tokenomics simulator with sliders for emission schedule, staking assumptions, and pool allocations, plus live line, pie, stake/reward, and APY charts.

## Major Releases

Only major releases should create a new versioned HTML snapshot.

```bash
make major-release RELEASE=v1.0.0
```

This updates:

- `release.json`
- `index.html`
- `releases/v1.0.0.html`

The generated pages show the major release name, release date, and source commit hash used to cut the release.
