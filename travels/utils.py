import requests
from django.conf import settings


def find(address):
    address_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={address}&key={settings.MAPS_API_KEY}"
    address = requests.get(address_url).json()
    coord = address["results"][0]["geometry"]["location"]
    return coord['lat'], coord['lng']
