from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

image = Image.open("TestImage.jpg")
print(image)
image_metadata = image._getexif()

for tag, value in image_metadata.items():
    key = TAGS.get(tag, tag)
    print(key + " " + str(value))