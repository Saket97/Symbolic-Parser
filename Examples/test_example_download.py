import urllib
for i in range(2,50):
	print "Downloading test%d.tig..."%(i)
	u = urllib.urlopen("http://www.computing.dcu.ie/~hamilton/teaching/CA448/testcases/test%d.tig"%i)
	f = open("/home/saket/Desktop/game_src/Examples/test%d.tig"%i,'w')
	data = u.read()
	for l in data:
		f.write(l)
	f.close()