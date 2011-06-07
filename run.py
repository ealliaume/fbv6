from fbv6 import fb
from optparse import OptionParser

def main():
        # http://docs.python.org/library/optparse.html
        utilisation = "utilisation : python  *.py -t template_name"
        parser = OptionParser(utilisation)
        parser.add_option("-t", dest="template",help="name of template")
        (options, args) = parser.parse_args()
        fb_template = options.template
        if  options.template is not None:
		fb("freebox", FREEBOX_PASSWORD, "http://mafreebox.freebox.fr/", fb_template)
        else:
		parser.print_help()

if __name__ == "__main__":
        main()		
