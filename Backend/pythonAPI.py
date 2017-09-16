from zomato import Zomato
import urllib2
import json
from pprint import pprint

def cuisineTranslate(cuisine):
    return {
            'American': '1',
            'Chinese': '25',
            'Fast Food': '40',
            'French': '45',
            'Italian': '55',
            'Japanese': '60',
            'Mediterranean': '70',
            'Mexican': '73',
            'Thai': '95',
            'Vietnamese': '99',
            'Indian': '148',
            }.get(cuisine, '')

#Within ~100ft or .004 of a degree
#Pass lat long every 30 seconds to array, remove oldest if does average not fufill deviation of .004 degree 
#pastLocations 


searchLat = str(lat)
searchLon = str(lon)
cuisineType = cuisineTranslate(cuisine) #check against array and convert to numerical value
searchdistance = str(distance * 1609) #distance will be in km, Zomato api needs in meters
"""
lat = str(43.472285)
lon = str(-80.544858)
cuisineType = str(55)
distance = str(1 * 1000)
"""
#adds lat and long based on profiles current location
mapUrl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + searchlat + "," + searchlon + "&key=AIzaSyCN1nbMMdIdWb9o2sfr4MVV1AZVlJ8G_Ug"

#uses urllib2 library to open and load json file
mapResponse = urllib2.urlopen(mapUrl)
mapData = json.load(mapResponse)

#creates query needed for Zomato 
restQuery = "lat=" + searchLat + ", lon=" + searchLon + ", radius =" + searchDistance + ", cuisines=" + cuisineType
restKey = Zomato("309bf0bce94239a8585b1b209da93a3d")
restJSON = restKey.parse("search", restQuery)


print restJSON

