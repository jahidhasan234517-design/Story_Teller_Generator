# News Intelligence Dashboard

A modern Django-based news intelligence platform that fetches public, no-auth news data, classifies articles, calculates sentiment, extracts trending topics, and presents the results in a responsive analytics dashboard.

## Features

- Latest news feed with search and filtering
- Category classification using keyword heuristics
- Sentiment analysis for titles and summaries
- Trending score dashboard
- Top topics extraction and analytics
- Responsive dashboard UI with light and dark themes
- Bookmark functionality with SQLite storage
- JSON endpoints for charts and widgets
- Deployment-ready configuration for Render

## Technologies

- Python 3
- Django 4
- SQLite
- Bootstrap 5
- Chart.js
- Requests
- Feedparser
- TextBlob

## Public APIs Used

This application uses public APIs that do not require authentication or API keys:

- Hacker News Algolia API: https://hn.algolia.com/api
- Google News RSS: https://news.google.com/rss

## Installation

```bash
git clone <repository-url>
cd news_intelligence
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Fetch initial news data:

```bash
python manage.py fetch_news
```

Run the server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Management Command

```bash
python manage.py fetch_news
```

The command fetches data from public APIs, normalizes it, classifies the category, analyzes sentiment, extracts keywords, computes popularity/trending metrics, and stores the news articles in SQLite.

## Deployment

This project is prepared for Render deployment.

1. Push the project to GitHub.
2. Create a new Render web service.
3. Connect the repository.
4. Use the included `render.yaml`.
5. Set environment variables if needed.

## Testing

```bash
python manage.py test
```

## Project Structure

```text
news_intelligence/
├── manage.py
├── news_intelligence/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── news/
│   ├── management/
│   │   └── commands/
│   │       └── fetch_news.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── hackernews.py
│   │   ├── google_news.py
│   │   ├── categorizer.py
│   │   ├── sentiment.py
│   │   ├── keywords.py
│   │   └── news_service.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
├── static/
├── requirements.txt
├── build.sh
├── render.yaml
├── .env.example
└── README.md
```

## Screenshots Placeholder

- Dashboard overview with KPIs and charts
- Latest news cards with search and filters
- Trending stories and topic intelligence
- Analytics dashboard with Chart.js visualizations
- Bookmark management page

## Notes

This app is designed to be resilient when public APIs fail and relies on cached and previously stored data instead of exposing stack traces or failing completely.
