import xml.etree.ElementTree as ET
import glob, os

# make sure to have a '/' at the beginning and end of the path string
# modify this as necessary
path_strings = [
    "/home/hpellerin/Documents/Programming/python/ai-robot/models/images/train/",
    "/home/hpellerin/Documents/Programming/python/ai-robot/models/images/", 
    "/home/hpellerin/Documents/Programming/python/ai-robot/models/images/test/"
]

for path_str in path_strings:
    os.chdir(path_str)
    for file_name in glob.glob("*.xml"):
        tree = ET.parse(file_name)
        image_name = tree.find("filename").text
        
        for elem in tree.findall("path"):
            elem.text = (path_str + image_name)

        tree.write(file_name)