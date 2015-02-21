#!/usr/bin/env python
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

class Potatoes(ndb.Model):
    """Model representing potatoes transaction type."""
    type = ndb.StringProperty()
    quantity = ndb.FloatProperty()
    price = ndb.FloatProperty()
    sellable = ndb.BooleanProperty()


pot = Potatoes(type="Agata", quantity=10, price=5, sellable=True)
pot.put()



class MainHandler(webapp2.RequestHandler):
    def get(self):


        potatoes_query = Potatoes.query().order(-Potatoes.type)
        potatoes_list = potatoes_query.fetch(30)

        template_values = {
            'potatoes_list': potatoes_list}

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        #self.response.write(len(potatoes_list))

class PotatoesListHandler(webapp2.RequestHandler):
    def get(self):


        potatoes_query = Potatoes.query().order(-Potatoes.type)
        potatoes_list = potatoes_query.fetch(30)

        list_obj=[]
        for p in potatoes_list:
            obj=p.to_dict()
            obj['key']=p.key.id()
            list_obj.append(obj)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(list_obj))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/potatoes_list', PotatoesListHandler)
], debug=True)
