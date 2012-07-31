#! /usr/bin/env python
# -*- coding: iso-8859-1 -*- 
import cookielib, os, urllib, urllib2, re

dic = {'Kio':1024,
	 'Mio':1048576,
	 'Gio':1073741824,
	 'Tio':1099511627776,
	 'Pio':1125899906842624,
	 'Eio':1152921504606846976,
	 'Zio':1180591620717411303424,
	 'Yio':1208925819614629174706176,
	 'kbit':1024,
	 'mbit':1048576,
	 'gbit':1073741824,
	 'tbit':1099511627776,
	 'pbit':1125899906842624,
	 'ebit':1152921504606846976,
	 'zbit':1180591620717411303424,
	 'ybit':1208925819614629174706176,
	 'octets':0,
	 'Paquet':0,
	 'Paquets':0,
	 'paquet':0,
	 'paquets':0,
	 'dB':0,
	 'Ko':1000,
	 'ko':1000,
	 'Mo':1000000,
	 'Go':1000000000,
	 'To':1000000000000,
	 'Po':1000000000000000}

class httpRequest(object):
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
    	self.list_value("conn_status")
    	self.list_value("net_ethsw_stats")

    def login_fb(self):
        login_data = urllib.urlencode({
            'login' : self.login,
            'passwd' : self.passwd,
        })
        response = self.opener.open(self.url+"login.php", login_data)
        return ''.join(response.readlines())	

    def list_value(self,end_url):
	response = self.opener.open(self.url+"settings.php?page="+end_url)
    	for line in response:
		urls = re.findall(r'id=[\'"]?([^\'" >]+).*?>(.*?)<', line)
		if urls is not None and urls != []:
			#print urls
			name=urls[0][0]
			value=urls[0][1]
			flow = re.findall(r'([1-9]+)[ ]([A-Za-z]+)[\/][s][ (]+max[ ]([1-9,]+)[ ]([A-Za-z]+)', value)
			flow2 = re.findall(r'([1-9,]+)[ ]([A-Za-z]+)', value)
			if flow != []:
				n=0
				for i in flow[0]:
					if n==0:
						flow=i
						n=1
					elif n==1:
						value=self.calcNetwork(flow,i)
						n=0
						print name+" "+value
			elif flow2 != []:
				value=self.calcNetwork(flow2[0][0],flow2[0][1])
				print name+" "+value
			elif value != "":
				print name+" "+value

    def calcNetwork(self,flow,unity):
	flow = float(flow.replace(",","."))
	return str(int(round(flow*dic[unity])))
