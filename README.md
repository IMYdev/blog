# Blogine
Lightweight blog engine that fetches Markdown posts from a GitHub repository and renders them as HTML.

## Features
- Upload a new post's Markdown file to the configured repo and it will appear on the blog's main page after a refresh.

- Compact and agile with a responsive layout, based on [Flask](https://flask.palletsprojects.com/en/stable/) and [skeleton css](https://getskeleton.com/).

## Requirements
Install the Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configuration
The GitHub repository used as the source for posts is configured in `app.py` (look for `GITHUB_REPO` and `RAW_BASE_URL`).

- If your posts repo is public, no extra auth is needed.
- For private repos, add authentication to the fetch logic in `app.py`

Posts are expected to be Markdown files with a small metadata header, a blank line, then the Markdown content.
Metadata header should look like this:
`Title: xxxx`
`Date: DD/MM/YY`
` `
`actual post content`

## Running the app
Start the app from the project root:

```bash
python app.py
```

The engine uses `waitress` by default. For development and local testing you can also run with Flask's built-in server (set `FLASK_APP=app.py`) then `python app.py`

`waitress` will serve the app on `http://0.0.0.0:8080` unless you change the default configuration.

## Project structure
- `app.py` main Flask application and logic for fetching/parsing posts.
- `templates/` Jinja2 templates.
- `static/` CSS and JS assets.
- `requirements.txt` Python dependencies.
- `LICENSE` project license.

## Contributing
Small patches and fixes are welcome. Open an issue or submit a PR with a clear description and I shall check it.

## License
This project is licensed under the GPLv3 copyleft.