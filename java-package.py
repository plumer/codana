import understand

projects=["tomcat6.0.0","tomcat6.0.43","tomcat7.0.0","tomcat7.0.61","tomcat8.0.0","tomcat8.0.21"]
for project in projects:
    db=understand.open(project+".udb")
    package={}
    edges=[]
    file=open(project+"_pack.txt","w+");
    for ent in db.ents("package"):
        l=ent.refs("contain");
        file.write("%s  %d\n"%(ent.name(),len(l)))
        for t in l:
            package[t.file().name()]=ent
            x=t.file().metric(['CountLine'])
            file.write("\t%s\t%s\n"%(t.file().name(),x['CountLine']))
    for ent in db.ents("java package"):
        for t in ent.refs("contain"):
            for x in t.file().depends().keys():
                if x.name() in package:
                    if[ent,package[x.name()]] not in edges:
                        edges.append([ent,package[x.name()]])
    file=open(project+"_pack_depends.txt","w+")
    for x,y in edges:
        file.write("%s   %s\n"%(x,y))
    file.close()
    db.close()
