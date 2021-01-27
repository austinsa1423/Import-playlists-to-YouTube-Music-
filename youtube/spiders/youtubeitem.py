'''-------------------------------------------------------------------------------------------------'''
### Yeah yeah, I know this is over engineered and there is a lot of pointless libs and code and that I wrote this in 2.7 in 2021. Its a 
### stripped down modified version of a old larger one and it works. 
### 
### All click actions are based on full XPaths since it seemed to get confused unless they were full ones. If it seems to not be 
### adding the songs to the playlist, update the XPaths where it seems to be getting stuck
'''-------------------------------------------------------------------------------------------------'''
import scrapy, time, re, datetime, os, json, io
from urlparse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class YoutubeitemSpider(scrapy.Spider):
	name = 'youtubeitem'

	def __init__(self):
		self.playlist = []
		self.count = 0
	
	def __del__(self):
		self.driver.quit()

	def start_requests(self):
		# Start Chrome
		options = webdriver.ChromeOptions()

		# In chrome go to chrome://version/ and paste your Profile path but remove the "default" at the end. I built this on windows and did not try it on any other OS so🤷‍♀️
		# Ex. C:\\Users\\AustinsTotallyAwesomePC\\AppData\\Local\\Google\\Chrome\\User Data
		options.add_argument("user-data-dir=<<enter chrome profile path here>>")
		# make sure the chrome driver version matches that of the chrome installed on your computer. 
		self.driver = webdriver.Chrome(executable_path="C:\\Python27\\chromedriver.exe", chrome_options=options)

		# Read in JSON lines from text file. Make sure that one playlist is on one line. Ex. {"playlist": "Normal songs I am comfortable sharing with people", "songs": [" ", " "]}
		with open('youtube\\playlists.json', 'r') as file:
			for line in file:
				self.playlist.append(line)
		print self.playlist
		# Reads linkfile for links to scrape
		for playlist in self.playlist:
			yield scrapy.Request("https://music.youtube.com/library/playlists", callback=self.parse)



	def parse(self, response):
		# This value sets up what playlist in the JSON you are starting one. 1 to start at the top
		#self.count = self.count + 3
		failed = []

		# Since this is a Google thing and people have 2 factor auth. You need to manually login. Going through a Google app, it does not like letting you in so we sign in through stackoverflow. Once fully signed in hit something to continue
		self.driver.get("https://music.youtube.com/")
		raw_input("Confirm that you are logged into YouTube Music and on the home page. Press Enter to continue...")

		# We will sit in here the rest of the program
		# Loops through all of the playlists in the file that were read in earlier
		while self.count < len(self.playlist):
			j = json.loads(self.playlist[self.count])
			self.count = self.count + 1
			print ""
			print j["playlist"]
			print j["songs"]
			print ""
			# Here we create the playlist 
			self.driver.get("https://music.youtube.com/library/playlists")
			time.sleep(5)
			self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-browse-response/ytmusic-section-list-renderer/div[2]/ytmusic-item-section-renderer/div[3]/ytmusic-grid-renderer/div[2]/ytmusic-two-row-item-renderer[1]/a/ytmusic-thumbnail-renderer/yt-img-shadow/img').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('/html/body/ytmusic-dialog/paper-dialog-scrollable/div/div/ytmusic-playlist-form/iron-pages/div[1]/div[1]/paper-input/paper-input-container/div[2]/div/iron-input/input').send_keys(j["playlist"])
			self.driver.find_element_by_xpath('/html/body/ytmusic-dialog/paper-dialog-scrollable/div/div/ytmusic-playlist-form/iron-pages/div[1]/div[2]/paper-button[2]').click()
	
			# Here we click on the search bar so we can type in it
			self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/paper-icon-button[1]').click()
			time.sleep(1)

			# Loops through all of the songs that are in the playlist and adds them to it
			for song in j["songs"]:
				# Clear type song and search
				self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input').clear()
				time.sleep(1)
				self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input').send_keys(song)
				time.sleep(1)
				self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input').send_keys(Keys.RETURN)
	
				time.sleep(3)
	
				# Song Name
				temp = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/div[2]/div[1]/yt-formatted-string').text
				# try excpet for unicode errors that are infrequent enough for me to not car to fix
				# any songs that failed are added to the list and printed at the end of each loop
				try:
					print temp
					print song
					print temp in song

					# Check if the first song is a match for the one from the file
					if temp in song:
						print "first result matched"
						element_to_hover_over = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/div[2]/div[1]/yt-formatted-string')
						hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
						hover.perform()
						time.sleep(1)
						self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/ytmusic-menu-renderer/paper-icon-button/iron-icon').click()
					else:
						temp = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[2]/div[2]/ytmusic-responsive-list-item-renderer[1]/div[2]/div[1]/yt-formatted-string').text
						print temp in song
						# check if the second one is a match 
						if temp in song: 
							print "second result matched"
							element_to_hover_over = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[2]/div[2]/ytmusic-responsive-list-item-renderer[1]/div[2]/div[1]/yt-formatted-string')
							hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
							hover.perform()
							time.sleep(1)
							self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[2]/div[2]/ytmusic-responsive-list-item-renderer[1]/ytmusic-menu-renderer/paper-icon-button/iron-icon').click()
						# screw it and just use the first one since that is what youtube thinks is right
						else:
							print "reverting to first result"
							element_to_hover_over = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/div[2]/div[1]/yt-formatted-string')
							hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
							hover.perform()
							time.sleep(1)
							self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/ytmusic-menu-renderer/paper-icon-button/iron-icon').click()
					
					# Click add song to playlist. Iterate through the pop up to find the right button. It likes to move sometimes
					k = 1
					while True:
						buttonName = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-popup-container/iron-dropdown[1]/div/ytmusic-menu-popup-renderer/paper-listbox/ytmusic-menu-navigation-item-renderer[%s]/a/yt-formatted-string' %k).text
						print buttonName
						if "Add to playlist" == buttonName.strip():
							self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-popup-container/iron-dropdown/div/ytmusic-menu-popup-renderer/paper-listbox/ytmusic-menu-navigation-item-renderer[%s]/a' %k).click()
							break
						else:
							k = k + 1		
					i = 1

					# Find the correct playlist to add to 
					while True:
						time.sleep(1)
						playlistName = self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-popup-container/iron-dropdown[2]/div/ytmusic-add-to-playlist-renderer/div[2]/div[2]/ytmusic-playlist-add-to-option-renderer[%s]/button/div/yt-formatted-string' %i).text
							  
						print playlistName
						print j["playlist"]
						if playlistName.strip()	== j["playlist"].strip():
							print "added"
							self.driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-popup-container/iron-dropdown[2]/div/ytmusic-add-to-playlist-renderer/div[2]/div[2]/ytmusic-playlist-add-to-option-renderer[%s]/button/div/yt-formatted-string' %i).click()
							break
						else:
							print "wrong playlist"
							i = i + 1
						time.sleep(2)
				except:
					# adds songs that are honest failures
					failed.append(song)
				print ""
				print "Failed"
				print failed