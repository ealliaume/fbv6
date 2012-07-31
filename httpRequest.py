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
	 'octets':1,
	 'Paquet':1,
	 'Paquets':1,
	 'paquet':1,
	 'paquets':1,
	 'dB':1,
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
    	self.list_switch("net_ethsw_stats")
    	self.list_nas("nas")

    def login_fb(self):
        login_data = urllib.urlencode({
            'login' : self.login,
            'passwd' : self.passwd,
        })
        response = self.opener.open(self.url+"login.php", login_data)
        return ''.join(response.readlines())	

    
    def list_switch(self,end_url):
	response = repr(self.opener.open(self.url+"settings.php?page="+end_url).read())
	net_ethsw_stats_regexp='(port_[1-4]_counters).+?(instantan.+?)[ :]+(.+?)[ ](.+?)/s+.+?(instantan.+?)[ :]+(.+?)[ ](.+?)/s+'
	net_ethsw_stats= re.findall(net_ethsw_stats_regexp,response)
	for j in [0,1,2,3]:
		print net_ethsw_stats[j][0]+"_in "+self.calcNetwork(net_ethsw_stats[j][2],net_ethsw_stats[j][3])
		print net_ethsw_stats[j][0]+"_in "+self.calcNetwork(net_ethsw_stats[j][5],net_ethsw_stats[j][6])

    def list_nas(self,end_url):
	response = repr(self.opener.open(self.url+"settings.php?page="+end_url).read())
	nas_regexp='(Espace.+?)[: ]+(.+?)[ ]([A-Za-z]+)<br/>.+?'
	nas= re.findall(nas_regexp,response)
	for j in [0,1]:
		print nas[j][0]+" "+self.calcNetwork(nas[j][1],nas[j][2])

    def list_value(self,end_url):
	response = self.opener.open(self.url+"settings.php?page="+end_url)
	port=0
    	for line in response:
                urls = re.findall(r'id=[\'"]?([^\'" >]+).*?>(.*?)<', line)
		if urls is not None and urls != []:
			name=urls[0][0]
			value=urls[0][1]
			flow = re.findall(r'([0-9]+)[ ]([A-Za-z]+)[\/][s][ (]+max[ ]([0-9,]+)[ ]([A-Za-z]+)', value)
			flow2 = re.findall(r'([0-9,]+)[ ]([A-Za-z]+)', value)
			if flow != []:
				print name+" "+self.calcNetwork(flow[0][0],flow[0][1])
				print name+"_full "+self.calcNetwork(flow[0][2],flow[0][3])
			elif flow2 != []:
				value=self.calcNetwork(flow2[0][0],flow2[0][1])
				print name+" "+value
			elif value != "":
				print name+" "+value

    def calcNetwork(self,flow,unity):
	flow = float(flow.replace(",","."))
	return str(int(round(flow*dic[unity])))
