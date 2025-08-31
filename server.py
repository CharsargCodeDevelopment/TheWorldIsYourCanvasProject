import flask
from flask import render_template
from flask import Flask
import json


app = Flask(__name__)



"""
{
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [0, 0],
                                [0, 10],
                                [10, 10],
                                [10, 0],
                                [0, 0] // Close the polygon
                            ]
                        ]
                    },
                    'properties': {
                        'color': '#0080ff' // Blue
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [15, 5],
                                [15, 15],
                                [25, 15],
                                [25, 5],
                                [15, 5] // Close the polygon
                            ]
                        ]
                    },
                    'properties': {
                        'color': '#ff0000' // Red
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [-10, -5],
                                [-10, -15],
                                [-20, -15],
                                [-20, -5],
                                [-10, -5] // Close the polygon
                            ]
                        ]
                    },
                    'properties': {
                        'color': '#00ff00' // Green
                    }
                }
            ]
        };
"""
def GenerateFeature(coordinates = [],color = None):
    properties = {'color':'#0080ff'} # Blue
    properties = {'color':'blue'} # Blue
    """
    if color == None:
        color = '#0080ff'
    if "#" in color:
        properties = {'color':color} 
    else:
        r,g,b = color
        color = '#%02x%02x%02x' % (r,g,b)
        properties = {'color':color} # Blue
    """
    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])
    geometry = {'type': 'Polygon','coordinates':[coordinates]}
    feature = {"type":"Feature","geometry":geometry,"properties":properties}
    #feature = {"type":"Feature","geometry":geometry}
    return feature

def ConvertColorToHex(color=None):
    
    if color == None:
        color = '#0080ff'
    if "#" in color:
        return color
    else:
        r,g,b = color
        color = '#%02x%02x%02x' % (r,g,b)
    return color

def DrawPixels(pixels,size = 0.0001757812499931788*1):
    featureCollection = {'type': 'FeatureCollection','features':[]}
    print("drawing")
    for x,y,color in pixels:
        #x*=size
        #y*=size
        coordinates = [[x,y],[x,y+size],[x+size,y+size],[x+size,y]]
        feature = GenerateFeature(coordinates,color = (255,0,0))
        featureCollection["features"].append(feature)
    print("Done drawing")
    return featureCollection


def GetColorLibrary(name = "internal"):
    colors = ['match',['get', 'color']]
    if name == "internal":
        #colors.extend(["red",ConvertColorToHex((255,0,0))])
        #colors.extend(["blue",ConvertColorToHex((0,0,255))])
        colors.extend(["black"," #000000"])
        colors.extend(["darkgrey"," #3c3c3c"])
        colors.extend(["grey"," #787878"])
        colors.extend(["lightgrey"," #d2d2d2"])
        colors.extend(["white"," #ffffff"])


        colors.extend(["darkredbrown"," #600018"])
        colors.extend(["red"," #ed1c24"])
        colors.extend(["orange"," #ff7f27"])
        colors.extend(["lightorange"," #f6aa09"])
        colors.extend(["yellow"," #f9dd3b"])

        colors.extend(["offwhite"," #fffabc"])
        colors.extend(["darkgreen"," #0eb968"])
        colors.extend(["lightgreen"," #13e67b"])
        colors.extend(["lightergreen"," #87ff5e"])
        colors.extend(["darkergreen"," #0c816e"])

        colors.extend(["greenblue"," #10aea6"])
        colors.extend(["lightgreen1"," #13e1be"])
        colors.extend(["darkblue"," #28509e"])
        colors.extend(["lightblue"," #4093e4"])
        colors.extend(["lighterblue"," #60f7f2"])

        colors.extend(["bluepurple"," #6b50f6"])
        colors.extend(["lighterpurple"," #99b1fb"])
        colors.extend(["deeppurple"," #780c99"])
        colors.extend(["darkpurple"," #aa38b9"])
        colors.extend(["lightpurple"," #e09ff9"])

        colors.extend(["darkrose"," #cb007a"])
        colors.extend(["rose"," #ec1f80"])
        colors.extend(["pink"," #f38da9"])
        colors.extend(["darkbrown"," #684634"])
        colors.extend(["brown"," #95682a"])

        colors.extend(["lightbrown"," #95682a"])

        
        


        
        colors.append('#808080')
    print(colors)
    return colors

def LoadPixels():
    with open('wplace.json') as json_data:
        d = json.load(json_data)
        #print(d)
    size = 0.0001757812499931788
    pixels = []
    print("TESTING123")
    i = 0
    for item in d:
        i+=1
        if i > 100:
            return pixels
        x,y = 0,0
        color = ""
        
        if "long" in item:
            x = item["long"]
        if "lat" in item:
            y = item["lat"]
        if "x" in item:
            x = (item["x"]-1024)*size
        if "y" in item:
            y = (item["y"]-1024)*size
        if "color" in item:
            color = item["color"]
        pixels.append((x,y,color))
    return pixels
        
mapStyle = {
            'version': 8,
            'sources': {
                'raster-tiles': {
                    'type': 'raster',
                    #'tiles': ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                    'tiles': ['data/{z}/{x}/{y}.png'],
                    #'tiles': ["https://backend.wplace.live/files/s0/tiles/{x}/{y}.png"],
                    'tileSize': 256,
                    #'minzoom': 0,
                    #'maxzoom': 19
                }
            },
            'layers': [
                {
                    'id': 'simple-tiles',
                    'type': 'raster',
                    'source': 'raster-tiles',
                    'attribution': "© OpenStreetMap contributors",
                }
            ],
            'id': 'blank'
        }


@app.route('/')


def main():

    #featureCollection = {'type': 'FeatureCollection','features':[]}
    #feature = GenerateFeature([[0,0],[10,0],[10,10],[0,10]])
    #featureCollection["features"].append(GenerateFeature([[0,0],[0,10],[10,10],[10,0]]))
    #print(feature)
    #featureCollection = DrawPixels([(0,0),(20,0)])
    pixels = [(i,0,"black") for i in range(1000)]
    for j in range(10):
        pixels.extend([(i,j*2,"black") for i in range(1000)])

    pixels = LoadPixels()
    
    featureCollection = DrawPixels(pixels)
    return render_template('index.html',a_json = featureCollection,fill_colors = GetColorLibrary(),style = mapStyle)
#LoadPixels()
