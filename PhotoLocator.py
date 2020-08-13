from PIL import Image
import requests
import sys
import exifread

# ad = input(str)
ad = "/home/alex/Изображения/фото из сети/w.jpg"


def dict_print(dictionary):
    for (key, value) in dictionary.items():
        print(key, "\t", value)


def GetMeta_web(url):
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
        GPS_date = {}
        for (tag, value) in exif.items():
            if tag == 34853:
                Latitude = str(value[2][0][0]) + "°" + str(value[2][1][0]) + "′" + str(value[2][2][0] / 10000) + "″" + \
                           value[1]
                Longitude = str(value[4][0][0]) + "°" + str(value[4][1][0]) + "′" + str(
                    value[4][2][0] / 10000) + "″" + str(value[3])
                GPS_date["Latitude:"] = Latitude
                GPS_date["Longitude:"] = Longitude
            if tag == 36867:
                GPS_date["Create date:"] = value
        return GPS_date

    else:
        print("no data available")

    return exif


def GetMeta_HD(address):
    with open(address, 'rb') as f:
        GPS = {}
        tags = exifread.process_file(f, details=False)
        if 'GPS GPSLatitude' in tags.keys():
            GPS['Latitude:'] = str(tags["GPS GPSLatitude"]) + str(tags["GPS GPSLatitudeRef"])
            GPS['Longitude:'] = str(tags["GPS GPSLongitude"]) + str(tags["GPS GPSLongitudeRef"])

        else:
            GPS = {
                'Latitude': None,
                'Longitude': None,
            }
    return GPS


dict_print(GetMeta_HD(ad))

# if exif is not None:
#     for (tag, value) in exif.items():
#         if tag == 34853:
#             print("Latitude:\t", value[2][0][0], "°", value[2][1][0], "′", value[2][2][0] / 10000, "″", value[1])
#             print("Longitude:\t", value[4][0][0], "°", value[4][1][0], "′", value[4][2][0] / 10000, "″", value[3])
#         if tag == 272:
#             print("Camera:\t", value)
#         if tag == 271:
#             print("Device:\t", value)
#         if tag == 36867:
#             print("Create date:\t", value)
#         if tag == 36868:
#             print("Time Original:\t", value)
#
# else:
#     print("no data available")
