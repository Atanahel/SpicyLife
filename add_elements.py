#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'benoit'

import urllib

params = {"name" : "Musee",
          "zipcode" : "1006",
          "address" : "Quai d'Ouchy 1",
          "city" : "Lausanne"}

params_url = urllib.urlencode(params)
f = urllib.urlopen("http://localhost:8080/add?%s" % params_url)
print f.read()

params = {"name" : "Victoria Hall",
          "zipcode" : "1204",
          "address" : "Rue du Général-Dufour 14",
          "city" : "Geneve"}

params_url = urllib.urlencode(params)
f = urllib.urlopen("http://localhost:8080/add?%s" % params_url)
print f.read()