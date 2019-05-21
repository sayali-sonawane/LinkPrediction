from pyparsing import *
import re
from string import punctuation
from collections import defaultdict
import copy
import networkx as nx
from networkx.algorithms import bipartite
import pprint
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import random as rnd
from sklearn.metrics import roc_auc_score
import operator
from collections import OrderedDict
from itertools import islice
import math
from numpy.random import beta
from collections import Counter

List_Categories = []
Network_Data_Dict = {}
Network_Data_Dict = defaultdict(dict)
Degree_Dict = {}
#Pyparsing rule for extracting all tuples of the form (key:value)
key = Word(alphanums)('key')
colon = Suppress(':')
dot = Literal(".")
alphabets = Word(alphanums)('value')
floatnumber = Combine( Word(nums) + Optional( dot + Optional(Word(nums))))
value = Optional(alphabets) + Optional(floatnumber) 
kvexpression = key + colon + value

#Pyparing rule for extracting date
dash = '-'
ssn = Combine(Word(nums, exact=4) + dash + Word(nums, max=2) + dash + Word(nums, max=2))

#Pyparsing rule for extracting Categories
salutation     = Word( alphas )
comma          = Literal(",")
andlit         = Literal("&")
pipe           = Literal ("|")
eiphen         = Literal ("-")
Complete = pipe + Group(salutation + Optional(comma) + Optional(eiphen) + Optional (andlit) + Optional (salutation) + Optional (Word( alphas ))) 

X = []
enc='utf-8'
temp = []
config_data = open('Amazon_Data.txt','r',encoding=enc)
        
for line in config_data.readlines()[:50000]:
    for match in kvexpression.scanString(line):
        result = match[0]
        if result.key == 'Id':
            List_Categories[:] = []
            Dict_network_data_index = result.value
            #print ('Id : ',result.value)
            Network_Data_Dict[result.value].update ({result.key:result.value})
            Network_Data_Dict[Dict_network_data_index].update ({'Customer_List':[]})
            Network_Data_Dict[Dict_network_data_index].update ({'Date':[]})
            Network_Data_Dict[Dict_network_data_index].update ({'Rating':[]})
        elif result.key == 'title':
            line = str(line)
            title = line.replace('title:','').replace('\n','')
            Network_Data_Dict[Dict_network_data_index].update ({'title':title})
        elif result.key == 'reviews':
            line = str(line)
            Total_Reviews = re.search(r'\d+', line).group()
            Network_Data_Dict[Dict_network_data_index].update ({'Total_Reviews':Total_Reviews})
        elif result.key == 'cutomer':
            Network_Data_Dict[Dict_network_data_index]['Customer_List'].append (str(result.value))
        elif result.key == 'rating':
            Network_Data_Dict[Dict_network_data_index]['Rating'].append (str(result.value))
        else:
            Network_Data_Dict[Dict_network_data_index].update ({result.key:result.value})    
            
        
    for match in Complete.scanString(line):
        result = str(match[0])
        result = re.sub("'|,'{}", '', result)
        to_remove = "[,|]"
        table = {ord(char): None for char in to_remove}
        result = result.translate(table)
        List_Categories.append(result)
        temp = copy.copy(List_Categories)
    Network_Data_Dict[Dict_network_data_index].update ({'Category_Type':temp})
    List_Categories[:] = []

    for match in ssn.scanString(line):
        tempDate = str(match[0])
        date = tempDate.replace('[','').replace(']','').replace("'",'')
        Network_Data_Dict[Dict_network_data_index]['Date'].append (date)
    
#pprint.pprint (Network_Data_Dict)


#Creating list of edges, Buyer Nodes and Products Nodes in Bipartite Graph and plotting the Bipartite Graph
customer_list = []
Product_Node_List = []
Customer_Node_List = []
Edge_List = []
Network_Bipartite_Graph = nx.Graph()
for each_enty in Network_Data_Dict:
    if Network_Data_Dict[each_enty]['Customer_List'] != []:
        Product_Node_List.append(Network_Data_Dict[each_enty]['ASIN'])
        Customer_Node_List.extend(Network_Data_Dict[each_enty]['Customer_List'])

