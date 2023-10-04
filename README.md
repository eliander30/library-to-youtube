# library-to-youtube
Script that download audios from library and generate video with images and audios then upload to youtube.

1- Extract the zip file

2- Install ffmpeg en linux (apt install ffmpeg)

3- Install pip3 en linux (apt install python3-pip)

4- Move to the folder where zip file was extracted and run the following command (pip3 install -r requirements.txt)

5- Localize where was installed the selenium_firefox module (cd / && locate firefox.py) and copy the path

6- Now edit the file firefox.py in the path we localized in the step 5 (remove all its content and replace the content 
of the firefox.py with the content of the firefox file inside the folder where the zip was extracted)

7- Open firefox, and open your youtube account, then go to Menu>help>More Troubleshooting information and localize where say profile path and copy it.

8- Now go to the firefox.py in the path we located in step 5 and open the file to edit and search for 
line 39 where say profile_new_path = '/home/eliander/.mozilla/firefox/o1r8934p.hola' and replace with the path u got from firefox in step 7.

the script should be setup and ready for run (python3 downupvideo.py)

#NOTE: Make sure u have google-chrome and firefox installed.

#NOTE: to change playlist title, find the file Constant.py under the folder "youtube_uploader_selenium" that is inside the folder
where all the files of the scripts were extracted. Change the value of variable "VIDEO_PLAYLIST" in the file Constant.py for example
VIDEO_PLAYLIST = 'playlist-example-title' and save the file.
