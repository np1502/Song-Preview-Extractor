#import json
import random
import sys
import urllib3
import urllib.request
from os.path import expanduser, join
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import time
import pandas

BASE_DIR = "E:\X_data"

user_details = [("devendrasaohisua@gmail.com","deadpool2")]

class Instagram_Reel():

	def __init__(self,username):
		super(Instagram_Reel,self).__init__()
		self.base_url = "https://www.instagram.com/"+username + "/"
		#self.cnt = 0
		self.check = {}
		#self.res_dict = {}
		#self.name = username

	def get_reels(self):
		
		driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
		driver.get(self.base_url)
		time.sleep(random.randint(4, 7))
		try:
			login_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button')
		except Exception as e:
			login_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button')
		login_button.click()
		time.sleep(random.randint(4, 7))
		user_curr = random.choice(user_details)
		email_button = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
		email_button.send_keys(user_curr[0])

		time.sleep(2)

		password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
		password.send_keys(user_curr[1])
		driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button").click()
		time.sleep(random.randint(4, 7))
		try:
			driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
		except Exception as e:
			driver.find_element_by_xpath('/html/body/div[1]/div/div/section/main/div/div/div/div/button').click()
		time.sleep(random.randint(4, 7))
		driver.get(self.base_url + "reels/")
		time.sleep(random.randint(4, 7))
		screen_height = driver.execute_script("return window.screen.height;")
		i = 1
		while True:
			database = pandas.read_csv("main_database.csv")
			reel_list = driver.find_elements_by_xpath('//div[@class ="Tjpra"]//a')
			#print(len(reel_list))  
			reel_list = [reel.get_attribute('href') for reel in reel_list]
			reel_list = [link for link in reel_list if link not in self.check]
			for link in reel_list:
				self.check[link] = 1
				driver.get(link)
				time.sleep(random.randint(4,6))
				try:
					music_details = driver.find_element_by_class_name("_4lIW3").text
				except Exception as e:
					continue
				music_details = music_details.split('•')
				if(len(music_details)==2 and music_details[1]!="Original Audio" and music_details[1] not in database["Song Name"].values):
					curr_df = pandas.DataFrame(columns = ["Artist","Song_Name","URI_Link","Reel_Cnt","Reel_Link"])
					audio_link = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/div[1]/article/header/div[2]/div[2]/a').get_attribute('href')
					driver.get(audio_link)
					time.sleep(random.randint(4,6))
					reel_cnt = driver.find_element_by_xpath('//div[@class = "_7UhW9    vy6Bb    yUEEX   KV-D4          uL8Hv         "]').text.split(' ')[0]
					
					audio_dl = driver.find_element_by_xpath('//audio').get_attribute('src')
					filename = music_details[1].split('(')[0] + ".mp3" 
					save_file = join(BASE_DIR,filename)
					urllib.request.urlretrieve(audio_dl,save_file)
					curr_df.loc[0] = [music_details[0],music_details[1],filename,reel_cnt,link]
					with open("main_database.csv","a") as f:
						curr_df.to_csv(f,header=False,index=False)
			driver.get(self.base_url + "reels/")
			time.sleep(random.randint(4, 7))
			for val in range(i):
				driver.execute_script("window.scrollTo({screen_height}*{val_a}, {screen_height}*{val_b});".format(screen_height=screen_height, val_a=val,val_b = val + 1))
				time.sleep(2)
			i += 1
			scroll_height = driver.execute_script("return document.body.scrollHeight;") 
			if (screen_height) * i > scroll_height:
				break
			
		driver.close()
		return 0

user_obj = Instagram_Reel('*account-name*')
user_obj.get_reels()


## converting reels count to decimal values

db = pandas.read_csv("main_database.csv")

for i,s in enumerate(db["Reel_Usage"].values):
    if(isinstance(s,str)):
        if(s[-1]=='K'):
            s=s[:-1]
            s=float(s)*1000
        elif(s[-1]=='M'):
            s=s[:-1]
            s=float(s)*1000000
    db.iloc[i,3]=s


db.to_csv('data.csv')

def download_y(df,session_id):
  for row in df.iterrows():
    file = row[1]["URI_Path"]
    drive_file = os.path.join("/content/gdrive/MyDrive/music_data_X",file)
    save_file = os.path.join("/content/gdrive/MyDrive/music_data_y",file)
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            "cookie":f'sessionid={session_id};'
    }
    reel_curr = Reel(row[1]["Reel_Link"])
    reel_curr.scrape(headers = headers)
    reel_link = reel_curr.video_url
    urllib.request.urlretrieve(reel_link,"reel.mp4")
    clip = mp.VideoFileClip("reel.mp4")
    clip.audio.write_audiofile(save_file)

download_y(data,"19723161168%3AEtZGGPeuCrLFhC%3A4")