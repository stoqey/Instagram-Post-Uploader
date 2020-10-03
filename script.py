import json
import os
import requests
from PIL import Image
from instabot import Bot
from resizeimage import resizeimage
import random

import config

data = ''

# replace eg.json with your own file name
with open('eg.json', encoding='utf-8') as file:
    data = file.read()

json_data = json.loads(data)

bot = Bot()

bot.login(username=config.USERNAME,
          password=config.PASSWORD)

for j_data in json_data:
    caption = j_data['caption']

    for image_path in (j_data['images']):
        print("Caption:", caption)
        print(image_path)
        response = requests.get(image_path)
        filename = str(random.randint(0,10000)) + '.jpg'
        file = open(filename, "wb")
        file.write(response.content)
        file.close()
        fd_img = open(filename, 'rb')
        img = Image.open(fd_img)
        width, height = img.size
        # If image width is greater than 1080, just upload it
        if(width > 1080): 
          img = resizeimage.resize_crop(img, [width, width])
          img.save(filename, img.format)
          fd_img.close()
        #If image width is not equal to height crop image to match width x width(as height)
        if(width != height):
            size = width, width
            img = resizeimage.resize_crop(img, size)
            img.save(filename, img.format)
            fd_img.close()
        bot.upload_photo(filename, caption=caption)
        os.remove(filename+".REMOVE_ME")
    print()
