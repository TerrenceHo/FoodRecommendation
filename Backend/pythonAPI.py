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


def queryAccept(query):

      #Variable Declaration
      searchLat = ""
      searchLon = ""
      cuisineType = ""
      priceLevel = ""
      searchDistance = "1"

      for key in query:
            if key == "lat":
                  searchLat = str(query["lat"])
            elif key == "lon":
                  searchLon = str(query["lon"])
            elif key == "cuisine":
                  cuisineType = cuisineTranslate(query["cuisine"])
            elif key == "price":
                  priceLevel = str(query["price"])
            elif key == "distance":
                  if query["distance"] == "20+":
                        searchDistance = str(24 * 1609)
                  else:
                  searchDistance = str(int(query["distance"]) * 1609)
            elif key == "time":

      '''      
      distanceRef = {"1":1, "5":5, "10":10, "15":15, "20":20, "20+":24}
      searchLat = str(lat)
      searchLon = str(lon)
      cuisineType = cuisineTranslate(cuisine) #check against array and convert to numerical value
      searchdistance = str(distance * 1609) #distance will be in km, Zomato api needs in meters
      #creates query needed for Zomato 
      '''
      restQuery = "lat=" + searchLat + ", lon=" + searchLon + ", radius =" + searchDistance + ", cuisines=" + cuisineType
      restKey = Zomato("309bf0bce94239a8585b1b209da93a3d")
      restJSON = restKey.parse("search", restQuery)
      return restJSON


distance = {"1":1, "5":5, "10":10, "15":15, "20":20, "20+":24}

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