for each_enty in Network_Data_Dict:
    for each_cust in Network_Data_Dict[each_enty]['Customer_List']:
        if ((each_cust in Customer_Node_List) and (Network_Data_Dict[each_enty]['ASIN'] in Product_Node_List)):
            Network_Bipartite_Graph.add_edge(each_cust,Network_Data_Dict[each_enty]['ASIN'])
            Edge_List.append((each_cust,Network_Data_Dict[each_enty]['ASIN']))    
Network_Bipartite_Graph.add_nodes_from(Customer_Node_List, bipartite='Customers')
Network_Bipartite_Graph.add_nodes_from(Product_Node_List, bipartite='Products')

for every_ID in Network_Data_Dict:
    product_node = Network_Data_Dict[every_ID]['ASIN']
    if product_node in Product_Node_List:
        Network_Bipartite_Graph.node[product_node]['Category'] = Network_Data_Dict[every_ID]['Category_Type']

print (nx.info (Network_Bipartite_Graph))


#Calculate Square Clustering Coefficient for Bipartite networks
##Y = []
##a = {}
##Clustering_Coefficient_Bipartite_Network = nx.square_clustering(Network_Bipartite_Graph,Customer_Node_List)
##for key, value in Clustering_Coefficient_Bipartite_Network.items():
##    Y.append(value)
##
##
###plt.scatter(list(a.keys()), list(a.values()), label= "stars", color= "m",marker= "*", s=30)
###plt.plot(list(a.keys()), list(a.values()))#, color='green', linestyle='dashed', linewidth = 3,marker='o', markerfacecolor='blue', markersize=12)
### x-axis label
##plt.loglog(list(test_dict.values()),Y,color='red')
##plt.xlabel('x - axis')
### frequency label
##plt.ylabel('y - axis')
### plot title
##plt.title('My scatter plot!')
### showing legend
##plt.legend()
### function to show the plot
##plt.show()

##pos = {}
##plt.figure(figsize=(8,8))
##X, Y = nx.bipartite.sets(Network_Bipartite_Graph,top_nodes=Customer_Node_List)
##pos.update((node, (0, index*10)) for index, node in enumerate(X))
##pos.update((node, (0.5, index*45)) for index, node in enumerate(Y))
##nx.draw(Network_Bipartite_Graph,edge_color="#ffa000",node_size = 25,node_color="#800000",pos=pos)
##plt.show()


#Plotting one mode projection graph of customers
#plt.figure(figsize=(10,10))
#Customer_One_Mode_Projection = nx.Graph()
#print ("Creating One Mode Projection\n")
#Customer_One_Mode_Projection = bipartite.weighted_projected_graph(Network_Bipartite_Graph, Customer_Node_List, ratio=False)
#spring_pos=nx.spring_layout(Customer_One_Mode_Projection,k=0.3)
#print ("One Mode Projection Created\n")
#nx.draw_networkx_nodes(Customer_One_Mode_Projection, pos=spring_pos, nodelist = Customer_Node_List, node_size=25, cmap=plt.cm.RdYlBu,node_color="#00BCD4", with_labels = True,font_size = 10)
#nx.draw_networkx_edges(Customer_One_Mode_Projection, pos=spring_pos, alpha=0.3)
#plt.axis("off")
#plt.title("One Mode Projection of Customer-Product Bipartite Network for Customer Nodes", fontweight='bold')
#plt.show(Customer_One_Mode_Projection)


