from PIL import Image



class ImageChanger:
    def __init__(self, image: Image) -> None:
        self.image = image
        self.mode = image.mode

    def change_brightness(self, brightness: int = 0) -> Image:
        new_image = self.image.copy()

        pixels = new_image.load()

        width, height = new_image.size
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                # Изменяем яркость каждого канала RGB и ограничиваем значения пикселей в диапазоне от 0 до 255
                r = max(0, min(r + brightness, 255))
                g = max(0, min(g + brightness, 255))
                b = max(0, min(b + brightness, 255))
                pixels[x, y] = (r, g, b)

        return new_image

    def change_contrast(self, contrast: float = 1.0) -> Image:
        new_image = self.image.copy()

        pixels = new_image.load()

        width, height = new_image.size
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                # Изменяем контрастность каждого канала RGB и ограничиваем значения пикселей в диапазоне от 0 до 255
                r = max(0, min(int((r - 128) * contrast + 128), 255))
                g = max(0, min(int((g - 128) * contrast + 128), 255))
                b = max(0, min(int((b - 128) * contrast + 128), 255))
                pixels[x, y] = (r, g, b)

        return new_image

    def change_contrast_n_brightness(self, contrast: float, brightness: int) -> Image:
        new_image = self.image.copy()

        pixels = new_image.load()

        width, height = new_image.size
        for x in range(width):
            for y in range(height):
                value = pixels[x, y]
                if self.mode == 'RGB':
                    # Если изображение в режиме 'RGB', разделим пиксель на каналы R, G, B
                    r, g, b = value

                    # Изменяем контрастность и яркость каждого канала RGB и ограничиваем значения пикселей в диапазоне от 0 до 255
                    r = max(0, min(int((r - 128) * contrast + 128) + brightness, 255))
                    g = max(0, min(int((g - 128) * contrast + 128) + brightness, 255))
                    b = max(0, min(int((b - 128) * contrast + 128) + brightness, 255))

                    # Обновляем значение пикселя с измененными каналами R, G, B
                    pixels[x, y] = (r, g, b)
                else:
                    # Если изображение в другом режиме, изменяем контрастность и яркость пикселя и ограничиваем значения в диапазоне от 0 до 255
                    new_value = max(0, min(int((value - 128) * contrast + 128) + brightness, 255))
                    pixels[x, y] = new_value

        return new_image



filename = 'cow.jpg'
with Image.open(filename) as image:
    image.load()
image.show()

changer = ImageChanger(image)
new_image1 = changer.change_brightness(brightness=100)
new_image2 = changer.change_contrast(contrast=3)
new_image3 = changer.change_contrast_n_brightness(contrast=4, brightness=100)

#new_image.save("output.png")
new_image1.show()
new_image2.show()
new_image3.show()