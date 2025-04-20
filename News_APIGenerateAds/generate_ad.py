import requests
import openai
from news_storage import create_news_table, insert_news, fetch_news_from_db

NEWS_API_KEY = "b33c8cca84c44b1fb0960a066c40800e"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"
NEWS_API_URL = "https://newsapi.org/v2/everything"

create_news_table()

def get_location_from_pincode(pincode):
    headers = {"User-Agent": "news-ad-generator/1.0"}
    params = {
        'postalcode': pincode,
        'countrycodes': 'in',
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    try:
        response = requests.get(GEOCODE_API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            address = data[0].get("address", {})
            return address.get("city") or address.get("state") or address.get("village")
    except Exception as e:
        print(f"[ERROR] Geolocation failed: {e}")
    return None

def fetch_news(location, product):
    query = f"{location} {product}"
    params = {
        'q': query,
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return [article['title'] for article in articles if article.get('title')]
    except Exception as e:
        print(f"[ERROR] NewsAPI failed: {e}")
    return []

def generate_ads_with_gpt(product, location, headlines):
    prompt = f"""
    You're a professional digital advertiser. Based on the following location and product,
    and the recent news headlines related to it, generate 3 engaging and creative advertisement lines
    that could be used on social media or banners.

    Location: {location}
    Product: {product}
    Headlines:
    {chr(10).join(f"- {title}" for title in headlines[:3])}

    Be catchy, concise, and sell the product hard, but don't sound too robotic.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        print(f"[ERROR] OpenAI API failed: {e}")
        return []

def generate_gpt_ads(pincode, product):
    location, headlines = fetch_news_from_db(pincode, product)

    if not headlines:
        location = get_location_from_pincode(pincode)
        if not location:
            return {"error": "Invalid pincode or location could not be determined."}

        headlines = fetch_news(location, product)
        if not headlines:
            return {"error": "No relevant news found for this product in that location."}

        insert_news(pincode, product, location, headlines)

    ads = generate_ads_with_gpt(product, location, headlines)
    return {
        "location": location,
        "product": product,
        "ads": ads
    }

# Example usage
if __name__ == "__main__":
    pincode = input("Enter pincode: ")
    product = input("Enter product: ")
    result = generate_gpt_ads(pincode, product)

    print("\n--- Generated GPT Ads ---")
    for ad in result.get("ads", []):
        print(ad)