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


##should write this to both determine if 4 corner criteria are satisfied, and for the good DF graphs should count percentage of bistable nodes.
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
        spec += activators + repressors + ( " : E\n" if i ==2 else "\n")
    return spec


#conn=sqlite3.connect("/scratch/ph325/PathProject2/fourCornerNodes/fourCorners.db")
conn=sqlite3.connect("fourCorners.db")
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS candidates(id integer PRIMARY KEY, network text , redp integer, type text)""")

#with open ('list.txt', 'r') as f:
#    for line in f:
#        numlist=line.split()
#        if int(numlist[0])==(int(sys.argv[1])+1):
#            networknum=numlist[1]


        
networknum='100120002'
fname='{}.txt'.format(networknum)

        
network=((int(networknum[0])-1,int(networknum[1])-1, int(networknum[2])-1),(int(networknum[3])-1, int(networknum[4])-1, int(networknum[5])-1),(int(networknum[6])-1,int(networknum[7])-1, int(networknum[8])-1))
networkSpec=NetworkSpecFile(network)
#print(networkSpec)
Network=DSGRN.Network(networkSpec)
pgraph=DSGRN.ParameterGraph(Network)
NetSplit=networkSpec.split("\n")
    
count = Network.size()
Tls = [math.factorial(len(Network.outputs(i))) for i in range(count)]
Xls = [len(pgraph.factorgraph(i)) for i in range(count)]
ls=Xls+Tls   
coeffs=[]

#compute paramater graph size and coefficients of labeling function
                    
for i in range(len(ls)):
    coeffs.append(functools.reduce(lambda x,y: x*y, ls[:i],1))
pgraphsize=functools.reduce(lambda x,y: x*y, ls)
#print(coeffs)
g1=pgraph.factorgraph(0)
g2=pgraph.factorgraph(1)
print(len(g1))
print(len(g2))

FPindexShift=11
redls=ls.copy()
del redls[1]
del redls[0]
redcoeffs=[]
for k in range(len(redls)):
    redcoeffs.append(functools.reduce(lambda x,y: x*y, redls[:k],1))
    
#print(redls)
numtotalnodes=0
numbistablenodes=0
numredparams=int(pgraphsize/(len(g1)*len(g2)))
print(numredparams)
goodredparams=0
#print(pgraphsize)
for k in range(numredparams):
    multiplierls=[]
    # now we need to compute the fixed values for the labeling function parameters
    remainder=k
    for l in range(len(redcoeffs)):
        multiplierls.insert(0, remainder//redcoeffs[-(l+1)])
        remainder=remainder%redcoeffs[-(l+1)]
    #here we add back in the nodes selected for the double factor graph
    multiplierls.insert(0,0)
    multiplierls.insert(1,0)
        

    multiplierls[0]=0
    multiplierls[1]=0
    #print(multiplierls)
    pindex=0
    for l in range(len(multiplierls)):
        pindex+=multiplierls[l]*coeffs[l] 
    #print(pindex)
    parameter=pgraph.parameter(pindex)
    domaingraph=DSGRN.DomainGraph(parameter)
    morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
    morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
    output=morsegraph.stringify()
    fps=[m.start() for m in re.finditer('FP',output)]
    fpsShifted=[m+FPindexShift for m in fps]
    levels=[output[m] for m in fpsShifted]
    levels2=list(dict.fromkeys(levels))
    #print(pindex, levels2 )
    if len(levels2)!=1:
        continue
    ff=levels2[0]
        
    multiplierls[0]=0
    multiplierls[1]=len(g2)-1
    #print(multiplierls)
    pindex=0
    for l in range(len(multiplierls)):
        pindex+=multiplierls[l]*coeffs[l] 
    #print(pindex)
    parameter=pgraph.parameter(pindex)
    domaingraph=DSGRN.DomainGraph(parameter)
    morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
    morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
    output=morsegraph.stringify()
    fps=[m.start() for m in re.finditer('FP',output)]
    fpsShifted=[m+FPindexShift for m in fps]
    levels=[output[m] for m in fpsShifted]
    levels2=list(dict.fromkeys(levels))
    #print(pindex, levels2 )
    if len(levels2)!=1:
        continue
    fl=levels2[0]
        
    multiplierls[0]=len(g1)-1
    multiplierls[1]=0
    #print(multiplierls)
    pindex=0
    for l in range(len(multiplierls)):
        pindex+=multiplierls[l]*coeffs[l]
    #print(pindex)
    parameter=pgraph.parameter(pindex)
    domaingraph=DSGRN.DomainGraph(parameter)
    morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
    morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
    output=morsegraph.stringify()
    fps=[m.start() for m in re.finditer('FP',output)]
    fpsShifted=[m+FPindexShift for m in fps]
    levels=[output[m] for m in fpsShifted]
    levels2=list(dict.fromkeys(levels))
    #print(pindex, levels2 )
    if len(levels2)!=1:
        continue
    lf=levels2[0]
        
    multiplierls[0]=len(g1)-1
    multiplierls[1]=len(g2)-1
    #print(multiplierls)
    pindex=0
    for l in range(len(multiplierls)):
        pindex+=multiplierls[l]*coeffs[l]
    #print(pindex)
    parameter=pgraph.parameter(pindex)
    domaingraph=DSGRN.DomainGraph(parameter)
    morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
    morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
    output=morsegraph.stringify()
    fps=[m.start() for m in re.finditer('FP',output)]
    fpsShifted=[m+FPindexShift for m in fps]
    levels=[output[m] for m in fpsShifted]
    levels2=list(dict.fromkeys(levels))
    #print(pindex, levels2 )
    if len(levels2)!=1:
        continue
    ll=levels2[0]
    
    

    if (ff==fl and fl==lf and ff !=ll):
        status="AND"      
    elif (ll==fl and fl==lf and ff !=ll):
        status="OR"
    else:
        continue
    #print(ff, lf, fl, ll)
    
    flag1=0
    flag2=0
    #now can look for bistable points criterion
    if status=='AND':
        #need to check paths against far walls
        #right side first
        multiplierls[0]=len(g1)-1
        for p in range(len(g2)):
            multiplierls[1]=p
            pindex=0
            for l in range(len(multiplierls)):
                pindex+=multiplierls[l]*coeffs[l] 
            parameter=pgraph.parameter(pindex)
            domaingraph=DSGRN.DomainGraph(parameter)
            morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
            morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
            output=morsegraph.stringify()
            fps=[m.start() for m in re.finditer('FP',output)]
            fpsShifted=[m+FPindexShift for m in fps]
            levels=[output[m] for m in fpsShifted]
            levels2=list(dict.fromkeys(levels))
            count=len(levels2)
            if count==2:
                flag1=1
                break

        multiplierls[1]=len(g2)-1
        for q in range(len(g1)):
            multiplierls[0]=q
            pindex=0
            for l in range(len(multiplierls)):
                pindex+=multiplierls[l]*coeffs[l] 
            parameter=pgraph.parameter(pindex)
            domaingraph=DSGRN.DomainGraph(parameter)
            morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
            morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
            output=morsegraph.stringify()
            fps=[m.start() for m in re.finditer('FP',output)]
            fpsShifted=[m+FPindexShift for m in fps]
            levels=[output[m] for m in fpsShifted]
            levels2=list(dict.fromkeys(levels))
            count=len(levels2)
            if count==2:
                flag2=1
                break
                
    if (flag1==0 or flag2==0) and status=='AND':
        continue

    if status=='OR':
        #need to check paths against far walls
        #left side first
        multiplierls[0]=0
        for p in range(len(g2)):
            multiplierls[1]=p
            pindex=0
            for l in range(len(multiplierls)):
                pindex+=multiplierls[l]*coeffs[l] 
            parameter=pgraph.parameter(pindex)
            domaingraph=DSGRN.DomainGraph(parameter)
            morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
            morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
            output=morsegraph.stringify()

            fps=[m.start() for m in re.finditer('FP',output)]
            fpsShifted=[m+FPindexShift for m in fps]
            levels=[output[m] for m in fpsShifted]
            levels2=list(dict.fromkeys(levels))
            count=len(levels2)
            if count==2:
                flag1=1
                break
        multiplierls[1]=0
        for q in range(len(g1)):
            multiplierls[0]=q
            pindex=0
            for l in range(len(multiplierls)):
                pindex+=multiplierls[l]*coeffs[l] 
            parameter=pgraph.parameter(pindex)
            domaingraph=DSGRN.DomainGraph(parameter)
            morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
            morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
            output=morsegraph.stringify()
            fps=[m.start() for m in re.finditer('FP',output)]
            fpsShifted=[m+FPindexShift for m in fps]
            levels=[output[m] for m in fpsShifted]
            levels2=list(dict.fromkeys(levels))
            count=len(levels2)
            if count==2:
                flag2=1
                break          
    if (flag1==0 or flag2==0) and status=='OR':
        continue
    goodredparams+=1
    
    #at this point, only good DF graphs should still be here, so we should count the percentage of bistable nodes. 
    #print(multiplierls)
    sql='''INSERT INTO candidates(network, redp ,type) VALUES (?,?,?)'''
    c.execute(sql, (networknum, k, status))
    for q in range(len(g1)): 
        multiplierls[0]=q    
        for p in range(len(g2)):
            multiplierls[1]=p
            pindex=0
            for l in range(len(multiplierls)):
                pindex+=multiplierls[l]*coeffs[l] 
            parameter=pgraph.parameter(pindex)
            domaingraph=DSGRN.DomainGraph(parameter)
            morsedecomposition=DSGRN.MorseDecomposition(domaingraph.digraph())
            morsegraph=DSGRN.MorseGraph(domaingraph, morsedecomposition)
            output=morsegraph.stringify()
            fps=[m.start() for m in re.finditer('FP',output)]
            fpsShifted=[m+FPindexShift for m in fps]
            levels=[output[m] for m in fpsShifted]
            levels2=list(dict.fromkeys(levels))
            count=len(levels2)
            count1=output.count("FP")
            numtotalnodes+=1
            if count==2:
                numbistablenodes+=1

print(networknum+" "+str(numbistablenodes)+" "+str(numtotalnodes)+" "+str(goodredparams)+" "+str(numredparams)+" "+str(pgraphsize))

with open(fname, 'w') as f3:
    f3.write(networknum+" "+str(numbistablenodes)+" "+str(numtotalnodes)+" "+str(goodredparams)+" "+str(numredparams)+" "+str(pgraphsize))

#conn.commit()