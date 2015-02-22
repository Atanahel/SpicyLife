#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'benoit'

import csv
import urllib

hostname='http://localhost:8080'

with open('data.tsv', 'rb') as csvfile:
    myReader = csv.reader(csvfile, delimiter='\t')
    keys=[]
    is_key=True
    for row in myReader:
        if is_key:
            for key in row:
                keys.append(key)
            is_key=False
        else:
            i=0
            entry=dict()
            for element in row:
                entry[keys[i]]=element
                i=i+1
            params_url = urllib.urlencode(entry)
            f = urllib.urlopen(hostname + "/add?%s" % params_url)
            print "element added"

print str(keys)
