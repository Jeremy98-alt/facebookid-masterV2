# facebookid-masterV2

This is a project that I made with my colleague Luca Occhipinti. In the first part of this project we selected all our friends to create an icon network based on a chain of mutual friends. After this job, for each person, we extracted the information and we made a new icon network based on friends' similarity features.

# Usage

1.  In "scraping1.3.py" you can extract your friends and then, for each friend, the mutual friends with you 
2.  In "GetInformations1.4.py" you can obtain information about you and your friends
3.  In "StatisticalInformation1.1.py" you can obtain a file where there are pairs of people who are similar to each other
4.  In "network.1.2.py" you can choose two types of execution mode:
       *  in the first you can connect all the friends who are similar to each other. After plotting your network, You can obtain information about each node such us the clustering coefficient and the relative entropy
       *  in the second you can connect yourself to your friends and these to the mutual friends with you. you can consider different centrality measures before plotting the nodes 

# Attention
we didn't report our personal files for privacy! ... a great pleasure for us, is to thank to Stefano Borzi and Alessio Piazza for the actual idea of part of this project. Where takes the foundamentals to the network of friends.
