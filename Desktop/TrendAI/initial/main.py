from geopy.geocoders import Nominatim
import tweepy
import snscrape.modules.twitter as sntwitter

def temp_input():
    pname = input("Product Name: ")
    pdesc = input("Product Description: ")
    pincode = input("Pincode: ")
    return pname, pdesc, pincode

def get_coordinates(pincode):
    geolocator = Nominatim(user_agent="trendai_app")
    location = geolocator.geocode({'postalcode': pincode})
    if location:
        return location.latitude, location.longitude, location.address
    else:
        print("Invalid pincode or location not found.")
        return None, None, None

def twitter_api_setup():
    api_key = '3FIkN5Hi9nQeFhJ1Rm8OKvSZ0'
    api_secret = 'S96cbpyVWftn71kU0AeUmsqCx0AcmXoqnIWVL603vgOYzuMvrJ'
    access_token = '1850515550994391041-S3bEooZRqzq5Cicju28uARsi7nPjzQ'
    access_token_secret = 'eYFQxOMjDUfxKDSQebGnzVRhMnHye9xnfQHx4Yxo3CodY'

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_woeid(api, latitude, longitude):
    # Get available trend locations
    closest_loc = None
    min_distance = float('inf')

    # Get all locations that Twitter has trending topic info for
    available_locs = api.available_trends()

    for loc in available_locs:
        loc_lat = loc['lat']
        loc_long = loc['long']
        distance = ((latitude - loc_lat) ** 2 + (longitude - loc_long) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_loc = loc

    if closest_loc:
        woeid = closest_loc['woeid']
        return woeid
    else:
        print("WOEID not found for the location.")
        return None

def get_trends(api, woeid):
    try:
        trends_result = api.get_place_trends(id=woeid)
        trends = [trend['name'] for trend in trends_result[0]['trends']]
        return trends
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return []

def get_trends_for_location(api, latitude, longitude):
    woeid = get_woeid(api, latitude, longitude)
    if woeid:
        trends = get_trends(api, woeid)
        return trends
    else:
        return []

def main():
    # Step 1: Get user input
    product_name, product_description, pincode = temp_input()

    # Step 2: Get coordinates
    latitude, longitude, address = get_coordinates(pincode)
    if not latitude or not longitude:
        return

    print(f"Location found: {address}")

    # Step 3: Set up Twitter API
    api = twitter_api_setup()

    # Step 4: Get trends for location
    trends = get_trends_for_location(api, latitude, longitude)
    if trends:
        print(f"\nTop trends in your area:")
        for trend in trends[:10]:
            print(trend)
    else:
        print("No trends found for your location.")

if __name__ == "__main__":
    main()
