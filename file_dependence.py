import understand
#import matplotlib.pyplot as plt
#import networkx as nx
projects=['6.0.0','6.0.43','7.0.0','7.0.61','8.0.0','8.0.21']
for project in projects:
    udb = understand.open("tomcat"+project+".udb")
    file=open(project+"1.txt","w+")
    filedep=open(project+"_depends.txt","w+")
    edges=[]
    nodes=[]
    for ent in sorted(udb.ents("file"),key=lambda ent: ent.name()):
        x=ent.metric(['CountLine','CountDeclClass','CountDeclMethod','CountDeclClassMethod'])
    
        nodes.append(ent.name())
        file.write("%s\t%s\t%s\t%s\t%s\n"%(ent.name(),x['CountLine'],x['CountDeclClass'],x['CountDeclMethod'],x['CountDeclClassMethod']))
        for t in ent.depends().keys():
            filedep.write("%s\t%s\n"%(ent.name(),t.name()))
            edges.append([ent.name(),t.name()])
    file.close()
    filedep.close()



#G=nx.Graph()
#for x in edges:
#    G.add_edge(x[0],x[1])
#for x in nodes:
#    G.add_node(x)
#pos=nx.spring_layout(G)
#nx.draw_networkx_nodes(G,pos)
#nx.draw_networkx_edges(G,pos)
#nx.draw_networkx_labels(G,pos,font_size=15,fonfamily='sans-serif')
#plt.axis('off')
#plt.savefig(project+".png")
#plt.show()
