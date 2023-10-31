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
        
    def inverse_colors(img_in) -> Image:
        """ This function create a copy of self.image,
        change colors of copy to invert and return changed image.

        If image mode is RGB then split image by r-g-b channels
        and work with them separately like black-white images.
        After all merge channels to new image and return it """
        w, h = img_in.size
        img_out = Image.new('L',(w, h))
        for x in range(w):
            for y in range(h):
                original_pxl = img_in.getpixel((x, y)) # The value of the
                result_pxl = 255 - original_pxl
                img_out.putpixel((x, y), result_pxl)
        return img_out
        
    def color_invert(img):
        r, g, b = img.split()
        r_new = inverse_colors(r)
        g_new = inverse_colors(g)
        b_new = inverse_colors(b)
        img_out = Image.merge('RGB',[r_new, g_new, b_new])
        return img_out
    
    def select_frame(img, point1, point2) -> Image:
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
        img_f = img
        draw = ImageDraw.Draw(img_f)
        start = point1
        w = point2[0] - point1[0]
        h = point2[1] - point1[1]
        draw.rectangle([start, (w,h)], outline = (255, 0, 0), width = 3)
        img_f.show()

    def blend_image(img1, img2, alpha) -> Image:
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
        w1, h1 = img1.size
        w2, h2 = img2.size
        dw = abs(w1 - w2)
        dh = abs(h1 - h2)
        img_big = img1 if (w1 > w2 and h1 > h2) else img2
        img_small = img2 if (w1 > w2 and h1 > h2) else img1
        w = w2 if (w1 > w2) else w1
        h = h2 if (h1 > h2) else h1
        img_cut = Image.new('L', (w2, h2))
        for x in range(w):
            for y in range(h):
                pxl = img_big.getpixel((x+dw/2, y+dh/2))
                img_cut.putpixel((x, y), pxl)
        img_out = Image.new('L', (w, h))
        for x in range(w):
            for y in range(h):
                pxl1 = img_cut.getpixel((x, y))
                pxl2 = img_small.getpixel((x, y))
                result_pxl = int((1 - alpha)*pxl1 + alpha*pxl2)
                img_out.putpixel((x, y), result_pxl)
        return img_out

    def color_blend(img1, img2, alpha):
        r1, g1, b1 = img1.split()
        r2, g2, b2 = img2.split()
        r_new = blend_image(r1, r2, alpha)
        g_new = blend_image(g1, g2, alpha)
        b_new = blend_image(b1, b2, alpha)
        img_out = Image.merge('RGB',[r_new, g_new, b_new])
        return img_out
    
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
