#! /usr/bin/python3
import os
from instalooter.looters import ProfileLooter
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def scrolldown():
	webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
	time.sleep(1)
	webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
	time.sleep(1)
	print(len(driver.find_elements_by_tag_name("li")))
	return len(driver.find_elements_by_tag_name("li"))

username_ = input("Please Input Username: ").strip()
password_ = getpass.getpass("Please Input Password: ").strip()


# Optional argument, if not specified will search path.

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
# driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.instagram.com/accounts/login/')
# time.sleep(5) # Let the user actually see something!
username_box = driver.find_element_by_name('username')
username_box.send_keys(username_)
password_box = driver.find_element_by_name('password')
password_box.send_keys(password_)


password_box.submit()
time.sleep(5)
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
link = driver.find_element_by_link_text('Profile')
link.click()
time.sleep(3)
links = driver.find_elements_by_tag_name('a')
for i in links:
	if 'following' in i.get_attribute('href'):
		print(i.get_attribute('href'))
		i.click()
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()

asdf = len(driver.find_elements_by_tag_name("li"))
asdfprevious = -1
print(asdf, asdfprevious)
while (asdf != asdfprevious):
	asdfprevious = asdf
	asdf = scrolldown()
	print(asdf, asdfprevious)
followinglist = []
atext = driver.find_elements_by_xpath("//li/div/div/div/div/a")
img=driver.find_elements_by_xpath("//a/img")

for i in atext:
	print(i.text)
	followinglist.append(i.text)
ThumbsFilePath='./thumbs/'
if not os.path.exists(ThumbsFilePath):
    os.makedirs(ThumbsFilePath)
UserFilePath='./users/'
if not os.path.exists(UserFilePath):
	os.makedirs(UserFilePath)
img_src=[]
for i in range(0,len(img)):
	img_src.append(img[i].get_attribute('src'))
	print(img_src)
	os.system('wget -q -O '+ThumbsFilePath+followinglist[i]+'.jpg '+img_src[i]+' &')
driver.quit()
looter=ProfileLooter("instagram")
looter.login(username_,password_)
for i in followinglist:

	print(i)
	i = i.strip()
	looter=ProfileLooter(i)
	for media in looter.medias():

		if media['is_video']:
			pass
			# print(media)
			# url = looter.get_post_info(media['code'])['video_url']
		else:
			# print(media)
			url = media['display_url']
		# print(url)
		if url.strip()[-2:] != '.1':
			with open(UserFilePath+i, "a") as output:
				output.write("{}\n".format(url))
	time.sleep(2.5)
	os.system('wget -q -i '+UserFilePath+i+' -P '+UserFilePath+i+' &')
