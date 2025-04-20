from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from .serializers import NewsRequestSerializer

NEWS_API_URL = "https://newsapi.org/v2/everything"
GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

class NewsScraper(APIView):

    def get(self, request):
        return render(request, 'fetch_news.html')  
    
    def post(self, request):
        serializer = NewsRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            pincode = serializer.validated_data.get('pincode')
            product = serializer.validated_data.get('product')  # Fetching product details

            # Step 1: Get location name using the pincode
            location_name = self.get_location_from_pincode(pincode)
            if not location_name:
                return Response({"error": "Invalid pincode or location not found."}, status=status.HTTP_400_BAD_REQUEST)

            query = f"{location_name} {product}" 
            params = {
                'q': query,
                'apiKey': settings.NEWS_API_KEY,
                'language': 'en'
            }

            try:
                response = requests.get(NEWS_API_URL, params=params)
                response.raise_for_status()  
                news_data = response.json()

                if news_data.get("status") != "ok":
                    return Response({"error": "Failed to fetch news."}, status=status.HTTP_400_BAD_REQUEST)

                articles = news_data.get("articles", [])
                return Response({"location": location_name, "product": product, "articles": articles}, status=status.HTTP_200_OK)

            except requests.exceptions.RequestException as e:
                return Response({"error": f"Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_location_from_pincode(self, pincode):
        try:
            headers = {
                "User-Agent": "my-news-app/1.0"
            }
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
        