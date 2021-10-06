import sqlite3
import DSGRN
import math
import re
import json
import time
from operator import itemgetter
import networkx as nx
import sys
import functools

def NetworkSpecFile(network):
    spec = ''
    for i in range(0,3):
        spec += 'X' + str(i) + ' : '
        activators = '+'.join([ 'X' + str(j) for j in range(0,3) if network[i][j] == 1])
        repressors = ')('.join([ '~X' + str(j) for j in range(0,3) if network[i][j] == -1])
        if activators:
            activators = '(' + activators + ')'
        if repressors:
            repressors = '(' + repressors + ')'
        #spec += activators + repressors +  "\n"
        spec += activators + repressors + ( " : E\n" if i > 0 else "\n")
    return spec

def find_neighbor_nodes(node, CX1neighbors, CX2neighbors):
    l1=CX1neighbors[node[0]]
    l2=CX2neighbors[node[1]]
    neighbors=[]
    for i in l2:
        neighbors.append((node[0], i))
    for i in l1:
        neighbors.append((i,node[1]))
        #print(neighbors)
    return neighbors


#with open ('list.txt', 'r') as f:
#    for line in f:
#        numlist=line.split()
#        if int(numlist[0])==(int(sys.argv[1])):
#            networknum=numlist[1]

networknum="100121021"    
fname='{}.txt'.format(networknum)

with open(fname, 'w') as f3:

    totalbistablenodes=0
    network=((int(networknum[0])-1,int(networknum[1])-1, int(networknum[2])-1),(int(networknum[3])-1, int(networknum[4])-1, int(networknum[5])-1),(int(networknum[6])-1,int(networknum[7])-1, int(networknum[8])-1))
    networkSpec=NetworkSpecFile(network)
    
    Network=DSGRN.Network(networkSpec)
    print(networkSpec)
    pgraph=DSGRN.ParameterGraph(Network)
    print(pgraph.size())
    
    #compute paramater graph size and coefficients of labeling function

    FPindexShift=11

    for pindex in range(pgraph.size()):
        parameter=pgraph.parameter(pindex)
        domaingraph=DSGRN.DomainGraph(parameter)
        morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
        morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
        output=morsegraph.stringify()
        #print(output)
        fps=[m.start() for m in re.finditer('FP',output)]
        fpsShifted=[m+FPindexShift for m in fps]
        levels=[output[m] for m in fpsShifted]
        levels2=list(dict.fromkeys(levels))
        #print(levels)
        # should change this to count bistable in third coordinate
        count=len(levels2)
        count1=output.count("FP")
        if count==2 and count1==2:
            #nodedict[(q,p)]= 'green'
            totalbistablenodes+=1
        elif count==2:
            #nodedict[(q,p)]= 'green'
            totalbistablenodes+=1
    print(totalbistablenodes)
 
    f3.write(networknum+" "+str(totalbistablenodes/pgraph.size()))
f3.close()


