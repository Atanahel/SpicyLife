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

_INDEX_NAME_2 = 'activities_2'

class RebuildIndexHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('Rebuilding Index!')
        index=search.Index(name=_INDEX_NAME)
        results = index.search("")
        for res in results:
            index.delete(res.doc_id)


        searchQuery = Activity.query()
        searchList = searchQuery.fetch()
        logging.info(searchList)







app = webapp2.WSGIApplication([
    ('/rebuildIndex', RebuildIndexHandler)
], debug=True)