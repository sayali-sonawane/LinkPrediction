from pyparsing import *
import re
from collections import defaultdict
import copy
import networkx as nx
from networkx.algorithms import bipartite
import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from string import punctuation

class BipartiteGraph:
    @property
    def createGraph(self):
        List_Categories = []
        # Network_Data_Dict = {}
        Network_Data_Dict = defaultdict(dict)

        # Pyparsing rule for extracting all tuples of the form (key:value)
        key = Word(alphanums)('key')
        colon = Suppress(':')
        dot = Literal(".")
        alphabets = Word(alphanums)('value')
        floatnumber = Combine(Word(nums) + Optional(dot + Optional(Word(nums))))
        value = Optional(alphabets) + Optional(floatnumber)
        kvexpression = key + colon + value

        # Pyparing rule for extracting date
        dash = '-'
        ssn = Combine(Word(nums, exact=4) + dash + Word(nums, max=2) + dash + Word(nums, max=2))

        # Pyparsing rule for extracting Categories
        salutation = Word(alphas)
        comma = Literal(",")
        andlit = Literal("&")
        pipe = Literal("|")
        eiphen = Literal("-")
        Complete = pipe + Group(
            salutation + Optional(comma) + Optional(eiphen) + Optional(andlit) + Optional(salutation) + Optional(Word(alphas)))

        temp = []
        enc = 'utf-8'
        path = "C:/Users/Sayali Sonawane/PycharmProjects/LinkPredictionBapartiteNetwork/Amazon_Data.txt"
        config_data = open(path, 'r', encoding=enc)
        print("read data")
        for line in config_data.readlines()[:100]:
            for match in kvexpression.scanString(line):
                result = match[0]
                if result.key == 'Id':
                    List_Categories[:] = []
                    Dict_network_data_index = result.value
                    # print ('Id : ',result.value)
                    Network_Data_Dict[result.value].update({result.key: result.value})
                    Network_Data_Dict[Dict_network_data_index].update({'Customer_List': []})
                    Network_Data_Dict[Dict_network_data_index].update({'Date': []})
                    Network_Data_Dict[Dict_network_data_index].update({'Rating': []})
                elif result.key == 'title':
                    line = str(line)
                    title = line.replace('title:', '').replace('\n', '')
                    Network_Data_Dict[Dict_network_data_index].update({'title': title})
                elif result.key == 'reviews':
                    line = str(line)
                    Total_Reviews = re.search(r'\d+', line).group()
                    Network_Data_Dict[Dict_network_data_index].update({'Total_Reviews': Total_Reviews})
                elif result.key == 'cutomer':
                    Network_Data_Dict[Dict_network_data_index]['Customer_List'].append(str(result.value))
                elif result.key == 'rating':
                    Network_Data_Dict[Dict_network_data_index]['Rating'].append(str(result.value))
                else:
                    Network_Data_Dict[Dict_network_data_index].update({result.key: result.value})

            for match in Complete.scanString(line):
                result = str(match[0])
                result = re.sub("'|,'{}", '', result)
                to_remove = "[,|]"
                table = {ord(char): None for char in to_remove}
                result = result.translate(table)
                List_Categories.append(result)
                temp = copy.copy(List_Categories)
            Network_Data_Dict[Dict_network_data_index].update({'Category_Type': temp})
            List_Categories[:] = []

            for match in ssn.scanString(line):
                tempDate = str(match[0])
                date = tempDate.replace('[', '').replace(']', '').replace("'", '')
                Network_Data_Dict[Dict_network_data_index]['Date'].append(date)

        # pprint.pprint(Network_Data_Dict)
        print(Network_Data_Dict)
        # Creating list of edges, Buyer Nodes and Products Nodes in Bipartite Graph and plotting the Bipartite Graph
        customer_list = []
        Product_Node_List = []
        Customer_Node_List = []

        technology = [  ' Technology', ' Physics', ' Anthropology', ' Sociology', ' Otolaryngology', ' Ecology', ' Internal Medicine', ' Graphic Novels', ' Windows OS', ' Thermodynamics', ' Ideologies', ' Reference', ' Internet', ' Windows', ' Camera & Photo', ' Windows - General', ' Graphics & Illustration', ' Professional Science', ' Philosophy', ' Education', ' Biology', ' Pedagogy', ' Databases', ' Study Guides', ' Humanities', ' Engineering', ' Environment', ' Electrical & Optical', ' Security', ' TOEFL', ' Entomology', ' Optics', ' Computer & Internet Books', ' Phenomenology', ' Biological Sciences', ' Science & Technology', ' Social Sciences', ' Science', ' Graphic Design', ' Encyclopedias', ' Computers & Internet']
        art = [' Photography Books',' Performing Arts', ' Poetry', ' Crafts & Hobbies', ' Artists  A', ' Graphic Arts', ' Photo Essays', ' Contemporary', ' Dance', ' Arts & Photography']
        business = [' Sales', ' Personal Finance', ' Manager', ' Investing', ' Warner Video Bargains', ' Management & Leadership', ' Business History', ' Warner Home Video', ' Project Management', ' Retirement Planning', ' Law', ' Law Practice', ' Other Practices', ' Disney Home Video', ' New Yorker Films', ' Deals Under', ' Industries & Professions', ' Management', ' Clamp School Detectives', ' Imports', ' Business & Investing Books', ' Home & Office',' Professional & Technical', ' Specialty Stores',' DVD Outlet',' Digital Business',' Deutsche Grammophon Records']
        fiction = [' Children', ' Artists & Writers', ' Thrillers', ' Comics & Graphic Novels', ' Short Stories', ' Genre Fiction', ' Romance', ' Fiction', ' Anime & Manga', ' Barney', ' Classics', ' Spy Stories', ' Superheroes', ' Twain  Mark', ' Drama', ' Books on Tape', ' Literature & Fiction', ' By Theme', ' World Literature', ' Thomas a', ' Witchcraft', ' Monsters', ' Popular Fiction', ' Characters & Series', ' Science Fiction', ' Mystery & Thrillers']
        general = [' Book Clubs', ' General', ' New & Used Textbooks', ' Special Topics', ' Genres', ' Special Features', ' DVDs Under', ' Paperback', ' jp - unknown', ' Test Prep Central', ' Puzzles', ' Amazon', ' All Deals', ' Special Interests', ' Collections & Readers', ' Books', ' Labels', ' DVD', ' Bargain Books Outlet', ' Infantil y familiar', ' Series', ' Categories', ' Boxed Sets', ' Authors  A', ' Special Groups', ' Concept Books', ' All Titles', ' Titles', ' Subjects', ' Formats']
        geography = [' Regions', ' Europe', ' Travel', ' New England', ' Travel Books', ' Tribal & Ethnic', ' Northeast', ' Outdoors & Nature', ' Middle Atlantic', ' Regional & International', ' United States', ' Travel Videos', ' Earth - Based Religions']
        health = [' Diets & Weight Loss', ' Cancer', ' Health  Mind', ' Cooking  Food', ' Physical Examination', ' Self Help', ' Infantil y juvenil', ' Pain Management', ' Obsessions', ' Diets', ' Disorders & Diseases', ' Pregnancy & Childbirth Books', ' Twins', ' Home & Garden', ' Baby -', ' Low Carb', ' Surgery', ' Medicine', ' Medical']
        history = [ ' History & Philosophy', ' Biographies & Memoirs', ' Memoirs', ' Historical', ' Historical Study', ' History', ' Biographies & Primers', ' By Decade', ' History of Technology']
        language = [ ' Libros en espa', ' Block  Francesca Lia', ' Spanish Language']
        movies = [ ' Animated Cartoons', ' Latin American Cinema', ' Bogosian  Eric']
        music = [ ' Rock', ' Eliot  T', ' Blues', ' Dance Pop', ' U', ' Music', ' Seventh Heaven', ' Dance & DJ', ' Studio Specials', ' Books  Music', ' Mozart  Wolfgang Amadeus', ' Jazz', ' Arena Rock', ' VHS', ' MTV', ' Modern Blues', ' Classic Rock', ' Vocal Jazz', ' New Age', ' Indie Music']
        people = [ ' Nonfiction', ' Women', ' Parenting Books', ' Family Life', ' Specific Groups', ' Kids & Family', ' People  A', ' Books for Babies', ' Inspirational', ' Teens', ' Hospitality  Travel', ' Cultural', ' Tarot', ' Styles', ' Lesbian Studies', ' Ages', ' Television', ' Mothers & Sons', ' Issues', ' Entertainment']
        political = [ ' Movements', ' Politics', ' Radical Thought', ' Revolutionary', ' Political']
        religion = [ ' African American', ' Islam', ' Christian Living', ' Christian DVD', ' Religions', ' Sermons', ' Religion & Spirituality', ' Clergy', ' Christian & Gospel', ' Protestantism', ' Christianity', ' Spirituality', ' Bibles', ' Jesus', ' Easwaran  Eknath', ' Pentecostal', ' Divination', ' Gospel', ' Occult', ' Greeley  Andrew', ' Youth Ministry', ' Occultism']
        sports = [ ' Games', ' Sports', ' Basketball', ' Adventurers & Explorers', ' Lackey  Mercedes']
        warfare = [ ' Naval', ' Military', ' World War II', ' Religious Warfare']

        Network_Bipartite_Graph = nx.Graph()
        for each_enty in Network_Data_Dict:
            if Network_Data_Dict[each_enty]['Customer_List'] != []:
                Product_Node_List.append(Network_Data_Dict[each_enty]['ASIN'])
                Customer_Node_List.extend(Network_Data_Dict[each_enty]['Customer_List'])
        print("customer list")
        Network_Bipartite_Graph.add_nodes_from(Customer_Node_List, bipartite='Customers')
        Network_Bipartite_Graph.add_nodes_from(Product_Node_List, bipartite='Products')
        for each_enty in Network_Data_Dict:
            for each_cust in Network_Data_Dict[each_enty]['Customer_List']:
                if ((each_cust in Customer_Node_List) and (Network_Data_Dict[each_enty]['ASIN'] in Product_Node_List)):
                    Network_Bipartite_Graph.add_edge(each_cust, Network_Data_Dict[each_enty]['ASIN'])

        print("added edges")

        category_list = set()
        for every_ID in Network_Data_Dict:
            product_node = Network_Data_Dict[every_ID]['ASIN']
            if product_node in Product_Node_List:
                Network_Bipartite_Graph.node[product_node]['Category'] = set()
                cats = Network_Data_Dict[every_ID]['Category_Type']
                for cat in cats:
                    if cat in technology:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('technology')
                    if cat in art:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('art')
                    if cat in business:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('business')
                    if cat in fiction:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('fiction')
                    if cat in general:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('general')
                    if cat in geography:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('geography')
                    if cat in health:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('health')
                    if cat in history:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('history')
                    if cat in language:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('language')
                    if cat in movies:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('movies')
                    if cat in music:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('music')
                    if cat in people:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('people')
                    if cat in religion:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('religion')
                    if cat in sports:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('sports')
                    if cat in warfare:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('warfare')
                    if cat in political:
                        Network_Bipartite_Graph.node[product_node]['Category'].add('political')
                    category_list = category_list | set(Network_Data_Dict[every_ID]['Category_Type'])
        print(nx.info(Network_Bipartite_Graph))
        temp = Network_Bipartite_Graph.node[Product_Node_List[0]]['Category']
        cust_nodes = set(n for n, d in Network_Bipartite_Graph.nodes(data=True) if d['bipartite'] == 'Customers')
        for cust in cust_nodes:
            if Network_Bipartite_Graph[cust]:
                prodList = Network_Bipartite_Graph[cust]
                if prodList:
                    labels = set()
                    for prod,value in prodList.items():
                        labels = labels | set(Network_Bipartite_Graph.node[prod]['Category'])
                    custLabels = []
                    for label in labels:
                        custLabels.append(label+"Cust")
                    Network_Bipartite_Graph.node[cust]['CustCategory'] = custLabels



        # pos = {}
        # plt.figure(figsize=(8, 8))
        # X, Y = nx.bipartite.sets(Network_Bipartite_Graph)
        # pos.update((node, (0, index * 10)) for index, node in enumerate(X))
        # pos.update((node, (0.5, index * 45)) for index, node in enumerate(Y))
        # nx.draw(Network_Bipartite_Graph, edge_color="#ffa000", node_size=25, node_color="#800000", pos=pos)
        # plt.show()
        #
        # # Plotting one mode projection graph of customers
        # plt.figure(figsize=(10, 10))
        # # Customer_One_Mode_Projection = nx.Graph()
        # print("Creating One Mode Projection\n")
        # Customer_One_Mode_Projection = bipartite.weighted_projected_graph(Network_Bipartite_Graph, Customer_Node_List,
        #                                                                   ratio=False)
        # spring_pos = nx.spring_layout(Customer_One_Mode_Projection, k=0.7)
        # print("One Mode Projection Created\n")
        # nx.draw_networkx_nodes(Customer_One_Mode_Projection, pos=spring_pos, nodelist=Customer_Node_List, node_size=25,
        #                        cmap=plt.cm.RdYlBu, node_color="#00BCD4", with_labels=True, font_size=10)
        # nx.draw_networkx_edges(Customer_One_Mode_Projection, pos=spring_pos, alpha=0.3)
        # plt.axis("off")
        # plt.title("One Mode Projection of Customer-Product Bipartite Network for Customer Nodes", fontweight='bold')
        # plt.show(Customer_One_Mode_Projection)

        # print (Customer_One_Mode_Projection.edge

        return Network_Bipartite_Graph