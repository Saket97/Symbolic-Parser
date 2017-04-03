import subprocess
for i in range(1,50):
    subprocess.call("java tigerLexer Examples/test%d.tig test%d_lex.tig"%(i,i), shell=True)