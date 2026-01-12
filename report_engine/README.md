# MAPA-RD Report Engine

A strict, premium PDF report generation engine using Playwright and Jinja2.

## Structure
- `/theme`: Contains strictly defined CSS variables (`tokens.css`).
- `/templates`: Jinja2 templates.
- `/schemas`: JSON Schema for input validation.
- `/sample_data`: Baseline JSON and assets.

## Usage

```bash
python run_report.py <path_to_json>
```

## Requirements
- Python 3.11+
- Playwright (`pip install playwright` && `playwright install chromium`)
- Jinja2
- jsonschema

## Rules
- **No external calls** (CDNs disabled in renderer).
- **Strict Validation**: Missing fields or assets cause immediate failure.
- **Premium Styling**: Only use variables from `tokens.css`.
