#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

act = Activity(name="Musee Olympique",
               address="Quai d'Ouchy 1",
               zipcode="1006",
               city="Lausanne",
               website="http://www.olympic.org/fr/musee",
               description="Le musée olympique est un musée consacré à l'histoire des Jeux olympiques inauguré le 23 juin 1993 à Lausanne en Suisse. Il est situé sur les hauteurs du quai d'Ouchy au bord du lac Léman. Il abrite des expositions permanentes et temporaires autour du sport et du mouvement olympique. Il est entouré d'un parc exposant de nombreuses œuvres d'art ayant pour thème le sport.",
               position=ndb.GeoPt(46.508001,6.634462))
#act.put()


class SearchHandler(webapp2.RequestHandler):
    def get(self):

        lat=46.5162554
        lng=6.6333172
        index = search.Index(_INDEX_NAME)
        query = "distance(position, geopoint(" + str(lat) + "," + str(lng) + ")) < 1000"

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
            obj['key']=p.key.id()
            obj['pos']={'lat' : obj['position'].lat , 'lng' : obj['position'].lon}
            del obj['position']
            list_obj.append(obj)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(list_obj))



class AddHandler(webapp2.RequestHandler):
    def get(self):

        name = self.request.get('name')
        address = self.request.get('address')
        zipcode = self.request.get('zipcode')
        city = self.request.get('city')
        website = self.request.get('website')
        description = self.request.get('description')

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
               position=pos)
        key = act.put()

        doc = search.Document(doc_id=key.urlsafe(),
        fields=[
                search.TextField(name='name', value=name),
                search.TextField(name='description', value=description),
                search.GeoField(name='position', value=search.GeoPoint(pos.lat, pos.lon))])
        search.Index(name=_INDEX_NAME).put(doc)
        logging.info('done')
        logging.info(doc)

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
    ('/search', SearchHandler),
    ('/add', AddHandler)
], debug=True)
