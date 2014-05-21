#!/usr/bin/env python

import urllib2
import logging
import sys
from bs4 import BeautifulSoup
import time
import re

# loggin parameters
logger = logging.getLogger("main.py")
logger.setLevel(logging.INFO)
# create a file handler
log_file = "main.log"
handler = logging.FileHandler(log_file)
# handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

topLevelUrl = "http://192.168.1.1"
username = ""
password = ""

passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm() 
passwordManager.add_password(None, topLevelUrl, username, password)
handler = urllib2.HTTPBasicAuthHandler(passwordManager) 

try:
	handler = urllib2.HTTPBasicAuthHandler(passwordManager)
	opener = urllib2.build_opener(urllib2.HTTPHandler, handler)
	urllib2.install_opener(opener)

	response = urllib2.urlopen(topLevelUrl + "/Action?reboot_loc=0&id=5&cmdReboot=Reboot")

	log = "Restarting the modem ..."
	logger.info(log)
	log = "sleeping for 1 minute 40 seconds ..."
	logger.info(log)
	time_to_wait = 100
	
	time.sleep(time_to_wait)
		

	count = 0
	while (count < 3):
		try:
			response = urllib2.urlopen(topLevelUrl + "/MainPage?id=6") # main page
		except Exception,e:
			log = "Exception when checking if router is up, Error: " + str(e)
			logger.error(log)

		if(response.code == 200):
			log = "Checking Router Status, HTTP Response : 200"
			logger.info(log)
			bs = BeautifulSoup(response)

			table = bs.find("table", {"class" : "mainContentTable"})
			row = table.findAll('tr')

			# to find uptime
			uptime = row[4].findAll('td')[1].string
			# to find if router is up
			green_led = row[13].findAll('td')[5].find("img")['src']

			log = "Up time : " + str(uptime)
			logger.info(log)
			
			regexp = re.compile(r'hag/images/greenled.gif')

			if regexp.search(green_led) is not None:
				log = "Router has green status\t EXITING"
				logger.info(log)
				break
			else:
				log = "Router hasnt connected to the net yet"
				logger.warning(log + "\tSTATUS:" + green_led)

		else:
			log = "Got Invalid code, HTTP code : " + str(response.code)
			logger.warning(log)

		count = count + 1
		log = "count :" + str(count)
		logger.warning(log)

		log = "sleeping for 1 minute ..."
		logger.info(log)
		time.sleep(60)



except Exception,e:
	log = "Could not restart the modem\nError : " + str(e)
	logger.error(log)