Auc_Dict_JC = OrderedDict()
#Calculating AUC for Jaccard Similarity Index
def Jaccard_Coefficient():
    global Network_Bipartite_Graph,Edge_List,Customer_Node_List,Product_Node_List,Auc_Dict_JC
    Total_No_Edges = len(Edge_List)
    Jaccard_Coefficient_List = []
    JC_Non_Sampled_Edges_Score = []
    True_Positives_List = []
    Auc_Score_Dict = {}
    neighbor_list = []
    Jaccard_Coefficient_Dict = {}
    Sorted_Jaccard_Coefficient_Dict = OrderedDict()
    Binary_Dict_EdgeList = {}
    Highest_Jaccard_Values = []
    Customer_One_Mode_Projection = bipartite.weighted_projected_graph(Network_Bipartite_Graph, Customer_Node_List, ratio=False)
    Fraction_of_Edges_Shown = 0.1
    j = 1
    auc_input_1 = []
    auc_input_2 = []
    #Calculating Binary List for all the present and not present edges in original graph
    while (True):
        No_of_Sampled_Edges = int (Fraction_of_Edges_Shown * Total_No_Edges)
        print ("No. of Sampled Edges - ",No_of_Sampled_Edges)
        Sampled_Edges = rnd.sample(Edge_List,No_of_Sampled_Edges)
        No_Edges_Not_Sampled = Total_No_Edges - No_of_Sampled_Edges
        for every_customer in Customer_Node_List:
            for every_product in Product_Node_List:
                if ((every_customer,every_product)) not in Sampled_Edges:
                    Cust_Neighbor_List = Customer_One_Mode_Projection.neighbors(every_customer)
                    list_neighbor = list(Network_Bipartite_Graph.neighbors(every_product))
                    set_Customer = set(Cust_Neighbor_List)
                    set_Product = set(list_neighbor)
                    Jaccard_Coefficient = float (len (set_Customer.intersection(set_Product)))/ float (len(set_Customer.union(set_Product)))
                    Jaccard_Coefficient_Dict.update({(every_customer,every_product):Jaccard_Coefficient})
        Sorted_Jaccard_Coefficient_Dict = OrderedDict(sorted(Jaccard_Coefficient_Dict.items(), key=operator.itemgetter(1), reverse=True))
        Highest_Jaccard_Values = OrderedDict(sorted(dict(list(Sorted_Jaccard_Coefficient_Dict.items()) [:No_Edges_Not_Sampled])))

        for every_cust in Customer_Node_List:
            for every_prod in Product_Node_List:
                if(every_cust,every_prod) in Edge_List:
                    auc_input_1.append(int(1))
                else:
                    auc_input_1.append(int(0))
                if(((every_cust,every_prod) in Highest_Jaccard_Values) or ((every_cust,every_prod) in Sampled_Edges)) :
                    auc_input_2.append(int(1))
                else:
                    auc_input_2.append(int(0))
        auc_Score = roc_auc_score(auc_input_1, auc_input_2)
        print ("Fraction_Labels -(%d), AUC_Score -(%d) ",Fraction_of_Edges_Shown,auc_Score)
        Auc_Dict_JC.update({Fraction_of_Edges_Shown:auc_Score})
        auc_input_1[:] = []
        auc_input_2[:] = []
        Jaccard_Coefficient_Dict.clear()
        Sorted_Jaccard_Coefficient_Dict.clear()
        Highest_Jaccard_Values.clear()
        Fraction_of_Edges_Shown+=0.1
        if Fraction_of_Edges_Shown > 0.9:
            break
        
Jaccard_Coefficient()

