from PIL import Image
import ImageChanger

file_name = 'images/cow.jpg'

if __name__ == '__main__':
    with Image.open(file_name) as image:
        image.load()

    image.show()
