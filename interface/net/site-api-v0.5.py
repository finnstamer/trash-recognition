mydata=[('one','1'),('two','2')]    #The first is the var name the second is the value
mydata=urllib.(mydata)
path='http://preclassical-princi.000webhostapp.com/api'    #the url you want to POST to
req=urllib.Request(path, mydata)
req.add_header("Content-type", "application/x-www-form-urlencoded")
page=urllib.urlopen(req).read()
print(page)