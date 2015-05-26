import subprocess
import re
bugnum={}
filein=open("8.0.22","r")
a=filein.read()
filein.close()
file=open("log.txt","w")
#command="svn log -r {2014-5-23}:{2014-11-22} -v"
#args=command.split()
#p=subprocess.Popen(args,cwd="f:/srtp/tomcat/tomcat",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#stdout,stderr=p.communicate()
#output=stdout.decode('gbk').split('------------------------------------------------------------------------')
output=a.split('------------------------------------------------------------------------')
for r in output:
    m=re.search("Fix.*https://(bz|issues).apache.org/bugzilla/show_bug.cgi\?id=\d+",r)
    if m:
        line=r.split("\n")
        for i in range(3,len(line)+1):
            if line[i]=='':
                break;
            if line[i].find('/'):
                filename=line[i].split('(')[0].split('/')
                if filename[-1] not in bugnum.keys():
                    bugnum[filename[-1]]=1
                else:
                    bugnum[filename[-1]]+=1
for i in bugnum.keys():
    file.write("%s\t%d\n"%(i,bugnum[i]))
file.close()