Auc_Dict_CN = OrderedDict()
#Calculating Common Neighbor Index
def Common_Neighbor():
    global Network_Bipartite_Graph,Edge_List,Customer_Node_List,Product_Node_List,Auc_Dict_CN
    Total_No_Edges = len(Edge_List)
    Auc_Score_Dict = {}
    neighbor_list = []
    Common_Neighbor_Dict = {}
    Sorted_Common_Neighbor_Dict = OrderedDict()
    Highest_Common_Neighbor_Values = []
    Customer_One_Mode_Projection = bipartite.weighted_projected_graph(Network_Bipartite_Graph, Customer_Node_List, ratio=False)
    Fraction_of_Edges_Shown = 0.1
    auc_input_1 = []
    auc_input_2 = []
    Fraction_of_Edges_Shown = 0.1
    Auc_Dict_JC = OrderedDict()
    while (True):
        No_of_Sampled_Edges = int (Fraction_of_Edges_Shown * Total_No_Edges)
        print ("No. of Sampled Edges - ",No_of_Sampled_Edges)
        Sampled_Edges = rnd.sample(Edge_List,No_of_Sampled_Edges)
        No_Edges_Not_Sampled = Total_No_Edges - No_of_Sampled_Edges
        for every_customer in Customer_Node_List:
            for every_product in Product_Node_List:
                if ((every_customer,every_product)) not in Sampled_Edges:
                    Cust_Neighbor_List = Customer_One_Mode_Projection.neighbors(every_customer)
                    list_neighbor = list(Network_Bipartite_Graph.neighbors(every_product))
                    set_Customer = set(Cust_Neighbor_List)
                    set_Product = set(list_neighbor)
                    Common_Neighbor = float (len (set_Customer.intersection(set_Product)))
                    Common_Neighbor_Dict.update({(every_customer,every_product):Common_Neighbor})
        Sorted_Common_Neighbor_Dict = OrderedDict(sorted(Common_Neighbor_Dict.items(), key=operator.itemgetter(1), reverse=True))
        Highest_Common_Neighbor_Values = OrderedDict(sorted(dict(list(Sorted_Common_Neighbor_Dict.items()) [:No_Edges_Not_Sampled])))

        #print (Highest_Common_Neighbor_Values)
        
        for every_cust in Customer_Node_List:
            for every_prod in Product_Node_List:
                if(every_cust,every_prod) in Edge_List:
                    auc_input_1.append(int(1))
                else:
                    auc_input_1.append(int(0))
                if(((every_cust,every_prod) in Highest_Common_Neighbor_Values) or ((every_cust,every_prod) in Sampled_Edges)) :
                    auc_input_2.append(int(1))
                else:
                    auc_input_2.append(int(0))
        auc_Score = roc_auc_score(auc_input_1, auc_input_2)
        print ("Fraction_Labels -(%d), AUC_Score -(%d) ",Fraction_of_Edges_Shown,auc_Score)
        Auc_Dict_CN.update({Fraction_of_Edges_Shown:auc_Score})
        auc_input_1[:] = []
        auc_input_2[:] = []
        Common_Neighbor_Dict.clear()
        Sorted_Common_Neighbor_Dict.clear()
        Highest_Common_Neighbor_Values.clear()
        Fraction_of_Edges_Shown+=0.1
        if Fraction_of_Edges_Shown > 0.9:
            break

Common_Neighbor()

Auc_Dict_AAI = OrderedDict()
#Calculating Adamic-Adar Index
def Adamic_Adar_Index():
    global Network_Bipartite_Graph,Edge_List,Customer_Node_List,Product_Node_List,Auc_Dict_AAI
    Total_No_Edges = len(Edge_List)
    Auc_Score_Dict = {}
    neighbor_list = []
    Adamic_Adar_Index_Dict = {}
    Sorted_Adamic_Adar_Index_Dict = OrderedDict()
    Highest_Adamic_Adar_Index_Values = []
    Customer_One_Mode_Projection = bipartite.weighted_projected_graph(Network_Bipartite_Graph, Customer_Node_List, ratio=False)
    Fraction_of_Edges_Shown = 0.1
    auc_input_1 = []
    auc_input_2 = []
    Auc_Dict_AAI = OrderedDict()
    Common_Neighbors_Neighbor = []
    Common_Neighbor = [] #List of common neighbors between Customers and Products
    while (True):
        No_of_Sampled_Edges = int (Fraction_of_Edges_Shown * Total_No_Edges)
        print ("No. of Sampled Edges - ",No_of_Sampled_Edges)
        Sampled_Edges = rnd.sample(Edge_List,No_of_Sampled_Edges)
        No_Edges_Not_Sampled = Total_No_Edges - No_of_Sampled_Edges
        for every_customer in Customer_Node_List:
            for every_product in Product_Node_List:
                if ((every_customer,every_product)) not in Sampled_Edges:
                    Cust_Neighbor_List = Customer_One_Mode_Projection.neighbors(every_customer)
                    list_neighbor = list(Network_Bipartite_Graph.neighbors(every_product))
                    set_Customer = set(Cust_Neighbor_List)
                    set_Product = set(list_neighbor)
                    Common_Neighbor = list(set_Customer.intersection(set_Product))
                    for each_item in Common_Neighbor:
                        Common_Neighbors_Neighbor.append(Customer_One_Mode_Projection.neighbors(each_item))
                    if len(Common_Neighbors_Neighbor) != 0.0:
                        Adamic_Adar_Index = float(1.0)/float(math.log10(len(Common_Neighbors_Neighbor)))
                    else:
                        Adamic_Adar_Index = float(0.0)
                    Adamic_Adar_Index_Dict.update({(every_customer,every_product):Adamic_Adar_Index})
        Sorted_Adamic_Adar_Index_Dict = OrderedDict(sorted(Adamic_Adar_Index_Dict.items(), key=operator.itemgetter(1), reverse=True))
        Highest_Adamic_Adar_Index_Values = OrderedDict(sorted(dict(list(Sorted_Adamic_Adar_Index_Dict.items()) [:No_Edges_Not_Sampled])))

        for every_cust in Customer_Node_List:
            for every_prod in Product_Node_List:
                if(every_cust,every_prod) in Edge_List:
                    auc_input_1.append(int(1))
                else:
                    auc_input_1.append(int(0))
                if(((every_cust,every_prod) in Highest_Adamic_Adar_Index_Values) or ((every_cust,every_prod) in Sampled_Edges)) :
                    auc_input_2.append(int(1))
                else:
                    auc_input_2.append(int(0))
        auc_Score = roc_auc_score(auc_input_1, auc_input_2)
        print ("Fraction_Labels -(%d), AUC_Score -(%d) ",Fraction_of_Edges_Shown,auc_Score)
        Auc_Dict_AAI.update({Fraction_of_Edges_Shown:auc_Score})
        auc_input_1[:] = []
        auc_input_2[:] = []
        Adamic_Adar_Index_Dict.clear()
        Sorted_Adamic_Adar_Index_Dict.clear()
        Highest_Adamic_Adar_Index_Values.clear()
        Fraction_of_Edges_Shown+=0.1
        if Fraction_of_Edges_Shown > 0.9:
            break

