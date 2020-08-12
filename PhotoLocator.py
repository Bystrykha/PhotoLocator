from PIL import Image
import requests
import sys

url = input(str)
print("Image is uploading...")

try:
    resp = requests.get(url, stream=True).raw
except requests.exceptions.RequestException as e:
    sys.exit(1)

try:
    img = Image.open(resp)
    print("successfully")
except IOError:
    print("Unable to open image")
    sys.exit(1)

print("Getting meta data...")
exif = img._getexif()

if exif is not None:
    for (tag, value) in exif.items():
        if tag == 34853:
            print("Latitude:\t", value[2][0][0], "°", value[2][1][0], "′", value[2][2][0] / 10000, "″", value[1])
            print("Longitude:\t", value[4][0][0], "°", value[4][1][0], "′", value[4][2][0] / 10000, "″", value[3])
        if tag == 272:
            print("Camera:\t", value)
        if tag == 271:
            print("Device:\t", value)
        if tag == 36867:
            print("Create date:\t", value)
        if tag == 36868:
            print("Time Original:\t", value)

else:
    print("no data available")
