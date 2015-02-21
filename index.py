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

def addInIndex(key,act):
    doc = search.Document(doc_id=key.urlsafe(),
    fields=[
            search.TextField(name='name', value=act.name),
            search.TextField(name='description', value=act.description),
            search.GeoField(name='position', value=search.GeoPoint(act.position.lat, act.position.lon))])
    search.Index(name=_INDEX_NAME).put(doc)
    #TODO check it was added

class RebuildIndexHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('Rebuilding Index!')
        index=search.Index(name=_INDEX_NAME)
        results = index.search("")
        for res in results:
            index.delete(res.doc_id)

        searchQuery = Activity.query()
        searchList = searchQuery.fetch()
        for p in searchList:
            addInIndex(p.key,p)
        logging.info(searchList)



app = webapp2.WSGIApplication([
    ('/rebuildIndex', RebuildIndexHandler)
], debug=True)