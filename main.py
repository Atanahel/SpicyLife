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

import os
import jinja2
import webapp2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Activity(ndb.Model):
    """ Model representing a possible activity."""
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    city = ndb.StringProperty()
    website = ndb.StringProperty()
    description = ndb.StringProperty()
    position = ndb.GeoPtProperty()
    tags = ndb.StringProperty(repeated=True)

act = Activity(name="Musée Olympique",
               address="Quai d'Ouchy 1",
               zipcode="1006",
               city="Lausanne",
               website="http://www.olympic.org/fr/musee",
               description="Le musée olympique est un musée consacré à l'histoire des Jeux olympiques inauguré le 23 juin 1993 à Lausanne en Suisse. Il est situé sur les hauteurs du quai d'Ouchy au bord du lac Léman. Il abrite des expositions permanentes et temporaires autour du sport et du mouvement olympique. Il est entouré d'un parc exposant de nombreuses œuvres d'art ayant pour thème le sport.",
               position=ndb.GeoPt(46.508001,6.634462))
act.put()


class SearchHandler(webapp2.RequestHandler):
    def get(self):


        searchQuery = Activity.query().order()
        searchList = searchQuery.fetch(30)

        list_obj=[]
        for p in searchList:
            obj=p.to_dict()
            obj['key']=p.key.id()
            obj['pos']={'lat' : obj['position'].lat , 'lon' : obj['position'].lon}
            del obj['position']
            list_obj.append(obj)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(list_obj))

app = webapp2.WSGIApplication([
    ('/search', SearchHandler)
], debug=True)
