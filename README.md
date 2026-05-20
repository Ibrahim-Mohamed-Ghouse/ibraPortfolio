# Ibrahim Mohamed Ghouse — Portfolio

Personal portfolio site built with Streamlit. Dark-mode editorial layout with scroll-reveal animations, a horizontal project rail, and a consolidated credentials section.

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
app.py                  # entry point
portfolio_content.py    # all content (edit this to update the site)
static/
  css/
    site.css            # base styles
    site_improved.css   # layout overrides
  docs/
    ibrahim-mohamed-ghouse-cv.pdf
  index.html            # standalone static version
.streamlit/
  config.toml           # dark theme config
```

## Updating content

All text, experience, projects, education, and skills live in `portfolio_content.py`. No need to touch `app.py` for content changes.
