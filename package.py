#used for reading package info
class packagereader:
    def _init_(self,ver):
        self.packages={}
        self.files={}
        file=open("tomcathistory//tomcat"+ver+"//tomcat_pack.txt","r")
        s=file.readline()
        while not s==EOF:
            x=s.split(' ')
            self.packages[x[0]]=[]
            for i in range(int(x[1])):
                t=file.readline()
                a=t.split(' ')
                self.packages[x[0]].append(a[0])
                self.files[a[0]]=a[1:]
            s=file.readline()
    def getpackage(self,packagename):
        return self.packages[packagename]
    def getfileinfo(self,filename):
        return self.files[filename]
