from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from youtube_uploader_selenium import YouTubeUploader
from datetime import datetime, timedelta
import csv
import requests
import time
import os
import json

items_list = []

items = "items.csv"

check_if_exist = os.path.exists(items)

if check_if_exist == False:
	os.system("touch items.txt")
else:
	file_items = open('items.txt')
	reader_obj = file_items.readlines()
	for row in reader_obj:
		cleaned_row = str(row).strip("\n")
		items_list.append(cleaned_row)	

# Initialize Chrome driver instance
options = Options()

#options.add_argument('--headless=new')

driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)

# Navigate to the url
driver.get('https://www.loc.gov/search/?fa=online-format%3Aaudio&sb=date&dates=1902&st=list&c=900')



content = driver.find_elements(By.CLASS_NAME, 'item-description')

titles = []
links = []


for con in content:
	element = con.find_element(By.TAG_NAME, 'a')
	print("title: " + element.text)	
	titles.append(element.text)
	link = element.get_attribute('href')
	print("link: " + link)
	links.append(link)
	description = con.find_element(By.CLASS_NAME, 'item-description-abstract').text
	print("description: " + description)
#	f = open('items.csv', 'a')
#	writer = csv.writer(f)
#	writer.writerow([element.text, description])
	

# Close the driver

counter = 0
number = 1
number2= 3
incremental = 0
hour = ["16:00","12:00"]
now = datetime.now()
cleantime = datetime.strftime(now, "%m/%d/%Y")
uva = cleantime
for ln in links:
	if counter <= 25:
		metadata_dict = {"title": "Example title video","description": "Example Description for video","tags": ["1901", "vinyl", "vinylcollection", "Gramophone", "Nostalgia", "Early1900sMusic"],"schedule": "09/26/2023, 00:00"}
		if number < 1:
			number = number + 1
		else:
			number = 0
		if number2 < 2:
			number2 = number2 + 1
		else:
			uva = datetime.strftime(datetime.strptime(cleantime, "%m/%d/%Y") + timedelta(days=incremental), "%m/%d/%Y")
			incremental = incremental + 1
			number2 = 1
		thetimedate = str(uva) + ", " + str(hour[number])
		metadata_dict["schedule"] = thetimedate
		print(str(uva) + " " + str(incremental))
		driver.get(ln)
		title = driver.find_element(By.XPATH, "/html/body/div/div[2]/main/div[1]/h1/cite").text
		#descrip = driver.find_element(By.CLASS_NAME, 'about-this-item-content').text
		datevar = driver.find_element(By.XPATH, "/html/body/div/div[2]/main/div[3]/div/div[1]/div/ul[3]/li").text
		print(title)
		cleaned_title = title.strip()
		if cleaned_title in items_list:
			continue
		else:
			time.sleep(5)
			link_file = driver.find_element(By.XPATH, '/html/body/div/div[2]/main/div[2]/div/div/div/div[1]/div/div/div[1]/mediaelementwrapper/audio')
			link_audio = link_file.get_attribute('src')
			print(link_audio)
			response = requests.get(link_audio)
			title2 = str(title.replace(' ', '_')).replace(",", '')
			filename = str(title2.replace("'",'')) + ".mp3"
			print(filename)
			open(filename, "wb").write(response.content)
			filename_nonoise = "noise_" + filename
			remove_noise = "ffmpeg -i " + filename + " -af arnndn=m=cb.rnnn " + filename_nonoise
			os.system(remove_noise)
			filename_rise_vol = "vol_" + filename_nonoise
			rise_volume = "ffmpeg -i " + filename_nonoise + " -af 'volume=3.5' " + filename_rise_vol
			os.system(rise_volume)
			image_name = ""
			thumbnail_image = ""
			try:
				theelem = driver.find_element(By.XPATH, '/html/body/div/div[2]/main/div[2]/div[2]/div/figure/div/a/img')
				link_image = theelem.get_attribute('src')
				print("link of image: " + link_image)
				response2 = requests.get(link_image)
				image_name1 = title2.replace("'",'') + ".jpg"
				open(image_name1, "wb").write(response2.content)
				temp_name = "new_" + image_name1
				temp_thumbnail = "temp_" + image_name1
				scale_image = "convert " + image_name1 + " -resize 1080x1080 " + temp_name
				os.system(scale_image)
				scale_to_thumbnail = "convert " + image_name1 + " -resize 720x720 " + temp_thumbnail
				image_name = "fixed_" + temp_name
				os.system(scale_to_thumbnail)
				combine_image = "convert -composite -gravity center background.jpg " + temp_name + " " + image_name
				os.system(combine_image)
				combine_thumbnail = "convert -composite -gravity center thumbnail_background.jpg " + temp_thumbnail + " " + "fixed_" + temp_thumbnail
				os.system(combine_thumbnail)
				thumbnail_image = "fixed_" + temp_thumbnail
			except:
				image_name = "default.jpg"
				thumbnail_image = "default_thumbnail.jpg"
		#	input_still = ffmpeg.input("default.jpg")
		#	input_audio = ffmpeg.input(filename)
			cmd = "ffmpeg -loop 1 -framerate 1 -i " + image_name + " -i " + filename_rise_vol + " -map 0 -map 1:a -c:v libx264 -preset ultrafast -tune stillimage -vf fps=10,format=yuv420p -c:a copy -shortest " + title2.replace("'",'') + ".mp4"
			print("Generating video: " + title2.replace("'",'') + ".mp4" + " aspect ratio 16:9")
			os.system(cmd)
			metadata_dict['title'] = str(cleaned_title + ", " + " #1901 #Early1900sMusic")
			metadata_dict['description'] = str("#vinyl, #vinylcollection, #vinylcollector, #1901, #vinylcollective, #VintageMusic #VinylRecords #Early1900sMusic #1920sMusic #Nostalgia #MusicHistory #RetroSounds #OldTimeMusic #Gramophone #RecordPlayer #VintageVibes #LostInTime #ThrowbackTunes #ClassicSounds #GoldenEraMusic #TimelessMelodies #MusicalHeritage #HistoricalRecordings #AnalogMusic vinyl community,vinyl,1901,vinyl records,ASMR,Gramophone,VintageVibes,vinyl ASMR,vinyl collection,vinyl collector,vinyl record collection,record collection,1900,vinyl music store,free to use music,cc0 music,free music no copyright,film,sound ai stock,vintage sample pack")
			jsonfilename = title2.replace("'",'') + ".json"
			videofilename = title2.replace("'",'') + ".mp4"
			json_file = open(jsonfilename, "w")
			json.dump(metadata_dict, json_file)
			json_file.close()
			print(videofilename + " " + jsonfilename + " " + thumbnail_image)
			time.sleep(5)
			uploader = YouTubeUploader(videofilename, jsonfilename, thumbnail_image)
			was_video_uploaded, video_id = uploader.upload()
			assert was_video_uploaded
			counter = counter + 1
			file_titles = open("items.txt", "a")
			file_titles.write(cleaned_title + "\n")
			file_titles.close()
		#	ffmpeg.concat(input_still, input_audio, v=1, a=1).output(title2.replace("'",'') + ".mp4").run(overwrite_output=True)
	else:
		break


driver.quit()



