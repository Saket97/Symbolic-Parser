# import subprocess
input_file = open("check1.txt",'r+')
line = input_file.readline()
print line
tmp = input_file.tell()
input_file.write("My name is Saket")
# input_file.flush()
input_file.seek(tmp,0)
print input_file.readline()
x = "Computer Science and engineering"
input_file.write(x+3)
input_file.close()