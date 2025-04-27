import requests

NEWS_API_KEY = '352d4c81be7d4b93a82927f05962b1fb'  # Replace with your actual NewsAPI key
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'

def fetch_news_articles(query: str, max_results: int = 5):
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': max_results,
        'apiKey': NEWS_API_KEY
    }

    try:
        response = requests.get(NEWS_API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print("[DEBUG] Unexpected API status:", data.get("status"))
            return []

        # Extract and return article info without strict string matching
        articles = [
            {
                'title': article.get('title', 'No Title'),
                'description': article.get('description', ''),
                'content': article.get('content', ''),
                'url': article.get('url', '#')
            }
            for article in data.get('articles', [])
        ][:max_results]

        # Debug log for verification
        print(f"[INFO] Retrieved {len(articles)} articles for query: '{query}'")

        return articles

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch news articles: {e}")
        return []
