from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json

def launch_facebook(url, chrome_profile):
	chrome_options = Options()
	chrome_options.add_argument(chrome_profile)
	chrome_options.add_argument('--profile-directory=Default')

	with Chrome(options=chrome_options) as driver:
		# Step 1: Go to mBasic Facebook and Login
		# driver.get("https://mbasic.facebook.com")
		
		# Step 2: Go to the URL
		driver.get(url)

		# Step 3: Get all article rows with beautifulsoup
		soup = BeautifulSoup(driver.page_source, "html.parser")
		posts = soup.find_all("div", {"class": "by di ds"})
		post_links = [x.get_attribute("href") for x in driver.find_elements_by_link_text("Full Story")]

		# Step 4: Go to EACH Post Detail and Grab their Content

		for i, d in enumerate(posts):
			# (user id, group id, etc etc)
			#TODO link post meta data and post content/comments
			post_meta_data = json.loads(d.get("data-ft"))

			# Step 4.1.a: Click "Full Story" in new tab
			full_story_link = driver.find_elements_by_link_text('Full Story')[i].send_keys(Keys.COMMAND + Keys.RETURN)
			driver.switch_to.window(driver.window_handles[-1])

			# Step 4.2: Grab content
			post_content = driver.find_elements_by_xpath("//*[@class='bx' or @class='bv']")

			# Step 4.3: Extract text and put into array
			post = [p.text for p in post_content]
			print(f'Post ID: {i}, Content: {post}')

			#TODO Step 4.4: Grab Comment

			driver.close()
			driver.switch_to.window(driver.window_handles[0])
			time.sleep(10)

		#TODO Add "Show More" posts logic

		return driver

def main():
	with open('mvars') as json_file:
		d = json.load(json_file)		
		url = d['url']
		chrome_profile = d['chrome_profile_dir'] # in order to avoid login whenever we start the script

	driver = launch_facebook(url, chrome_profile)
	

if __name__ == "__main__":
	main()