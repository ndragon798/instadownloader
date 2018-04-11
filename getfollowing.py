#! /usr/bin/python3
import os
import time
import getpass
from instalooter.looters import ProfileLooter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def instalinks(media, looter):
    if media.get('__typename') == "GraphSidecar":
        media = looter.get_post_info(media['shortcode'])
        nodes = [e['node'] for e in media['edge_sidecar_to_children']['edges']]
        return [n.get('video_url') or n.get('display_url') for n in nodes]
    elif media['is_video']:
        media = looter.get_post_info(media['shortcode'])
        return [media['video_url']]
    else:
        return [media['display_url']]


def scrolldown():
	webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
	time.sleep(1)
	webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
	time.sleep(1)
	# print(len(driver.find_elements_by_tag_name("li")))
	return len(driver.find_elements_by_tag_name("li"))
#Read in username and password for instagram
username_ = input("Please Input Username: ").strip()
password_ = getpass.getpass("Please Input Password: ").strip()


# Optional argument, if not specified will search path.
#Setup headless chrome for selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
#Load login page
driver.get('https://www.instagram.com/accounts/login/')
# Type in login 
username_box = driver.find_element_by_name('username')
username_box.send_keys(username_)
password_box = driver.find_element_by_name('password')
password_box.send_keys(password_)
password_box.submit()

#Wait for login
time.sleep(5)
#Close popup
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#Go to profile
link = driver.find_element_by_link_text('Profile')
link.click()
time.sleep(3)
# Open following tab
links = driver.find_elements_by_tag_name('a')
for i in links:
	if 'following' in i.get_attribute('href'):
		print(i.get_attribute('href'))
		i.click()
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
#Find inital amount of loaded following
asdf = len(driver.find_elements_by_tag_name("li"))
asdfprevious = -1
print(asdf, asdfprevious)
#Scroll all the way down the following list
while (asdf != asdfprevious):
	asdfprevious = asdf
	asdf = scrolldown()
	print(asdf, asdfprevious)
followinglist = []
#Grab all user names and images
atext = driver.find_elements_by_xpath("//li/div/div/div/div/a")
img=driver.find_elements_by_xpath("//a/img")

for i in atext:
	print(i.text)
	followinglist.append(i.text)

#Create thumbs and users directories
ThumbsFilePath='./thumbs/'
if not os.path.exists(ThumbsFilePath):
    os.makedirs(ThumbsFilePath)
UserFilePath='./users/'
if not os.path.exists(UserFilePath):
	os.makedirs(UserFilePath)
img_src=[]
#Grab all the thumbnails
for i in range(0,len(img)):
	img_src.append(img[i].get_attribute('src'))
	# print(img_src)
	os.system('wget -q -O '+ThumbsFilePath+followinglist[i]+'.jpg '+img_src[i]+' &')

#Close selenium
driver.quit()
#Login into instagram
looter=ProfileLooter("instagram")
looter.login(username_,password_)
followinglist=['katie_len22']
#Loop through all the people who are being followed and grab their photo urls
for i in followinglist:

	print(i)
	i = i.strip()
	looter=ProfileLooter(i)
	with open(UserFilePath+i, "a") as output:
		for media in looter.medias():
			for link in instalinks(media,looter):
				print(link)
				output.write("{}\n".format(link))
	#Try and not get rate limited by instagram
	time.sleep(4)
	#Wget from the file
	os.system('wget -q -i '+UserFilePath+i+' -P '+UserFilePath+i+' &')
