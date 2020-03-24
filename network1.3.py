#Execute with Python2
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import sys
import numpy as np
import os
reload(sys)
sys.setdefaultencoding('utf-8')

#We have the correct distribution, calculate the entropy for each item: genre,add_info and birthday
def entr_genre(count_male, count_female):
	tot = float(count_male) + float(count_female)
	
	try:
		e1 = (count_male/tot) * np.log2(1/(count_male/tot))	
	except ZeroDivisionError as error:
		e1 = 0

	try:
		e2 = (count_female/tot) * np.log2(1/(count_female/tot))	
	except ZeroDivisionError as error:
		e2 = 0
	
	return e1+e2

def entr_addinfo(count_inner, count_outer):
	tot = float(count_inner) + float(count_outer)

	try:
		e1 = (count_inner/tot) * np.log2(1/(count_inner/tot))	
	except ZeroDivisionError as error:
		e1 = 0	
	
	try:
		e2 = (count_outer/tot) * np.log2(1/(count_outer/tot))	
	except ZeroDivisionError as error:
		e2 = 0
	
	return e1+e2

def entr_birthday(count_boy, count_adult, count_elder):
	tot = float(count_boy) + float(count_adult) + float(count_elder)

	try:
		e1 = (count_boy/tot) * np.log2(1/(count_boy/tot))
	except ZeroDivisionError as error:
		e1 = 0 
	
	try:
		e2 = (count_adult/tot) * np.log2(1/(count_adult/tot))
	except ZeroDivisionError as error:
		e2 = 0
	
	try:
		e3 = (count_elder/tot) * np.log2(1/(count_elder/tot))	
	except ZeroDivisionError as error:
		e3 = 0
	
	return e1+e2+e3

#return the main entropy
def entropy(entropy_node):	
	f = open("SimilarityFriendsJeremy.txt", "r")
	f1 = f.readlines() #for each line
	list_of_friend = []
	for x in f1:
		list_of_friend.append(x.split(','))
	
	#counter genre maschio/femmina
	count_male = 0
	count_female = 0

	#counter type similarity inner/outer
	count_inner = 0
	count_outer = 0

	#counter ranges ragazzo/adulto/anziano
	count_boy = 0
	count_adult = 0
	count_elder = 0 

	for x in list_of_friend:
		if x[0] == entropy_node:
			
			#add the genre
			if x[2] == "maschio":
				count_male +=1
			else:
				count_female += 1

			if x[3] == "inner_cluster":
				count_inner +=1
			else:
				count_outer += 1
			
			x[4] = x[4].replace('\n','')
			if x[4] == "ragazzo":
				count_boy +=1
			elif x[4] == "adulto":
				count_adult += 1
			else:
				count_elder += 1

	return round((entr_genre(count_male, count_female) + entr_addinfo(count_inner, count_outer) + entr_birthday(count_boy, count_adult, count_elder))/3,2)

#display the clustering for a node
def clust(entropy_node, listclustering_nodes):
	clust_coeff = 0
	for x in listclustering_nodes:
		if x == entropy_node:
			clust_coeff = listclustering_nodes[x]
	
	return round(clust_coeff,2)

def child(G):
	fig = pylab.figure()
	fig.set_facecolor("#ffffff")

	nx.draw(G,
		alpha=.5,

		#font style
		font_size=5,
		font_color="#000000",
		font_family = 'sans-serif',

		#node style
		node_color='#12ddff',
		edge_color='#607d8b',
		node_size=500,
		cmap=pylab.cm.Blues,
		with_labels=True)

	plt.savefig("SimilarityWithOuterCluster.png")

	plt.show(block=False)
	plt.pause(180)
	plt.close("all")
	os._exit(0)

def parent(G):
	#get for each node the clustering coefficient
	listclustering_nodes = nx.clustering(G) 
	
	entropy_node = raw_input("\nWhich Node (write esc to exit): ")
	
	if entropy_node != "esc":
		print("\nThe entropy of {} is {}".format(entropy_node,entropy(entropy_node) ))
		print("The coefficient clustering of {} is {}".format(entropy_node,clust(entropy_node, listclustering_nodes) ))

	return entropy_node


if __name__ == '__main__':
	print("Which option do you want?")
	print("1. Similarity Friends")
	print("2. Measures of centrality with your friends")
	choose = int(raw_input("Choose it: "))

	if choose == 1:
		file_name = "SimilarityFriends.txt"

		file = open(file_name, "r").read()
		arr = file.split("\n")
		arr.pop()

		G = nx.Graph()

		for i in arr:
			tmp = i.split(",")
			if(tmp[3] == "outer_cluster"): 
				G.add_node(tmp[1])
			else:
				G.add_edge(*(tmp[0], tmp[1]))

		pid = os.fork()
		while True:
			if pid == 0:
				child(G)
			else:
				answer = parent(G)
			
			if answer != "esc":
				continue
			else:
				break

	else:
		file_name = "YourFriends.txt"

		file = open(file_name, "r").read()
		arr = file.split("\n")
		arr.pop()

		G = nx.Graph()

		for i in arr:
			tmp = i.split(",") 
			G.add_edge(*(tmp[0], tmp[1]))

		fig = pylab.figure()
		fig.set_facecolor("#ffffff")

		while True:
			print("\nWhich measure of centrality do you want?")
			print("1. degree centrality")
			print("2. betweenness centrality")
			print("3. closeness centrality")
			print("4. pagerank centrality")
			choose2 = int(raw_input("Choose it (write 5 to exit): "))

			if choose2 == 1:
				c = nx.degree_centrality(G)
			elif choose2 == 2:
				c = nx.betweenness_centrality(G,normalized = True,endpoints = False)
			elif choose2 == 3:
				c = nx.closeness_centrality(G)
			elif choose2 == 4:
				c = nx.pagerank(G, alpha = 0.8)
			else:
				break

			nx.draw(G,
				alpha=.5,

				#font style
				font_size=5,
				font_color="#000000",
				font_family = 'sans-serif',
			
				#node style
				node_color='#00ff00',
				edge_color='#607d8b',
				node_size=[(c[n]+0.00001)*5000 for n in G.nodes()], #make a values normalization
				cmap=pylab.cm.Blues,
				with_labels=True) 

			if choose2 == 1:
				plt.savefig("Degree_Graph.png")
			elif choose2 == 2:
				plt.savefig("Betweenness_Graph.png")
			elif choose2 == 3:
				plt.savefig("Closeness_Graph.png")
			elif choose2 == 4:
				plt.savefig("PageRank_Graph.png")

			plt.show()