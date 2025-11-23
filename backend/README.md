# OpenBookLoad Backend

Web novel scraper and ebook converter. Scrapes novels from supported websites and converts them to ebook formats.

## Setup

Requires Python 3.12.8 (see `.python-version`). If using pyenv: `pyenv local 3.12.8`

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Install [Calibre](https://calibre-ebook.com/download) for ebook conversion (AZW3 format).

## Run

```bash
python main_console.py
```

## Tests

```bash
pytest tests/
```

## Adding Support

### New Website

1. Create scraper class in `services/` (see `services/honeyfeed.py`)
2. Add website to `Website` enum in `services/conversion_service.py`
3. Add case to `_scrape_novel()` method in `ConversionService`

### New Output Format

1. Add format to `OutputFormat` enum in `services/conversion_service.py`
2. Implement converter method (e.g., `_convert_to_epub()`)
3. Add case to `run()` method in `ConversionService`
