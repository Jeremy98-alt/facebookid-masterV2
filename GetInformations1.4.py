from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import gender_guesser.detector as gender  #for guessing a gender of a person
import json
import time

#extract his city
def catch_city(x, file):
    word_to_find = "Vive a"
    city = ''
    if word_to_find in x[0]:
        city = x[0].replace('Vive a ', '')
        file.write(','+city)
    return city

def catch_birthday(x, file):
    birthday = ''
    if x[0] == "Data di nascita":
        birthday = x[1]
        file.write(','+birthday)
    return birthday         

#extract his school/university
def catch_school(x, file):
    word_to_find = ["studiato","Studia", "Frequenta", "frequentato"]
    school = ''
    if any(wtf in x[0] for wtf in word_to_find):
        l = list(x[0].split())

        if l[0] == "Studia" or l[1] == "studiato":
            num_presso = l.index("presso")+1
        
        if l[0] == "Frequenta":
            num_presso = l.index("Frequenta")+1
        
        if l[1] == "frequentato":
            num_presso = l.index("frequentato")+1

        for w in range(num_presso, len(l)):
            if w == len(l)-1:
                school += l[w]
            else:
                school += l[w] +" " 
        file.write(','+school)
    return school

#gender for recognition if its male or female, andy(if i can't establish it), unknown(name not found)
def catch_genre(name, file):
    d = gender.Detector() 
    if d.get_gender(name) == "male":
        genre = "maschio"
    elif d.get_gender(name) == "female":
        genre = "femmina"
    else:
        genre = "maschio"
    
    file.write(genre)
    return genre


def extract_features():
    html_div_info = driver.find_element_by_id('pagelet_timeline_medley_about') #this is the main div where you can extract informations
    informations = html_div_info.find_elements_by_class_name('_c24')  #these elements are inside the div, i should parse the information

    with open('FriendFeatures.text', 'a', newline='\n') as file:
        your_name = driver.find_elements_by_xpath("//*[@id='fb-timeline-cover-name']/a")
        name = your_name[0].text
        file.write(name+',')

        genre = catch_genre(name.split()[0], file)

        flg = 0
        for info in informations:
            x = list(info.text.splitlines())
            
            school = catch_school(x, file)
            city = catch_city(x, file)
            birthday = catch_birthday(x, file)

            #fake controlls, for reducing the unnecessary info like number family, residence's address, date of birth (we want only the date!)
            list_ = ['familiari', 'Indirizzo', 'Data di nascita']
            if any(word in x[0] for word in list_):
                print(x[0] + " selected")
                flg=1
            
        file.write('\n')

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

extract_features()

f = open("LinkFriends.txt", "r")
f1 = f.readlines() #for each line
for x in f1:
    driver.get(x)
    about = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[2]/div[3]/ul/li[2]/a').click()
    time.sleep(3)
    extract_features()

driver.close()
driver.quit()

