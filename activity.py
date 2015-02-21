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
    position = ndb.GeoPtProperty()
    tags = ndb.StringProperty(repeated=True)