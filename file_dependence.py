import understand
import matplotlib.pyplot as plt
import networkx as nx

project="tomcat"
udb = understand.open(project+".udb")
file=open(project+".txt","w+")
filedep=open(project+"_depends.txt","w+")
edges=[]
nodes=[]
for ent in sorted(udb.ents("file"),key=lambda ent: ent.name()):
    #x=ent.metric(['CountLine','CountLineBlank'])
    #file.write("%s\t%s\t%s\n"%(ent.name(),x['CountLine'],x['CountLineBlank']))
    #for t in ent.depends().keys():
    nodes.append(ent.name())
    file.write("%s\n"%(ent.name()))
    for t in ent.depends().keys():
        filedep.write("%s\t%s\n"%(ent.name(),t.name()))
        edges.append([ent.name(),t.name()])
file.close()
filedep.close()
G=nx.Graph()
for x in edges:
    G.add_edge(x[0],x[1])
for x in nodes:
    G.add_node(x)
pos=nx.shell_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
#nx.draw_networkx_labels(G,pos,font_size=15,fonfamily='sans-serif')
plt.axis('off')
plt.savefig(project+".png")
plt.show()
