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
        self.conn_status()

    def login_fb(self):
        login_data = urllib.urlencode({
            'login' : self.login,
            'passwd' : self.passwd,
        })
        response = self.opener.open(self.url+"login.php", login_data)
        return ''.join(response.readlines())	

    def conn_status(self):
    	self.list_value(["<span"],"conn_status"," ","")

    def list_value(self,search_list,end_url,split,port):
	end=""
	voie=""
	response = self.opener.open(self.url+"settings.php?page="+end_url)
    	for line in response:
    	    for search in search_list:
    			if search in line:
				print line
    				item = self.replaceFb(line).split(split)
				print len(item)
	    			if len(item) == 1 and item[0]!='':
	    				end=end+self.calcNetwork(item[0])+" "
	    			elif len(item) == 2:
	    				end=end+item[0]+":"+self.calcNetwork(item[1])+" "
	    			elif len(item) == 3:
					value=self.calcNetwork(item[2])
					if "." not in value:
						end=end+item[1]+":"+value+" "
	    			elif len(item) == 4:
					name=item[1]
					value=self.calcNetwork(item[2])
					value2=self.calcNetwork(item[3])
					if self.isInt(value) is True:
	    					end=end+item[1]+":"+self.calcNetwork(item[2])+" "
	    					end=end+item[1]+"_2:"+self.calcNetwork(item[3])+" "			
	if end[-1:]==" ":
		final=""
		number=0
		number2=0
		for i in end:
			number=number+1
		for i in end:
			if number2==number-1:
				print final
			else:
				number2=number2+1
				final=final+i
	else:
		print end

    def isInt(self,num):
    		try: 
        		int(num)
        		return True
    		except ValueError:
        		return False

    def replaceFb(self,chain):
		item = chain.replace(' ','')
		item = item.replace('<li>','')
		item = item.replace(':<spanid=\"conn',' ')
		item = item.replace('\"val=\"',' ')
		item = item.replace('</span>','')
		item = item.replace('</li>','')
		item = item.replace('\">',' ')
		item = item.replace('/s','')
		item = item.replace('(','')
		item = item.replace(')','')
		item = item.replace('\n','')
		item = item.replace('\t','')
		item = item.replace('_','')
		item = item.replace('<th>','')
		item = item.replace('</th>','')
		item = item.replace('<td>','')
		item = item.replace('</td>','')
		item = item.replace('max',' ')
		item = item.replace('<br/>','')
		item = item.replace('<divid=\"','')
		item = item.replace('/','')
		item = item.replace('<span>','')
		item = item.replace('<h2>','')
		item = item.replace('Freebox','')
		item = item.replace('é','e')
		item = item.replace('Ã©','e')
		item = item.replace('Ã','e')
		return str(item)

    def calcNetwork(self,chain):
		unity=re.sub("\d", "", chain).replace(",","")
		if unity in dic.keys():
			value=float(chain.replace(unity,'').replace(",","."))*dic[unity]
			end=int(round(value)) 
		else:
			end=chain 	
		return str(end)
