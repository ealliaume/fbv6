from httpRequest import httpRequest
from optparse import OptionParser
from freeboxParsing import freeboxParsing

def main():
        # http://docs.python.org/library/optparse.html
        utilisation = "utilisation : python  *.py -p password"
        parser = OptionParser(utilisation)
        parser.add_option("-p", dest="password",help="password")
        (options, args) = parser.parse_args()
        fb_password = options.password
	data = httpRequest("freebox", fb_password, "http://mafreebox.freebox.fr/")
	#print freeboxParsing(data)

if __name__ == "__main__":
        main()		
