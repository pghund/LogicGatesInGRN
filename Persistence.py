import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import cechmate as cm
from persim import plot_diagrams
from operator import itemgetter


value=0.30
# there is only an edge if the points are hamming distance one apart. Then we assign the edge a score. 
# so at most we need a matrix which is about 1000 by 32

#first let us make a list of all the points and their scores.

def HammDist(v1, v2):
    sum=0
    for i in range(len(v1)):
        if v1[i]!=v2[i]:
            sum+=1
    return sum

ls=[]
filtration=[]
with open ('FullDataReduced.txt', 'r') as f:
    i=0
    for line in f:
        #if i==1000:
        #    break
        s=line.split()
        v=[]
        for k in range(16):
                if s[0][k]=="R":
                    v.append(-1)
                elif s[0][k]=="A":
                    v.append(1)
                else:
                    v.append(0)
        ls.append([v, float(s[1])])
        score=0.55-float(s[1])
        filtration.append(([i], score))
        #if score==0:
        #    filtration.append(([i], 0))
        #elif score<=0.05:
        #    filtration.append(([i], 1))
        #elif score<=0.1:
        #    filtration.append(([i], 2))
        #elif score<=0.15:
        #    filtration.append(([i], 3))
        #elif score<=0.2:
        #    filtration.append(([i], 4))
        #elif score<=0.25:
        #    filtration.append(([i], 5))
        #elif score<=0.3:
        #    filtration.append(([i], 6))
        #elif score<=0.35:
        #    filtration.append(([i], 7))
        #elif score<=0.4:
        #    filtration.append(([i], 8))
        #elif score<=0.45:
        #    filtration.append(([i], 9))
        #elif score<=0.5:
        #    filtration.append(([i], 10))
        #elif score<=0.55:
        #    filtration.append(([i], 11))

        i+=1


#print(filtration[:340])
#print(ls[:100])
length=len(ls)
Mat=[]
for i in range(length):
    Mat.append([])
    for j in range(i+1, length):
        if HammDist(ls[i][0], ls[j][0])<3:
            Mat[i].append([j, min(ls[j][1], ls[i][1])])
            score=0.55-min(ls[j][1], ls[i][1])
            filtration.append(([i,j], score))
            #if score==0:
            #    filtration.append(([i, j], 0))
            #elif score<=0.05:
            #    filtration.append(([i, j], 1))
            #elif score<=0.1:
            #    filtration.append(([i,j], 2))
            #elif score<=0.15:
            #    filtration.append(([i,j], 3))
            #elif score<=0.2:
            #    filtration.append(([i,j], 4))
            #elif score<=0.25:
            #    filtration.append(([i,j], 5))
            #elif score<=0.3:
            #    filtration.append(([i,j], 6))
            #elif score<=0.35:
            #    filtration.append(([i,j], 7))
            #elif score<=0.4: 
            #    filtration.append(([i,j], 8))
            #elif score<=0.45: 
            #    filtration.append(([i,j], 9))
            #elif score<=0.5:
            #    filtration.append(([i,j], 10))
            #elif score<=0.55:
            #    filtration.append(([i,j], 11))

    #if len(Mat[i])<2:
    #    print(i)
    #    print(Mat[i])

print(len(filtration))
filtration.sort(key=itemgetter(1))
#print(filtration)
#this should give a matrix with edges labeled by lesser values.
# now we want to draw points and edges depending on whether the points and edges are there.
#so which nodes appear?
#print(Mat[:10])
NodeList=[]
for i in range(length):
    if ls[i][1]>value:
        NodeList.append(i)

#print(NodeList)
#now which edges appear?

EdgeList=[]
for entry in NodeList:
    for j in range(len(Mat[entry])):
        if Mat[entry][j][1]>value:
            EdgeList.append((entry, Mat[entry][j][0]))


#print(EdgeList)

#G=nx.Graph()
#G.add_nodes_from(NodeList)
#G.add_edges_from(EdgeList)
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.savefig('Homology.png')

dgms = cm.phat_diagrams(filtration, show_inf = True)
with open ('DeathMinusBirth.txt', 'w') as f:
    for i in range(len(dgms[0])):
        #if dgms[0][i][0]>8:
        #    continue
        if dgms[0][i][1]>11:
            f.write(str(dgms[0][i][0])+" "+str(12))
            f.write('\n')
        else: 
            f.write(str(dgms[0][i][0])+" "+str(float(dgms[0][i][1])-float(dgms[0][i][0])))
            f.write('\n')

f.close()
#with open ('Filtration.txt', 'w') as f:
#    for i in range(len(filtration)):
#        f.write(str(filtration[i]))
#        f.write('\n')



#print("H0:\n", dgms[0][0][0])
plot_diagrams(dgms[0])
plt.savefig('Diagram.png')