Adamic_Adar_Index()


def Clustering_Coeff():
    Clustering_Coefficient = []
    Degree = []
    Y = []
    Z = []
    Network_Bipartite_Graph_top,Network_Bipartite_Graph_bottom = bipartite.sets(Network_Bipartite_Graph,top_nodes=Customer_Node_List)
    NTop = list(Network_Bipartite_Graph_top)
    NBottom = list(Network_Bipartite_Graph_bottom)
    print ("Length of Customer Node - ",len(NTop))
    print ("Length of Product Node - ",len(NBottom))
    Clustering_Coefficient_Bipartite_Network = nx.square_clustering(Network_Bipartite_Graph,NTop)
    for key, value in Clustering_Coefficient_Bipartite_Network.items():
        Y.append(value)
    Avg_CLustering_Coeffcient_Customer_Network = float(sum(Y))/float(len(Y))
    print ("Avg_CLustering_Coeffcient_Customer_Network - ",Avg_CLustering_Coeffcient_Customer_Network)

    Clustering_Coefficient_Bipartite_Network_Product = nx.square_clustering(Network_Bipartite_Graph,NBottom)
    for key, value in Clustering_Coefficient_Bipartite_Network_Product.items():
        Z.append(value)
    Avg_CLustering_Coeffcient_Product_Network = float(sum(Z))/float(len(Z))
    print ("Avg_CLustering_Coeffcient_Product_Network - ",Avg_CLustering_Coeffcient_Product_Network)


Clustering_Coeff()

Auc_Dict_JC_lists = sorted(Auc_Dict_JC.items())
x, y = zip(*Auc_Dict_JC_lists)

Auc_Dict_CN_lists = sorted(Auc_Dict_CN.items())
u, v = zip(*Auc_Dict_CN_lists)

Auc_Dict_AAI_lists = sorted(Auc_Dict_AAI.items())
m, n = zip(*Auc_Dict_AAI_lists)

#Preferential Attachment Values
c = (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)
d = (0.542763157894,0.586622807017,0.630482456140,0.656798245614,0.7006578947368,0.7269736842105,0.7620614035087,0.7883771929824,0.8322368421052)

plt.plot(x,y)
plt.plot(u,v)
plt.plot(m,n)
plt.plot(c,d)

plt.ylabel('AUC')
plt.xlabel('Fraction of edges Observed')
plt.title('Link Prediction for Amazon Customer-Product Network for 2000 Nodes')
plt.savefig('Amazon_Data_AUC.png')
plt.legend(["Jaccard Coefficient","Common Neighbor","Adamic-Adar Index","Preferential Attachment"], loc = 'bottom right')
plt.show()
