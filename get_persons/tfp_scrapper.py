
# coding: utf-8

# In[26]:


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import numpy as np
import os
from tqdm import tqdm_notebook as tqdm


# In[31]:


class the_famous_people_com_scrapper:
    def __init__(self):
        self.base_url="https://www.thefamouspeople.com/{}.php"
        self.countries_url=["pakistan","bangladesh","iraq","iran_islamic_republic","afghanistan","nepal","turkey","india"]
        self.countries=["pakistan","bangladesh","iraq","iran","afghanistan","nepal","turkey","india"]
        
        
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("— incognito")
        self.browser=webdriver.Chrome(executable_path="./chromedriver", chrome_options=self.option)
        self.columns=["name","occupation","dob","country"]
        self.results=None
        print (self.results)
        self.year_thresh=1930
        
    def get_query_url(self,country_url):
        return self.base_url.format(country_url)
    
    def load_country_page(self,country_url):
        url=self.get_query_url(country_url)
        self.browser.get(url)
        print ("loading page {} ...might take some time".format(url))
        view_button_element = self.browser.find_elements_by_xpath("//div[@class='loading-bar']")
        while view_button_element[0].is_displayed():
            view_button_element[0].click()
            time.sleep(1.5)
            view_button_element = self.browser.find_elements_by_xpath("//div[@class='loading-bar']")
    
    def extract_people_of_country(self,country,country_url):
        self.load_country_page(country_url)
        person_elements=self.browser.find_elements_by_class_name("catprofiles")
        person_list=[]
        for index,person_element in zip(tqdm(range(len(person_elements))),person_elements):
            person_element=person_element.find_element_by_tag_name("div")
            try:
                pe_name=person_element.find_element_by_tag_name("img").get_attribute("title").lower()
            except:
                pe_name=""
            try:
                pe_occupation=person_element.find_element_by_class_name("rec-country-name").text.lower().replace("(","").replace(")","")
            except:
                pe_occupation=""
            try:
                pe_dob=person_element.find_element_by_tag_name("p").text
                if len(pe_dob)>4:
                    year=pe_dob[-4:]
                    if not year.isdigit():
                        continue
                    elif int(year)<self.year_thresh:
                        continue
                else:
                    pe_dob=""
            except:
                pe_dob=""
#             print ("\t",index+1,pe_name,pe_occupation,pe_dob,country)
            person_list.append([pe_name,pe_occupation,pe_dob,country])
        print ("num of people extracted={}".format(len(person_list)))
        return person_list
            
    def extract_persons(self):
        for country,country_url in zip(self.countries,self.countries_url):
            print ("===>extracting for country {}".format(country))
            p_list=self.extract_people_of_country(country,country_url)
            if self.results is None:
                self.results=pd.DataFrame(p_list,columns=self.columns)
            else:
                self.results=self.results.append(pd.DataFrame(p_list,columns=self.columns),ignore_index=True)
#         print (self.results)
        return self.results
#         self.results.to_csv(self.savepath)
    


# In[32]:


# ps=the_famous_people_com_scrapper()
# person_df=ps.extract_persons()

