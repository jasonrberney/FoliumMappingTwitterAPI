import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from TwitterSearch import *
from geopy import geocoders
import folium
import time
import webbrowser
import os
from geopy.exc import GeocoderTimedOut

def geo(location):
    g = geocoders.Nominatim()
    loc = g.geocode(location, timeout=10)
    return loc.latitude, loc.longitude

# ask the user for location of where they want the map and what they want a map of
while True:
    where = raw_input('Where do you want a map of? ')
    try:
        #creates a map centered on the location specified using default configuration
        BerneyMap = folium.Map(location=geo(where), tiles='Mapbox Control room', zoom_start=8)
    except AttributeError:
        print "Cannot create map with given location. Please try again."
    else:
        break
    
# ask the user what they want to search Twitter for    
what = raw_input('What words would you like to search for?')

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([what]) # define all words to look for

    tso.set_include_entities(False) # don't give the entity information

    #object creation with secret token
    ts = TwitterSearch(
        consumer_key = 'XXX',
        consumer_secret = 'XXX',
        access_token = 'XXX',
        access_token_secret = 'XXX'
     )
    for tweet in ts.search_tweets_iterable(tso):
        twt = tweet['text']
        user = tweet['user']['screen_name']
        tweetContent = ( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
        if tweet['place'] is not None:
            print tweetContent
            time.sleep(.1)
            # relevance-based search by location and name
            (lat, lng) = geo(tweet['place']['full_name'])
            if lat == 0 and lng == 0:
                # relevance-based search by different location and name values
                (lat, lng) = geo(tweet['contributors'], ['coordinates'])
                if lat == 0 and lng == 0:
                    pass
            print '(' + str(lat) +', ' +str(lng)+')'
            # create markers and add them to the map
            folium.Marker([lat, lng], popup=tweetContent).add_to(BerneyMap)
        else:
            pass

except AttributeError:
    pass
 
# take care of all twitter errors
except TwitterSearchException as e: 
    print(e)

print "Done!"

#saves to whatever directory you're in
MyMap.save('MyMap.html')

#This will take the location of the map in our local directory and return the absolute path to it
webbrowser.open('file://'+ os.path.realpath('MyMap.html'))
