import numpy as np

n=7
N=np.zeros((n,n),dtype=int)
N[0,2]=1  # 3->1
N[2,3]=1  # 4->3
N[1,5]=1  # 6->2
N[3,6]=1  # 7->4
N[4,6]=1  # 7->5

# Build linear system for XN=NX plus block constraint X[4:7,0:4]=0
idx={(i,j): i*n+j for i in range(n) for j in range(n)}
eqs=[]
for i in range(n):
    for j in range(n):
        row=np.zeros(n*n,dtype=int)
        for k in range(n):
            if N[k,j]==1: row[idx[(i,k)]] ^= 1   # (XN)_{ij}
            if N[i,k]==1: row[idx[(k,j)]] ^= 1   # (NX)_{ij}
        eqs.append(row)

for i in range(4,7):
    for j in range(0,4):
        row=np.zeros(n*n,dtype=int)
        row[idx[(i,j)]]=1
        eqs.append(row)

A=np.vstack(eqs)%2

# rank over F2
A=A.copy()
r=0
for c in range(A.shape[1]):
    piv=None
    for i in range(r,A.shape[0]):
        if A[i,c]==1: piv=i; break
    if piv is None: continue
    A[[r,piv]]=A[[piv,r]]
    for i in range(A.shape[0]):
        if i!=r and A[i,c]==1:
            A[i,:]^=A[r,:]
    r+=1

dim = A.shape[1]-r
print(dim, 2**dim)