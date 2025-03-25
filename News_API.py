import requests

NEWS_API_URL = "https://newsapi.org/v2/everything"
GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"
API_KEY = "b33c8cca84c44b1fb0960a066c40800e"  


def get_location_from_pincode(pincode):
    try:
        headers = {"User-Agent": "my-news-app/1.0"}
        params = {
            'postalcode': pincode,
            'countrycodes': 'in',
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        }
        response = requests.get(GEOCODE_API_URL, params=params, headers=headers)
        response.raise_for_status()
        location_data = response.json()

        if location_data:
            address = location_data[0].get('address', {})
            city = address.get('city') or address.get('town') or address.get('village')
            state = address.get('state')
            return city or state
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None


def fetch_news(location_name):
    params = {
        'q': location_name,
        'apiKey': API_KEY,
        'language': 'en'
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        news_data = response.json()

        if news_data.get("status") != "ok":
            print("Failed to fetch news.")
            return []

        return news_data.get("articles", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return []


def main():
    pincode = input("Enter the pincode: ")
    location = get_location_from_pincode(pincode)

    if not location:
        print("Invalid pincode or location not found.")
        return

    print(f"Fetching news for {location}...")
    articles = fetch_news(location)

    if not articles:
        print("No news articles found.")
    else:
        for idx, article in enumerate(articles, 1):
            print(f"\n{idx}. {article.get('title')}")
            print(f"Source: {article.get('source', {}).get('name')}")
            print(f"URL: {article.get('url')}")


if __name__ == "__main__":
    main()