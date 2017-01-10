import urllib
testfile = urllib.URLopener()
for i in range(13,27):
	testfile.retrieve("http://web.cse.iitk.ac.in/users/piyush/tmp/slides_lec%d.pdf"%(i), "/media/saket/4630856330855AB7/ML/CS772/lect%d.pdf"%i)
