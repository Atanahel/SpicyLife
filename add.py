#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from index import addInIndex

_INDEX_NAME = 'activities'


act = Activity(name="Musee Olympique",
               address="Quai d'Ouchy 1",
               zipcode="1006",
               city="Lausanne",
               website="http://www.olympic.org/fr/musee",
               description="Le musée olympique est un musée consacré à l'histoire des Jeux olympiques inauguré le 23 juin 1993 à Lausanne en Suisse. Il est situé sur les hauteurs du quai d'Ouchy au bord du lac Léman. Il abrite des expositions permanentes et temporaires autour du sport et du mouvement olympique. Il est entouré d'un parc exposant de nombreuses œuvres d'art ayant pour thème le sport.",
               position=ndb.GeoPt(46.508001,6.634462))
#act.put()

class AddHandler(webapp2.RequestHandler):
    def get(self):

        name = self.request.get('name')
        address = self.request.get('address')
        zipcode = self.request.get('zipcode')
        city = self.request.get('city')
        website = self.request.get('website')
        description = self.request.get('description')
        img_url = self.request.get('img_url')
        long_description = self.request.get('long_description')
        if self.request.get('price')=="":
            price = -1
        else:
            price = float(self.request.get('price'))
        access = self.request.get('access') #train, car-only etc...
        time = self.request.get('time') #time of the day
        if self.request.get('duration')=="":
            duration = -1
        else:
            duration = float(self.request.get('duration'))
        requirements = self.request.get('requirements')

        #check validity
        if name == "" or address == "" or city == "" or zipcode == "":
            logging.error("AddHandler : unsufficient parameters")
            self.error(422)
            return

        #find position if not given
        if self.request.get('lat') != "" and self.request.get('lng') != "":
            pos = ndb.GeoPt(self.request.get('lat') + ", " + self.request.get('lng'))
        else:
            pos = ndb.GeoPt(self._geocode(address + " " + zipcode + " " + city))


        act = Activity(name=name,
               address=address,
               zipcode=zipcode,
               city=city,
               website=website,
               description=description,
               position=pos,
               img_url=img_url,
               long_description=long_description,
               price=price,
               access=access,
               time=time,
               duration=duration,
               requirements=requirements)
        key = act.put()

        addInIndex(key,act)

    def _geocode(self,address):
        try:
            logging.info("Geocode address: %s", address)
            parameter = {'address': address.encode('utf-8'), 'sensor': 'false'}
            payload = urllib.urlencode(parameter)
            url = ('https://maps.googleapis.com/maps/api/geocode/json?%s' % payload)
            logging.info("Geocode URL: %s", url)
            result = urlfetch.fetch(url)
            jsondata = json.loads(result.content)
            logging.info(jsondata)
            location = jsondata['results'][0]['geometry']['location']
            coordinates = '%s,%s' % (location['lat'], location['lng'])
            logging.info("Geocode coordinates: %s", coordinates)
            return coordinates
        except:
            return "0.0,0.0"

app = webapp2.WSGIApplication([
    ('/add', AddHandler)
], debug=True)
