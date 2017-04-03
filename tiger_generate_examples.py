import pickle
import subprocess
output = []
output_file = open("tigerExamplesList1.pkl", "wb")
n_error = 0
for j in range(400):
    print "generating example: ",j
    try:
        tmp = subprocess.check_output("python2 tiger_string_generator.py", shell=True)
    except:
        n_error += 1
        print "Error"
        continue
    index = tmp.rindex("output")
    index += 8
    tmp = tmp[index+1:len(tmp)-2]
    tmp = tmp.split(",")
    t = ''
    for i in tmp:
        t += i
    t = subprocess.check_output("echo %s | sed \"s/'//g\" "%t, shell=True)
    output.append(t.strip())

pickle.dump(output, output_file)
output_file.close()
print "nerror: ",n_error
