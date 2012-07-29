from fbv6 import fb
from optparse import OptionParser

def main():
        # http://docs.python.org/library/optparse.html
        utilisation = "utilisation : python  *.py -p password"
        parser = OptionParser(utilisation)
        parser.add_option("-p", dest="password",help="password")
        (options, args) = parser.parse_args()
        fb_password = options.password
	fb("freebox", fb_password, "http://mafreebox.freebox.fr/")

if __name__ == "__main__":
        main()		
