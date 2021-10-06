import math
import time
import numpy as np
from numba import jit

# our matrix A will be 16 by 16
# 16 by 16 is too large. Switching to 2 by 16
# we need to figure out both the extension to continuous labels and apply to dimension reduction
#for the extension to continuous, instead of having classes, maybe we can give some weight to all 
# nodes. For example if we have x1 and x2 with scores s1 and s2, the weight could be e^{-(10*|s1-s2|)^4}
# might be necessary to do stochastic gradient descent

@jit(nopython=True)
def mmult(A, v):
    w=[]
    for i in range(2):
        sum=0
        for j in range(16):
            sum+=A[i,j]*v[j]
        w.append(sum)
    return w

@jit(nopython=True)
def vecDiff(v, w):
    u=np.zeros(16)
    for i in range(16):
        u[i]=v[i]-w[i]
    return u

@jit(nopython=True)
def NormSq(v):
    sum=0
    for i in range(2):
        sum+=v[i]**2
    return sum

@jit(nopython=True)
def HammDist(v1, v2):
    sum=0
    for i in range(len(v1)):
        if v1[i]!=v2[i]:
            sum+=1
    return sum


ls=np.zeros((123402,16))
ls2=np.zeros(123402)

with open('FullData.txt', 'r') as f:
    i=0
    for line in f:
        #if i ==40000:
        #    break
        s=line.split()
        for k in range(16):
            if s[0][k]=="R":
                ls[i, k]=-1
            elif s[0][k]=="A":
                ls[i,k]=1
            else:
                ls[i,k]=0
        si=float(s[1])
        ls2[i]=si
        i+=1

f.close()

gamma=1
Tol=0.01
UA=np.zeros((2,16))
A=np.ones((2,16))
A[1,2]=0
A[1,3]=0
A[1,9]=0
A[1,15]=0
A[0,1]=0
A[0,13]=0
A[0,9]=0
#A[2,4]=0
#A[2,6]=0
#A[2,14]=0


#this will control the starting guess

@jit(nopython=True)
def iterate(A):
    partialsMat=np.zeros((2,16))
    sum3=0
    #print(A)
    #first we should get and store the relevant entry
    for i in range(123402):
        #print(ls[i])
        xi=ls[i]
        f1=0
        f3=0
        f2=np.zeros((2,16))
        f4=np.zeros((2,16))
        for j in range(123402):
            #here we could try only counting the local points, everything within say 5 using the Hamming distance
            if j==i or HammDist(ls[j], xi)>5:
                continue
            #print(ls[j])
            xj=ls[j]
            e1=math.exp(-NormSq(mmult(A, vecDiff(xi,xj))))
            e2=math.exp(-(10*(ls2[i]-ls2[j]))**2)
            f1+=e1
            f3+=e2*e1
            
            #currently, there is nothing which would differentiate the alphas    
            for alpha in range(2):
                for beta in range(16):
                    innerSum=0
                    for k in range(16):
                        innerSum+=A[alpha,k]*(xi[k]-xj[k])
                    f2[alpha,beta]+=e1*e2*innerSum*(xi[beta]-xj[beta])*(-2)
                    f4[alpha,beta]+=(-2)*e1*innerSum*(xi[beta]-xj[beta])
        if f1==0:
            print ("Here is a problem")
            print(i)
            continue
        for alpha in range(2):
            for beta in range(16):
                partialsMat[alpha,beta]+=(f2[alpha,beta]/f1-(f3/f1)*(f4[alpha,beta]/f1))
        sum3+=f3/f1
    return (partialsMat, sum3)
    
    

#lets try to write one iteration
#we have converted the code 00A0R0RRA00A to a list of number [0,0,1, 1, -1, ..]
count=0
flag=0
Uscore=0
score=0
#start=time.time()
while (count<50 and flag==0):
    partialsMat, Uscore=iterate(A)
    print(Uscore)
    #print(partialsMat)
    #print(gamma)
    if Uscore<score:
        gamma=gamma/2
    score=Uscore
    for alpha in range(2):
        for beta in range(16):
            UA[alpha, beta]=A[alpha, beta]+gamma*partialsMat[alpha,beta]
    #this would be one iteration of gradient descent
    count+=1
    Adiff=0
    for i in range(2):
        for j in range(16):
            if abs(UA[i,j]-A[i,j])>Adiff:
                Adiff=abs(UA[i,j]-A[i,j])
    
    #print(Adiff)
    if Adiff<Tol:
        flag=1

    for i in range(2):
        for j in range(16):
            A[i,j]=UA[i,j]

#end=time.time()
#print(end-start)
#print(flag)
print(A)
with open('matrix.txt', 'w') as f:
    for i in range(2):
        for j in range(16):
            f.write(str(A[i,j])+" ")
        if i==0:
            f.write("\n")
f.close()