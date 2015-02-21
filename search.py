#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'benoit'

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import search
import os
import jinja2
import webapp2
import json
import logging
import urllib
from activity import Activity

_INDEX_NAME = 'activities'


act = Activity(name="Musee Olympique",
               address="Quai d'Ouchy 1",
               zipcode="1006",
               city="Lausanne",
               website="http://www.olympic.org/fr/musee",
               description="Le musée olympique est un musée consacré à l'histoire des Jeux olympiques inauguré le 23 juin 1993 à Lausanne en Suisse. Il est situé sur les hauteurs du quai d'Ouchy au bord du lac Léman. Il abrite des expositions permanentes et temporaires autour du sport et du mouvement olympique. Il est entouré d'un parc exposant de nombreuses œuvres d'art ayant pour thème le sport.",
               position=ndb.GeoPt(46.508001,6.634462))
#act.put()


from math import radians, cos, sin, asin, sqrt
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        #extract location
        if self.request.get('lat')!="" and self.request.get('lng')!="":
            query_lat=float(self.request.get('lat'))
            query_lng=float(self.request.get('lng'))
        elif self.request.get('address')!="":
            try:
                location=self._geocode(self.request.get('address'))
                query_lat=float(location['lat'])
                query_lng=float(location['lng'])
            except:
                logging.error("Unable to find location from address : "+self.request.get('address'))
                self.error(500)
                return
        else:
            logging.error("Search : No location information given")
            self.error(500)
            return

        #extract search radius
        if self.request.get('rad')!="":
            query_rad=int(self.request.get('rad'))
        else:
            query_rad=200000

        #search query
        index = search.Index(_INDEX_NAME)
        query_string = "distance(position, geopoint(" + str(query_lat) + "," + str(query_lng) + ")) < " + str(query_rad)

        sort_options=search.SortOptions(
            expressions=[
                search.SortExpression(expression="distance(position, geopoint(" + str(query_lat) + "," + str(query_lng) + "))",
             direction=search.SortExpression.ASCENDING, default_value=999999.99)],
            limit=1000)
        query_options=search.QueryOptions(limit=20,sort_options=sort_options)
        query=search.Query(query_string=query_string, options=query_options)

        #get corresponding values in datastore
        keys=[]
        try:
            results = index.search(query)
            for doc in results:
                logging.info('Document ! ' + str(doc.doc_id))
                keys.append(ndb.Key(urlsafe=doc.doc_id))
        except search.Error:
            logging.exception('Can not search index!')
            return

        logging.info(keys)
        searchList = ndb.get_multi(keys=keys)

        list_obj=[]
        for p in searchList:
            obj=p.to_dict()
            obj['key']=p.key.urlsafe()
            obj['pos']={'lat' : obj['position'].lat , 'lng' : obj['position'].lon}
            obj['dist']=haversine(obj['position'].lat,obj['position'].lon,query_lat,query_lng)
            del obj['position']
            list_obj.append(obj)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(list_obj))

    def _geocode(self,address):
        logging.info("Geocode address: %s", address)
        parameter = {'address': address.encode('utf-8'), 'sensor': 'false'}
        payload = urllib.urlencode(parameter)
        url = ('https://maps.googleapis.com/maps/api/geocode/json?%s' % payload)
        logging.info("Geocode URL: %s", url)
        result = urlfetch.fetch(url)
        jsondata = json.loads(result.content)
        logging.info(jsondata)
        return jsondata['results'][0]['geometry']['location']

app = webapp2.WSGIApplication([
    ('/search', SearchHandler),
], debug=True)