import understand

projects=["tomcat6.0.0","tomcat6.0.43","tomcat7.0.0","tomcat7.0.61","tomcat8.0.0","tomcat8.0.21"]
for project in projects:
    db=understand.open("..//"+project+".udb")
    package={}
    edges=[]
    file=open(".//tomcat_history//"+project+"//tomcat_pack.txt","w");
    p=sorted(db.ents("package"),key=lambda ent: ent.name())
    for ent in p:
        l=ent.refs("contain");
        m=ent.metric(['CountDeclClass','CountDeclFile','CountLineCode'])       
        file.write("%s\t%d\t%s\t%s\t%s\n"%(ent.name(),len(l),m['CountDeclFile'],m['CountDeclClass'],m['CountLineCode']))
        for t in l:
                package[t.file().name()]=ent
                x=t.file().metric(['CountLineCode','CountDeclClass','CountDeclMethod','CountDeclClassMethod'])
                file.write("\t%s\t%s\t%s\t%s\t%s\n"%(t.file().name(),x['CountLineCode'],x['CountDeclClass'],x['CountDeclMethod'],x['CountDeclClassMethod']))
    file.close()
    #for ent in p:
    #   for t in ent.refs("contin"):
    #        for x in t.file().depends().keys():
    #            if x.name() in package:
    #                if[ent,package[x.name()]] not in edges:
    #                    edges.append([ent,package[x.name()]])
    #file=open(project+"_pack_depends.txt","w+")
    #for x,y in edges:
    #    file.write("%s   %s\n"%(x,y))
    #file.close()
    db.close()
