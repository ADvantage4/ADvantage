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

def fetch_news(location_name, product):
    try:
        query = f"{location_name} {product}"
        params = {
            'q': query,
            'apiKey': API_KEY,
            'language': 'en'
        }
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        news_data = response.json()

        if news_data.get("status") != "ok":
            print("Failed to fetch news.")
            return []

        return news_data.get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def main():
    pincode = input("Enter pincode: ").strip()
    product = input("Enter product category: ").strip()
    
    location_name = get_location_from_pincode(pincode)
    if not location_name:
        print("Invalid pincode or location not found.")
        return

    print(f"Fetching news for {location_name} related to {product}...\n")
    articles = fetch_news(location_name, product)

    if articles:
        for idx, article in enumerate(articles[:5], start=1):  # Displaying top 5 articles
            print(f"{idx}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}\n")
    else:
        print("No relevant news found.")

if __name__ == "__main__":
    main()
