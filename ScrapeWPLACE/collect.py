import requests
import os
from PIL import Image
import json
width = 2002
height= 1024


width = 16
height = 16
image_url = "https://backend.wplace.live/files/s0/tiles/2002/1024.png"

data = []

colors = ["black","darkgrey","grey","lightgrey"]

#['match', ['get', 'color'], 'black', ' #000000', 'darkgrey', ' #3c3c3c', 'grey', ' #787878', 'lightgrey', ' #d2d2d2', 'white', ' #ffffff', 'darkredbrown', ' #600018', 'red', ' #ed1c24', 'orange', ' #ff7f27', 'lightorange', ' #f6aa09', 'yellow', ' #f9dd3b', 'offwhite', ' #fffabc', 'darkgreen', ' #0eb968', 'lightgreen', ' #13e67b', 'lightergreen', ' #87ff5e', 'darkergreen', ' #0c816e', 'greenblue', ' #10aea6', 'lightgreen1', ' #13e1be', 'darkblue', ' #28509e', 'lightblue', ' #4093e4', 'lighterblue', ' #60f7f2', 'bluepurple', ' #6b50f6', 'lighterpurple', ' #99b1fb', 'deeppurple', ' #780c99', 'darkpurple', ' #aa38b9', 'lightpurple', ' #e09ff9', 'darkrose', ' #cb007a', 'rose', ' #ec1f80', 'pink', ' #f38da9', 'darkbrown', ' #684634', 'brown', ' #95682a', 'lightbrown', ' #95682a', '#808080']
colors = ['black', 'darkgrey', 'grey', 'lightgrey', 'white', 'darkredbrown', 'red', 'orange', ' #ff7f27', 'lightorange', ' #f6aa09', 'yellow', ' #f9dd3b', 'offwhite', ' #fffabc', 'darkgreen', ' #0eb968', 'lightgreen', ' #13e67b', 'lightergreen', ' #87ff5e', 'darkergreen', ' #0c816e', 'greenblue', ' #10aea6', 'lightgreen1', ' #13e1be', 'darkblue', ' #28509e', 'lightblue', ' #4093e4', 'lighterblue', ' #60f7f2', 'bluepurple', ' #6b50f6', 'lighterpurple', ' #99b1fb', 'deeppurple', ' #780c99', 'darkpurple', ' #aa38b9', 'lightpurple', ' #e09ff9', 'darkrose', ' #cb007a', 'rose', ' #ec1f80', 'pink', ' #f38da9', 'darkbrown', ' #684634', 'brown', ' #95682a', 'lightbrown', ' #95682a', '#808080']
colors2 = []
for item in colors:
    if "#" not in item:
        colors2.append(item)
print(colors2)

colors = []



for x in range(width):
    for y in range(height):
        pass
locations = [(1024,1024)]
for x in range(width):
    for y in range(height):
        locations.append((x+1030,y+1030))

import tqdm
for x,y in tqdm.tqdm(locations):
    image_url = f"https://backend.wplace.live/files/s0/tiles/{x}/{y}.png"
    img_data = requests.get(image_url).content
    os.makedirs(f"data\{x}",exist_ok=True)
    with open(f'data\\{x}\\{y}.png', 'wb') as handler:
        handler.write(img_data)
    try:
        im = Image.open(f'data\\{x}\\{y}.png')
        for i in range(1000):
            for j in range(1000):
                x1 = i+((x)*1000)
                y1 = j+((y)*1000)
                index = (im.getpixel((i,j)))
                if index >= len(colors):
                    color = "None"
                else:
                    color = colors[index]
                data.append({"x":x1,"y":y1,"color":color})
        with open("output.json","w") as file:
            #file.write(json.dump(data))
            json.dump(data,file)
        print("SUCSSESS")
    except Exception as e:
        print(e)
                
                
