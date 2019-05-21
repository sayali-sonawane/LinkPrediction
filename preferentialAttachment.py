import networkx as nx
import numpy as np
from biSBM import biSBM
from sklearn import metrics
from matplotlib import pyplot as plt
import random
from linkPred import linkPred
from networkx.algorithms import bipartite

class prefAttach:
    def __init__(self, bipartiteGraph):
        self.graph = bipartiteGraph
        self.top_nodes = set(n for n,d in self.graph.nodes(data=True) if d['bipartite']=='Customers')
        self.bottom_nodes = set(self.graph.nodes()) - self.top_nodes

    def predictAuc(self):
        # alpha = [0.2, 0.4, 0.6, 0.8, 0.95]
        alpha = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]
        edgeLength = len(self.graph.edges())
        edges = self.graph.edges()
        graph = nx.Graph()
        iterations = 1
        aucDict = {}
        allAUC = []
        for a in alpha:
            auc = []
            for iter in range(iterations):
                sampledLen = int(edgeLength * a)
                graph.add_nodes_from(self.top_nodes, bipartite='Customers')
                graph.add_nodes_from(self.bottom_nodes, bipartite='Products')
                for node in set(n for n,d in graph.nodes(data=True) if d['bipartite']=='Customers'):
                    graph.node[node]['CustCategory'] = self.graph.node[node]['CustCategory']
                for node in set(n for n,d in graph.nodes(data=True) if d['bipartite']=='Products'):
                    graph.node[node]['Category'] = self.graph.node[node]['Category']
                sampledIndex = list(np.random.choice(edgeLength, sampledLen))
                sampledEdges = []
                for i in sampledIndex:
                    sampledEdges.append(edges[i])
                graph.add_edges_from(sampledEdges)

                for i in range(edgeLength - sampledLen):
                    max = (-1)*np.inf
                    max_c = 0
                    max_p = 0
                    for c in self.top_nodes:
                        for p in self.bottom_nodes:
                            if (c, p) in sampledEdges:
                                continue
                            else:
                                graph.add_edge(c, p)
                                oneModeProjections = bipartite.weighted_projected_graph(graph, self.top_nodes, ratio=True)
                                prob = len(oneModeProjections[c])*len(graph[p])
                                if (prob > max):
                                    max = prob
                                    max_c,max_p = (c,p)
                                graph.remove_edge(c,p)
                    print(a)
                    graph.add_edge(max_c,max_p)
                aucScore = self.CalcAUCScore(graph)
                auc.append(aucScore)
                allAUC.append(auc)
                graph.clear()
            aucDict[a] = sum(auc)/len(auc)
            print(allAUC)
            print(a)
        print(allAUC)
        print("prf attach" + str(aucDict))
        return aucDict

    def CalcAUCScore(self, predGraph):
        bipartite = self.graph
        # predGraph = self.predictGraph()

        bipartBin = []
        predBin = []
        for c in self.top_nodes:
            for p in self.bottom_nodes:
                if (c,p) in bipartite.edges():
                    bipartBin.append(1)
                else:
                    bipartBin.append(0)
                if (c,p) in predGraph.edges():
                    predBin.append(1)
                else:
                    predBin.append(0)
        aucScore = metrics.roc_auc_score(bipartBin,predBin)
        return aucScore

    def printAUC(self):
        aucDict = self.predictAuc()

        x = []
        y = []
        for key, value in aucDict.items():
            x.append(key)
            y.append(value)

        plt.plot(x,y)
        plt.xlabel('Fraction of sampled edges')
        plt.ylabel('AUC')
        plt.title('AUC vs Fraction of sampled edges')
        plt.show()
