import googlemaps
import os

gmaps = googlemaps.Client(key='AIzaSyAkYWSuQTwm_W8j1EPHaGaZsPiClyDpwHU')

# Geocode an address
geocode_result = gmaps.geocode('126 parasol, ashmore, qld')

# Look up place details by address
#places_result = gmaps.places(query='restaurants in Ashmore QLD', location=(-28.0167, 153.3833))

print(geocode_result)
#print(places_result)