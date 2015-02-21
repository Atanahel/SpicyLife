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


class Activity(ndb.Model):
    """ Model representing a possible activity."""
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    city = ndb.StringProperty()
    website = ndb.StringProperty()
    description = ndb.StringProperty()
    long_description = ndb.StringProperty()
    price = ndb.FloatProperty()
    img_url = ndb.StringProperty()
    access = ndb.StringProperty() #train, car-only etc...
    time = ndb.StringProperty() #time of the day
    duration = ndb.FloatProperty() #duration of the activity
    requirements = ndb.StringProperty()
    position = ndb.GeoPtProperty()
    tags = ndb.StringProperty(repeated=True)