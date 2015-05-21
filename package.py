#used for reading package info
class packagereader:
    def __init__(self,version):
        self.__packages={}
        self.__files={}
        file=open(".//tomcat_history//tomcat"+version+"//tomcat_pack.txt","r")
        s=file.readline()
        while s!='':
            x=s[:-1].split('\t')
            self.__packages[x[0]]=x[2:]
            for i in range(int(x[1])):
                t=file.readline()
                a=t[:-1].split('\t')
                if a[1] not in self.__packages[x[0]]:
                    self.__packages[x[0]].append(a[1])
                    self.__files[a[1]]=a[2:]
            s=file.readline()
        file.close()
    def getpackagelist(self):
        return self.__packages.keys()
    def getpackagecontain(self,packagename):
        return self.__packages[packagename][3:]
    def getpackageinfo(self,packagename):
        return self.__packages[packagename][0:3]
    def getfileinfo(self,filename):
        return self.__files[filename]
if __name__=='__main__':
    a=packagereader('6.0.43')
    l=a.getpackagelist()
    file=open("list.txt","w")
    for i in l:

        file.write(i)
        for x in a.getpackageinfo(i):
            file.write("\t%s"%(x))
        file.write("\n")

        for t in a.getpackagecontain(i):
            file.write(t)
            for x in a.getfileinfo(t):
                file.write("\t%s"%(x))
            file.write("\n")
    file.close()
