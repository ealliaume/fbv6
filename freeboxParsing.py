#! /usr/bin/env python
# -*- coding: iso-8859-1 -*- 
import cookielib
import os
import urllib
import urllib2
import re


class freeboxParsing(object):
    def __init__(self, data):
	self.data=data
        self.loopData()

    def loopData(self):
	print self.data
	for line in self.data:
		print line
