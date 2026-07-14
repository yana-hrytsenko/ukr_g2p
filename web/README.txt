# Rushnyk

A rule-based Ukrainian phonetic transcription engine, with a small web UI
to try it live.

Type Ukrainian text and Rushnyk runs it through a real linguistic pipeline —
stress assignment, grapheme parsing, then phonemic → broad → narrow
phonological rules (voicing/articulation/softness assimilation, vowel
reduction, gemination, coarticulation) — and renders the result as:

- Ukrainian Cyrillic transcription (phonemic / broad / narrow)
- IPA (phonemic / broad / narrow)
- a rough English-friendly approximation

## Run it locally

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000**.

## How it's built

- `main/` — the transcription engine (pure Python, no framework
  dependencies beyond `ukrainian-word-stress` for stress placement)
- `app.py` — a thin Flask API (`POST /api/transcribe`) wrapping
  `main.transcribe()`
- `static/index.html` — a single-file frontend (vanilla JS, no build step)

The engine itself is organized as a pipeline of declarative rule objects:

```
text
  → preprocess / annotate / apply exceptions
  → stress assignment
  → grapheme parsing → phonemes
  → phonemic rules (assimilation)
  → broad rules (reduction, gemination, allophony)
  → narrow rules (fine coarticulation)
  → render (per target: Ukrainian / IPA / English-friendly)
```

## Deploy

**Render / Railway / Fly / any Heroku-style host:** the included
`Procfile` (`gunicorn app:app`) and `requirements.txt` are enough —
just point the platform at this repo.

**Hugging Face Spaces (Docker):** push this repo to a Space with the
Docker SDK — the included `Dockerfile` handles the rest.

**Any other host:** `python app.py` runs a plain Flask dev server on
`$PORT` (defaults to 5000); swap in `gunicorn app:app` for production.

## API

```
POST /api/transcribe
Content-Type: application/json

{ "text": "привіт" }
```

Returns all seven render modes for the given text in one response.
