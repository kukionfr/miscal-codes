# coding=utf-8

import os
# data processing
import pandas as pd
# selenium main
from selenium import webdriver
# selenium error handling
from selenium.common.exceptions import NoSuchElementException
# selenium explicit wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# python libraries
from time import sleep

# Kyu Sang Han
# PhD Candidate, Johns Hopkins University
# khan21@jhu.edu

chromedriver= r"C:/Users/kuki/Desktop/Desktop/search_store/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver)
# Fetch a webpage
driver.get('http://gs25.gsretail.com/gscvs/ko/store-services/locations#')
addresses=[]
# desktop =  os.path.join(os.environ["HOMEPATH"], "Desktop")
df1 = pd.read_excel("input.xlsx", index_col=None, na_values=['NA'],usecols="A",header=None)

keywords = map(unicode,df1[0])
keywords = [s + u'점' for s in keywords]

#keywords = [u'시흥점'] #2ea
#keywords = [u'연수청학점'] #1ea
#keywords = [u'주안주공점'] #nothing
i=1
for keyword in keywords:
	print i
	driver.find_element_by_name('stb4').clear()
	search = driver.find_element_by_name('stb4')
	search.send_keys(keyword)

	sleep(2) #give time to generate click button
	button = driver.find_element_by_xpath('//*[@id="searchButton"]')
	button.click()

	sleep(2) #give time to update address
	# no address error handling
	try: #if there is no 2nd address
		res = driver.find_element_by_xpath('//*[@id="storeInfoList"]/tr[2]/td[2]/a')

		storename1 = driver.find_element_by_xpath('//*[@id="storeInfoList"]/tr[1]/td[1]/a')
		storename2 = driver.find_element_by_xpath('//*[@id="storeInfoList"]/tr[2]/td[1]/a')

		searchword = keyword.encode('utf8')
		storename1= storename1.text.encode('utf8')[4:]
		storename2= storename2.text.encode('utf8')[4:]

		if searchword == storename2:
			print 'second one matches'
			address = res.text.encode('utf8')
		else: raise NoSuchElementException
	except NoSuchElementException:
		try: #then first one is the correct address
			print 'first one matches'
			res = driver.find_element_by_xpath('//*[@id="storeInfoList"]/tr[1]/td[2]/a')
			address= res.text.encode('utf8')
		except NoSuchElementException: #it's possible that there is no address 
			print 'nothing'
			address = 'NA'

	addresses.append(address)
	i=i+1

d={'address':addresses}
df = pd.DataFrame(data=d)
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
