#  News-Finder

**News-Finder** is a full-stack interactive news web app built with **FastAPI** and **ReactPy**.  
It allows users to explore the latest headlines, search for specific topics, browse news by category, view random articles, and even travel back in time to read old articles from the **New York Times Archive**.

---

##  Features

- **Homepage:** Displays top headlines from around the world.  
- **Search:** Search for articles using keywords (via [NewsAPI](https://newsapi.org)).  
- **Categories:** Browse by predefined topics — *sports, business, technology, entertainment, health, science.*  
- **Random Article Roulette:** Displays a random article with a fun “roulette” animation.  
- **Article Time Machine:** Fetches historical articles from the **New York Times Archive API** by date.  
- **Responsive Navigation:** Sidebar menu for easy access to all sections.  

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | FastAPI |
| **Frontend** | ReactPy (React-style components in Python) |
| **Routing** | ReactPy Router |
| **Async Networking** | httpx + asyncio |
| **APIs Used** | [NewsAPI.org](https://newsapi.org), [New York Times Archive API](https://developer.nytimes.com/) |
| **Styling** | Custom CSS (`styles.css`) |

---

##  Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/news-finder.git
cd news-finder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your API Keys
Replace the placeholder API keys in `main.py` with your own:
```python
# NewsAPI key
apiKey=your_newsapi_key_here

# New York Times API key
api-key=your_nyt_key_here
```
Get your keys here:
- [NewsAPI.org →](https://newsapi.org/)
- [NYT Developer Portal →](https://developer.nytimes.com/)

---

##  Run the App

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Then open the app in your browser:
```
http://127.0.0.1:8000
```

---

##  Project Structure

```
├── main.py          # Main FastAPI + ReactPy application
├── styles.css       # Frontend styles
├── requirements.txt # Dependencies
└── README.md        # Project documentation
```

---

##  Routes Overview

| Path | Description |
|------|--------------|
| `/` | Homepage — Top headlines |
| `/search` | Search for news articles |
| `/random_article` | Random news roulette |
| `/article_time_machine` | Old articles by date |
| `/category-<category>` | Category-specific news (e.g., `/category-sports`) |

---

##  How It Works

- **ReactPy** components handle UI rendering and client-side routing.
- **FastAPI** serves the app and CSS file.
- **httpx** handles async API requests to fetch articles.
- Data is dynamically rendered into cards using `render_news_list()`.

---

##  Example: Searching for Articles
Enter a keyword like `AI` or `space` and press **Search** — the app will fetch popular results from NewsAPI and display them instantly.

---

##  License

This project is licensed under the **MIT License** — feel free to modify and use it.
