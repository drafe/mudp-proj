from PIL import Image
from Paddinger import Style, Paddinger
from Blurrer import Blurr, Blurrer
from SobelEdgeDetector import SobelEdgeDetector



class ImageChanger:
    def __init__(self, image: Image) -> None:
        self.image = image
        self.mode = image.mode

    def change_brightness(self, brightness: int = 0) -> Image:
        """ This function create a copy of self.image,
        change brightness of copy and return changed image;
        
        :param brightness ∈ [-255, 255];
            brightness = 0 return unchanged image;
            brightness ∈ [-255, 0) return image with low level of brightness;
            brightness ∈ (0, 255] return image with high level of brightness;
        """

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
        """ This function create a copy of self.image,
        change contrast of copy and return changed image;

        :param contrast ∈ [0.0, ...) ;
            contrast = 1 return unchanged image;
            contrast ∈ [0, 1) return image with low level of contrast;
            contrast > 1 return image with high level of contrast;
        """
        
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
        """ This function create a copy of self.image,
        change contrast of copy and return changed image.

        If image mode is RGB then split image by r-g-b channels
        and work with them separately like black-white images.
        After all merge channels to new image and return it;

        :param contrast ∈ [0.0, ...) ;
            contrast = 1 return unchanged image;
            contrast ∈ [0, 1) return image with low level of contrast;
            contrast > 1 return image with high level of contrast;

        :param brightness ∈ [-255, 255];
            brightness = 0 return unchanged image;
            brightness ∈ [-255, 0) return image with low level of brightness;
            brightness ∈ (0, 255] return image with high level of brightness;

        """

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


    def inverse_colors(self) -> Image:
        """ This function create a copy of self.image,
        change colors of copy to invert and return changed image.

        If image mode is RGB then split image by r-g-b channels
        and work with them separately like black-white images.
        After all merge channels to new image and return it """
        pass

    def select_frame(self, point1: list[int], point2: list[int]) -> Image:
        """ This function create a copy of self.image,
        paint a rectangle with corners on point1 and point2

        //   point1(0,0) point2(3,2)
        //    0    1    2    3
        // 0  ○──────────────┼──
        //    │              │
        // 1  │              │
        //    │              │
        // 2  ┼──────────────○ (3, 2)
        //    │
        //    │
        """
        pass

    def blend_image(self, another_image: Image, level: float) -> Image:
        """ This function check the sizes if self.image and another_image,
        cut images to the smallest one.
        Then create new image of smaller size then input ones
        as result of blending of both images according to level argument
        and return it;

        :param another_image is image to blend with;
        :param level ∈ [0, 1]
            level = 0 return just second image (another_image)
            level = 1 return just first image (self.image)
            level ∈ (0, 1) return mixed image with level*100% of first image
            and (1-level)*100% of second one

        If image mode is RGB then split image by r-g-b channels
        and work with them separately like black-white images.
        After all merge channels to new image and return it
        """
        pass

    def blurr_image(self, method: Blurr, kernel_size: int, padding_style: Style) -> Image:
        """ This function create a copy of self.image with paddings*
        and blurr it by chosen method.

        :argument method ∈ [Blurr.MEAN, Blurr.GAUSS]
        :argument kernel_size >=3
        :argument padding_style ∈ [Style.BLACK, Style.MIRROR, Style.CLAMP]

         *(padding size = kernel_size//2)
        """
        padded_image = Paddinger.add_padding(self.image, kernel_size // 2, padding_style)
        if self.mode == 'L':
            blurred_image = Blurrer.blurr(padded_image, method, kernel_size)
        else:
            blurred_image = Image.merge(self.mode,
                                        [Blurrer.blurr(ch, method, kernel_size) for ch in padded_image.split()])

        return blurred_image

    def detect_edge(self) -> Image:
        """ This function return image of edges detecting on self.image """
        kernel_size = 3
        padding_style = Style.MIRROR
        padded_image = Paddinger.add_padding(self.image, kernel_size // 2, padding_style)
        edged_image = SobelEdgeDetector.edge_detect(padded_image)
        return edged_image


if __name__ == '__main__':
    with Image.open('images/cow.jpg') as img:
        img.load()

    bw_img = img.convert('L')
    print(img.mode, bw_img.mode == 'L')
    im_ch = ImageChanger(image=img)
    # new = im_ch.blurr_image(method=Blurr.GAUSS, padding_style=Style.MIRROR, kernel_size=12)
    new = im_ch.detect_edge()
    new.show()
