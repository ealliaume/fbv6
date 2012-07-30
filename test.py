#http://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link
s='<a href="http://www.ptop.se" target="_blank">http://www.ptop.se</a>'
import re
urls = re.findall(r'href=[\'"]?([^\'" >]+)', s)
print ', '.join(urls)

