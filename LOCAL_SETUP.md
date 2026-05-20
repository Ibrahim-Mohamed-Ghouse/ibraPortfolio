## Local run

Create a virtual environment, install the dependency, then start Streamlit:

```bash
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/streamlit run app.py
```

Then open `http://localhost:8501`.

## Notes

- The app entrypoint is `app.py`.
- Portfolio content is stored in `portfolio_content.py`.
- Styling lives in `static/css/site.css`.
- The CV download uses `static/docs/ibrahim-mohamed-ghouse-cv.pdf`.
- Hosting is intentionally left for later.
