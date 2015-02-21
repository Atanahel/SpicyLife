#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'benoit'

import urllib
import webapp2

params1 = {"name" : "Musee",
          "zipcode" : "1006",
          "address" : "Quai d'Ouchy 1",
          "city" : "Lausanne"}
#params_url = urllib.urlencode(params)
#f = urllib.urlopen("http://localhost:8080/add?%s" % params_url)
#print f.read()

params2 = {"name" : "Victoria Hall",
          "zipcode" : "1204",
          "address" : "Rue du Général-Dufour 14",
          "city" : "Geneve"}

#params_url = urllib.urlencode(params)
#f = urllib.urlopen("http://localhost:8080/add?%s" % params_url)
#print f.read()

params3 = {"name" : "Vol en parapente biplace",
          "description" : "Volez comme un oiseau à Champoussin",
          "long_description" : "Notre prestaire se trouve à Champoussin, au cœur du Val d'Illiez. Fort de ces 25 ans d'expérience, il vous amènera au septième ciel durant 30 min de vol au dessus ",
          "price" : "119",
          "normal_price" : "130",
          "address" : "Route de Fayoz 1",
          "zipcode" : "1873",
          "address" : "Rue du Général-Dufour 14",
          "city" : "Val d'Illiez",
          "access" : "Par la route En train (gare à 3km) En Bus (arrêt à 500m)",
          "time" : "Matin Après-midi",
          "duration" : "0.5",
          "website" : "blahblah.com",
          "requirements" : "Bonnes chaussures fermées. Pantalon.",
          "img_url" : "http://img0.gtsstatic.com/wallpapers/a76987362eaae80fb8f827cbd713a486_large.jpeg"}

class AddHandler(webapp2.RequestHandler):
    def get(self):
        params_url = urllib.urlencode(params1)
        f = urllib.urlopen(self.request.host_url + "/add?%s" % params_url)
        params_url = urllib.urlencode(params2)
        f = urllib.urlopen(self.request.host_url + "/add?%s" % params_url)
        params_url = urllib.urlencode(params3)
        f = urllib.urlopen(self.request.host_url + "/add?%s" % params_url)

app = webapp2.WSGIApplication([
    ('/add_elements', AddHandler)
], debug=True)