from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import numpy as np
import string
import distance

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

f = open("FriendFeatures.text", "r")
f1 = f.readlines() #for each line
list_of_friendTAG = []
for x in f1:
    l = x.split(',')

    temp = {
        'name': l[0],
        'genre': l[1],
        'add_info': l[2:len(l)-1],
        'birthday': l[len(l)-1]
    }

    #the first control, if is correct the birthday day
    control_birthday = temp['birthday'].split() 
    try:
        control_birthday[0] = int(control_birthday[0])
    except ValueError:
        temp['add_info'].append(temp['birthday'])
        temp['birthday'] = '1 gennaio 1998' #set nan for distinguishing that the person hasn't set his birthday

    #the second control, if is correct the birthday day
    control_birthday = temp['birthday'].split() 
    try:
        control_birthday[len(control_birthday)-1] = int(control_birthday[len(control_birthday)-1])
    except ValueError:
        temp['birthday'] = '1 gennaio 1998' #set nan for distinguishing that the person hasn't set his birthday
        
    list_of_friendTAG.append(temp)


#remove stop words, from temp['add_info']
stop_words = stopwords.words('italian')

for x in list_of_friendTAG:
    for idx,add_infoX in enumerate(x['add_info']):
        word_tokens = word_tokenize(add_infoX)
        x['add_info'][idx] = word_tokens

        #drop the stop words, from a list:
        for word in stop_words:
            if word in x['add_info'][idx]:
                while (x['add_info'][idx].count(word)):  
                    x['add_info'][idx].remove(word)
        
        #drop the punctuation, from a list:
        for punct in string.punctuation:
            if punct in x['add_info'][idx]:
                while (x['add_info'][idx].count(punct)):  
                    x['add_info'][idx].remove(punct)

#change the list of list in a simple LIST
for x in list_of_friendTAG:
    if len(x['add_info']) != 0:
        x['add_info'] = list(np.concatenate(x['add_info']))

#measure of jaccard similary and prints your friends
with open('SimilarityFriends.txt', 'w', newline = '\n') as file:
    for x in list_of_friendTAG:
        
        list1_add_info = x['add_info']
        list1_genre = x['genre']
        list1_birthday = x['birthday']
        
        for y in list_of_friendTAG:
            list2_add_info = y['add_info']
            list2_genre = y['genre']
            list2_birthday = y['birthday']

            if(x['name'] != y['name']):
                total_jacc = 0
                
                total_jacc += jaccard_similarity(list1_add_info,list2_add_info)
                total_jacc += distance.jaccard(list1_genre,list2_genre)
                total_jacc += distance.jaccard(list1_birthday,list2_birthday)
                
                if total_jacc > 1.2:
                    year = int(y['birthday'].split()[2])
                    age = 2020 - year

                    if total_jacc < 1.8:
                        if age <= 29:
                            ins=x['name']+","+y['name']+','+y['genre']+','+"outer_cluster"+','+"ragazzo"
                        elif age >= 30 and age <= 64:
                            ins=x['name']+","+y['name']+','+y['genre']+','+"outer_cluster"+','+"adulto"
                        else:
                            ins=x['name']+","+y['name']+','+y['genre']+','+"outer_cluster"+','+"anziano"
                    else:
                        if age <= 29:
                            ins=x['name']+","+y['name']+','+y['genre']+','+"inner_cluster"+','+"ragazzo"
                        elif age >= 30 and age <= 64:
                            ins=x['name']+","+y['name']+','+y['genre']+','+"inner_cluster"+','+"adulto"
                        else:
                            ins=x['name']+","+y['name']+','+y['genre']+','+"inner_cluster"+','+"anziano"


                    file.write(ins+'\n')
