import networkx as nx
from ReadFile import BipartiteGraph
import math
import random
import numpy as np

class biSBM:
    def __init__(self, bipartiteGraph):
        self.graph = bipartiteGraph
        self.top_nodes = set(n for n,d in self.graph.nodes(data=True) if d['bipartite']=='Customers')
        self.bottom_nodes = set(self.graph.nodes()) - self.top_nodes

    def createBiSBM(self):

        edges = self.graph.edges()
        edgeLength = len(edges)
        # customers = bipartiteGraph.sets(bipartiteGraph, bipartite='Customers')
        top_nodes = set(n for n,d in self.graph.nodes(data=True) if d['bipartite']=='Customers')
        bottom_nodes = set(self.graph.nodes()) - top_nodes
        prodGroup = ['technology','art','business','fiction','general','geography','health','history','language','movies','music','people','religion','sports','warfare','political']
        custGroup = ['technologyCust','artCust','businessCust','fictionCust','generalCust','geographyCust','healthCust','historyCust','languageCust','moviesCust','musicCust','peopleCust','religionCust','sportsCust','warfareCust','politicalCust']
        crossEdges = self.getCrossEdges(top_nodes, bottom_nodes, custGroup, prodGroup)
        custCount = self.countCustNodes(top_nodes, custGroup)
        prodCount = self.countProdNodes(bottom_nodes, prodGroup)

        prob = 0
        for c in custGroup:
            cust = custCount[c]
            for p in prodGroup:
                prod = prodCount[p]
                if crossEdges[(c,p)]:
                    mrs = crossEdges[(c,p)]
                    if mrs:
                        prob += mrs * math.log(mrs/(prod*cust),math.e)
        print('biSBM')
        return prob


    # m_rs
    def getCrossEdges(self, top_nodes, bottom_nodes, top_groups, bottom_groups):
        count = {}
        temp = 0
        graph = self.graph
        for custGrp in top_groups:
            for prodGrp in bottom_groups:
                temp = 0
                for cust in top_nodes:
                    for prod in bottom_nodes:
                        if (cust, prod) in graph.edges():
                            if custGrp in graph.node[cust]['CustCategory'] and prodGrp in graph.node[prod]['Category']:
                                temp += 1
                count[(custGrp,prodGrp)] = temp
        return count

    def countCustNodes(self, nodes, group):
        count = {}
        for g in group:
            temp = 0
            for node in nodes:
                if g in self.graph.node[node]['CustCategory']:
                    temp += len(self.graph.node[node])
            count[g] = temp
        return count

    def countProdNodes(self, nodes, group):
        count = {}
        for g in group:
            temp = 0
            for node in nodes:
                if g in self.graph.node[node]['Category']:
                    temp += len(self.graph.node[node])
            count[g] = temp
        return count

    def createAUC(self):
        alpha = [0.2,0.4,0.6,0.8,0.95]
        edgeLength = len(self.graph.edges())
        edges = list(self.graph.edges())
        for a in alpha:
            sampledLen = int(edgeLength/a)
            sampledEdges = list(np.random.choice(edges, sampledLen))
            graph = nx.Graph()
            graph.add_nodes_from(self.top_nodes, bipartite='Customers')
            graph.add_nodes_from(self.bottom_nodes, bipartite='Products')
            graph.add_edges_from(sampledEdges)

            for i in range(edgeLength - sampledLen):
                for c in self.top_nodes:
                    for p in self.bottom_nodes:
                        if (c,p) in sampledEdges:
                            continue
                        else:
                            graph.add_edge(c,p)
