from PIL import Image

filename = 'Qinglong.jpg'
with Image.open(filename) as img_Qinglong:
    img_Qinglong.load()
img_Qinglong.show()
