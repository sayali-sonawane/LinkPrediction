import networkx as nx
from biSBM import biSBM
from ReadFile import BipartiteGraph
from linkPred import linkPred
from preferentialAttachment import prefAttach

#creating bipartite graph
bipartiteClass = BipartiteGraph()
bipartiteGraph = bipartiteClass.createGraph

# biSBM
linkPredictionGraph = linkPred(bipartiteGraph)
linkPredictionGraph.printAUC()

#pref attachment
# prefAttach = prefAttach(bipartiteGraph)
# prefAttach.printAUC()

#deg dist
# linkPredictionGraph = linkPred(bipartiteGraph)
# linkPredictionGraph.getDegDist()

# biSBMModel = biSBM(bipartiteGraph=bipartiteGraph)
# biSBM = biSBMModel.createBiSBM()