#! /usr/bin/env python
# -*- coding: iso-8859-1 -*- 
import cookielib, os, urllib, urllib2, re


class fb(object):
    def __init__(self, login, passwd, url):
        cookie_filename = "/tmp/fb.cookies"
        self.login = login
        self.passwd = passwd
        self.url = url
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        self.login_fb()
        self.cj.save()
        self.content("conn")

    def login_fb(self):
        login_data = urllib.urlencode({
            'login' : self.login,
            'passwd' : self.passwd,
        })
        response = self.opener.open(self.url+"login.php", login_data)
        return ''.join(response.readlines())

    def content(self,argument):
	response = self.opener.open(self.url+"settings.php?page="+argument)
	for line in response:
		print line
