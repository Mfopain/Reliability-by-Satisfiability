# It's a class that creates a directed graph
"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go
import networkx as nx
import  matplotlib.pyplot  as  plt

from pyFaulT2RePol.LogicGate import *

"""
Fault tree construction
"""

FaultTrees={}
class FaultTree:
    """
    A class to graphically illustrate the potential causes of a failure in the form of a diagram
    Attributes:
        
        id: integer,
          identification number
        NNode: integer,
        Node: list,
        Label: list,
        AdjMat: a list of lists,
        RelMat: a list of lists,
        IdxTable: a list of lists,
    
        """
    NFaultTree=0       
    def __init__(self,n):
        """
        Summary of FaultTree
        :param n: DESCRIPTION
        :type n: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self.id=id(self)
        FaultTrees[str(self.id)]=self
        self.__class__.NFaultTree+=1
        self.NNode=n # Le système a moins de composant que n
        self.Node=[]
        self.Label=[]
        self.AdjMat={}#matlib.zeros((n, n))
        self.RelMat=[[],[],[],[],[],[]] 
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        self.IdxTable=[[],[],[]] 
        #[[NumRel],[Node i],[Node j]]
    
    def __del__(self):
        """
        Deletes class
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self.__class__.NFaultTree-=1
    
    def IdxNode(self,Indices=None):
        """
        Summary IdxNode
        :param Indices: DESCRIPTION, defaults to None
        :type Indices: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE
       
        Args:
            Indices (list, optional): _description_. Defaults to None.

        Returns:
           list: A function that returns the index of the node in the list of nodes.
        """
        res=None
     
        if (Indices in self.Node):
            res=0
            while (self.Node[res]!=Indices):
                res=res+1
        return res

    def Root(self):
        """
        AI is creating summary for Root
        :return: DESCRIPTION
        :rtype: TYPE
        
        
        """
        res=[]
        for i in self.AdjMat.keys():
            if (sum(self.AdjMat[i])<=self.AdjMat[i][i]):
                res.append(i)
        return res
    
    def Leaves(self):
        """
        Summary
        :return: DESCRIPTION
        :rtype: TYPE

                """
        res=[]
     # Checking if the node is a leaf node.
        for j in range(len(self.AdjMat)):
            Temp=0
            # Iterating over the keys of the dictionary `self.AdjMat`.
            for i in range(len(self.AdjMat)):
               # Checking if the node is a leaf node.
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(j)
        return res
    
    def Update(self):
        """
        Updates the class
        :return: DESCRIPTION
        :rtype: TYPE

        """
        n=len(self.RelMat[0])
        if (n>0):
            Test=(len(self.Node)<=self.NNode-2)
            Test=Test or ((self.RelMat[1][-1] in self.Node) and (self.RelMat[2][-1] in self.Node))
            Test=Test or ((not(self.RelMat[1][-1] in self.Node) or not(self.RelMat[2][-1] in self.Node)) and (len(self.Node)<=self.NNode-1))
            if not(Test):
                del(self.RelMat[0][-1])
                del(self.RelMat[1][-1])
                del(self.RelMat[2][-1])
                del(self.RelMat[3][-1])
                del(self.RelMat[4][-1])
                del(self.RelMat[5][-1])
            else:
                if not(self.RelMat[1][-1] in self.Node):
                    self.Node.append(self.RelMat[1][-1])
                    self.Label.append(ID_P(1))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if not(self.RelMat[2][-1] in self.Node):
                    self.Node.append(self.RelMat[2][-1])
                    self.Label.append(ID_P(self.RelMat[0][-1]))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if (self.RelMat[0][-1]>=0):
                    self.IdxTable[0].append(n-1)
                    self.IdxTable[1].append(self.IdxNode(self.RelMat[1][-1]))
                    self.IdxTable[2].append(self.IdxNode(self.RelMat[2][-1]))
                    self.AdjMat[self.IdxTable[1][-1]][self.IdxTable[2][-1]]=1
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):
        """
        summary for InOrder2
        :param xx: DESCRIPTION, defaults to [1,3,2]
        :type xx: TYPE, optional
        :param yy: DESCRIPTION, defaults to [1,2,30]
        :type yy: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE
        
        Args:
            xx (list, optional): list of items to be sorted. Defaults to [1,3,2].
            yy (list, optional): list of items to be sorted. Defaults to [1,2,30].

        Returns:
            booleen: True if the elements of the list xx are less than or equal to the elements of the list yy.
            xx[i]<=yy[i]
        """
        res=True
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))):
            res=(res and (xx[i]<=yy[i]))
            i=i+1
        return res
   
    def Sort(self):     
        Temp1=[]
        Temp2=[]
        for i in range(len(self.IdxTable[0])):
            j=0
            for k in range(len(self.IdxTable[0])):           
                #if (self.InOrder2(self.RelMat[2][k],self.RelMat[1][i]) and (self.IdxTable[2][k]!=self.IdxTable[1][i])):
                Test=(self.AdjMat[self.IdxNode(self.RelMat[2][k])][self.IdxNode(self.RelMat[1][i])]==1)
                Test=Test or (self.InOrder2(self.RelMat[2][k],self.RelMat[1][i]))
                Test=Test and (self.IdxTable[2][k]!=self.IdxTable[1][i])
                if Test:
                    j=j+1
            while (j in Temp1):
                j=j+1
            Temp1.append(j)
            Temp2.append(0)
        for i in range(len(self.IdxTable[0])):
            Temp2[int(Temp1[i])]=i
        Temp3=[[],[],[]]
        Temp4=[[],[],[],[],[],[]]
        for i in range(len(self.IdxTable[0])):
            Temp3[0].append(i)
            Temp3[1].append(self.IdxTable[1][int(Temp2[i])])
            Temp3[2].append(self.IdxTable[2][int(Temp2[i])])
            Temp4[0].append(self.RelMat[0][int(Temp2[i])])
            Temp4[1].append(self.RelMat[1][int(Temp2[i])])
            Temp4[2].append(self.RelMat[2][int(Temp2[i])])
            Temp4[3].append(self.RelMat[3][int(Temp2[i])])
            Temp4[4].append(self.RelMat[4][int(Temp2[i])])
            Temp4[5].append(self.RelMat[5][int(Temp2[i])])
        self.IdxTable=Temp3.copy()
        self.RelMat=Temp4.copy()
        
    def NewRelation(self,Port=1,IndicesIn=None,IndicesOut=None,Orders=None,Times=None,IndicesPrincipal=None):
        """
        summary NewRelation
        
        :param Port: DESCRIPTION, defaults to 1
        :type Port: TYPE, optional
        :param IndicesIn: DESCRIPTION, defaults to None
        :type IndicesIn: TYPE, optional
        :param IndicesOut: DESCRIPTION, defaults to None
        :type IndicesOut: TYPE, optional
        :param Orders: DESCRIPTION, defaults to None
        :type Orders: TYPE, optional
        :param Times: DESCRIPTION, defaults to None
        :type Times: TYPE, optional
        :param IndicesPrincipal: DESCRIPTION, defaults to None
        :type IndicesPrincipal: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE
    
        Args:
            Port (int, optional): _description_. Defaults to 1.
            IndicesIn (list, optional): _description_. Defaults to None.
            IndicesOut (list, optional): _description_. Defaults to None.
            Orders (list, optional): _description_. Defaults to None.
            Times (list, optional): _description_. Defaults to None.
            IndicesPrincipal (list, optional): _description_. Defaults to None.
        """
        if (IndicesIn!=None) and (IndicesOut!=None):
            if True:#(len(IndicesIn)==self.NNode) and (len(IndicesOut)==self.NNode):
                self.RelMat[0].append(Port)
                self.RelMat[1].append(IndicesIn)
                self.RelMat[2].append(IndicesOut)
                self.RelMat[3].append(Orders)
                self.RelMat[4].append(Times)
                self.RelMat[5].append(IndicesPrincipal)
                self.Update()
                self.Sort()
        #print(self.RelMat)
    
    def ViewGraph(self,Dir=None):
        """
        Visualize the FaultTree sketch
        
        :param Dir: DESCRIPTION, defaults to None
        :type Dir: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        G=nx.DiGraph()
        GNode={}
        nn=len(self.Node)
        for i in self.AdjMat.keys():
            for j in range(len(self.AdjMat[i])):
                if (self.AdjMat[i][j]==1):
                    GNode[nn-1-self.IdxNode(self.Node[i])]=str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i]
                    GNode[nn-1-self.IdxNode(self.Node[j])]=str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j]
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
                    #G.add_edge(str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i],str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j])
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))
        #CompleteNode=self.Node.copy()
        
        mm=nn
        for i in range(nn):
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn):
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
            for j in range(self.NNode):
                Temp=[0 for k in range(self.NNode)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]):
                    #print(Temp)
                    if not(Temp in self.Node):
                        GNode[mm]=str(mm)+':'+ID_P(1)
                        G.add_edge(GNode[mm],GNode[nn-1-self.IdxNode(self.Node[i])])
                        mm+=1
                        #G.add_edge(str(self.Node[i]),str(Temp))
                    #CompleteNode.append(Temp)
        
        #print(G.adj)
        #fig=plt.figure(figsize=(5,5))
        plt.subplots(figsize=(10, 10))
        plt.clf() # Efface le contenu de la figure courante
        nx.draw_networkx(G,pos=nx.circular_layout(G),node_size=(10**4)/2)
        #nx.draw(G)
        #nx.draw(G,pos=nx.circular_layout(G),node_color='r',edge_color='b')
        plt.axis('off')
        #plt.grid(False)
        if (Dir!=None):
            plt.savefig(Dir+"AD.png")
            plt.savefig(Dir+"AD.pdf",format="pdf")
        plt.show()
        
"""
Dir="E:/Pedagogie/Encadrement/EncadrementEnsai/MasterRThese/20192020/TadieBenjaulys/"
MyTree=FaultTree(2)
#MyTree.NewRelation(1,[1,0],[1,0])
#MyTree.NewRelation(1,[0,1],[0,1])
MyTree.NewRelation(4,[0,1],[1,1])
MyTree.NewRelation(3,[1,1],[1,1])

print(MyTree.NNode)
print(MyTree.Leaves())
print(MyTree.Node)
print(MyTree.IdxTable)
print(MyTree.RelMat)
print(MyTree.AdjMat)
print(MyTree.Root())
MyTree.ViewGraph(Dir)
"""