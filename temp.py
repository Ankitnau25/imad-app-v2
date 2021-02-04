import numpy
from FUNCTIONS.clique_problem import clique_problem


def clique(g,k):
#####################################
#                                   #
#  - Input: the adjacency matrix of #
#    a graph with vertices          #
#    {0, 1, ..., n} and a positive  #
#    integer k.                     #
#                                   #
#  - Output: A list of vertices     #
#    forming a clique of size k in  #
#    g if one exists, or []         #
#    otherwise.                     #
#                                   #
#  - Use the function               #
#    clique_problem(g, k) that      #
#    returns 1 if the graph g       #
#    has a clique of size k and 0,  #
#    otherwise.                     #
#                                   #
#  Example:                         #
#            g: [[0 1 1]            #
#                [1 0 1]            #
#                [1 1 0]]           #
#            k: 3                   #
#                                   #
#   clique_problem(g, k): 1         #
#   clique(g, k): [0, 1, 2]         #
#                                   #
#                                   #
#####################################
    # Write yur code here.
    if clique_problem(g,k)==0:
#     if False:  
        return []
    else:
        p=0 
        out=[]
        le=k
        while(p<len(g)):
            if p in out and sum(g[p])==k-1:
                p+=1
            else:
                for l in range(len(g[p])):
                    if g[p][l]==1:
                        li_i=[p,l]
                        i=l
                        for m in range(len(g[i])): 
                            if g[i][m]==1:
                                flag=True
                                for n in li_i:
                #                     print(m,n)
                                    if g[m][n]==0:
                                        flag=False
                                        break
                                if flag:    
                                    li_i.append(m)
                                    i=m           
                        if len(li_i)>=le:            
                            out=list(set(out+li_i))          
                p+=1 
        return out     
def main(input):
    return clique(input[0], input[1])
