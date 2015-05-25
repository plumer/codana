import understand
#import matplotlib.pyplot as plt
#import networkx as nx
projects=['6.0.0','6.0.43','7.0.0','7.0.61','8.0.0','8.0.21']
for project in projects:
    udb = understand.open("../tomcat"+project+".udb")
    file=open("tomcat_history//tomcat"+project+"//tomcat.txt","w")
    filedep=open("tomcat_history//tomcat"+project+"//tomcat_depends.txt","w")
    edges=[]
    nodes=[]
    for ent in sorted(udb.ents("file"),key=lambda ent: ent.name()):
        x=ent.metric(['CountLine','AvgCyclomatic'])
    
        nodes.append(ent.name())
        file.write("%s\t%s\t%s\n"%(ent.name(),x['CountLine'],x['AvgCyclomatic']))
        for t in ent.depends().keys():
            filedep.write("%s\t%s\n"%(ent.name(),t.name()))
            edges.append([ent.name(),t.name()])
    file.close()
    filedep.close()
