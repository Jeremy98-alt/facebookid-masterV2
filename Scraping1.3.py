from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import time

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install()) 
driver.get('https://it-it.facebook.com/')

username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
submit = driver.find_element_by_id("loginbutton")

#login to enter in your profile
username.send_keys(input('Email: '))
password.send_keys(input('Password: '))

submit.click()

#put here your profile friends link 
driver.get("insert-your-profile-friends-link")

#scrape whole page for getting names
pause_time = 1
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    time.sleep(pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

usernames = []
#extract the main div with friends
html_list = driver.find_element_by_id('pagelet_timeline_medley_friends')
#in this div search friends
usernames = html_list.find_elements_by_class_name('fsl')
print(len(usernames))

#extract the friend profile link for each person
link = driver.find_elements_by_class_name('_39g5') 

with open("LinkFriends.txt", 'w', newline='\n') as link_file:
    with open('YourFriends.txt', 'w', newline = '\n') as file:

        lista_link=[]
        for idx,name in enumerate(link):
            l = name.get_attribute('href')
            l = l[len(l)-7:]
            if l == "friends":
                lista_link.append( name.get_attribute('href') )
                link_file.write(name.get_attribute('href')+'\n')

        #we should drop the inactive's name, from our dict.... in this moment we drop only manually
        for name in usernames:        
            ins="Put-Your-Name-Here,"+name.text+'\n'
            file.write(ins)        

        #we execute again the main scrape
        i=0
        for name in lista_link:
            name = name+"_mutual"  #add in link /friend_MUTUAL!
            driver.get(name)
            pause_time = 1
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(pause_time)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            full_friend_usernames = []
            friends_usernames = []

            html_list = driver.find_element_by_id('pagelet_timeline_medley_friends')
            full_friend_usernames = html_list.find_elements_by_class_name('fsl')
            print(len(full_friend_usernames))

            for nome_amico in full_friend_usernames:
                friends_usernames.append(nome_amico.text )
                
            for nome in friends_usernames:
                list_nome1 = driver.find_elements_by_xpath("//*[@id='fb-timeline-cover-name']/a")
                list_nome1 = list_nome1[0].text
                ins=list_nome1+','+nome+'\n'
                file.write(ins)
            
            i+=1
            print(i)

driver.close()
driver.quit()

