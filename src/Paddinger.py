from PIL import Image
from enum import Enum


class Style(Enum):
    BLACK = 1
    MIRROR = 2
    CLAMP = 3
    # WRAP = 4


class Paddinger:
    """ Add different Style of paddings to image """

    @staticmethod
    def _black_padding(image: Image, padding_size: int) -> Image:
        w, h = image.size
        new_image = Image.new(image.mode, (w+2*padding_size, h+2*padding_size))
        for x in range(w):
            for y in range(h):
                pix = image.getpixel((x, y))
                new_image.putpixel((x+padding_size, y+padding_size), pix)
        return new_image

    @staticmethod
    def _mirror_padding(image: Image, padding_size: int) -> Image:
        w, h = image.size
        w_new, h_new = w + padding_size * 2, h + padding_size * 2
        new_image = Image.new(image.mode, (w_new, h_new))
        for x in range(w_new):
            for y in range(h_new):
                if x <= padding_size:
                    x_ = padding_size - x
                elif x >= w + padding_size:
                    x_ = 2 * w - x + padding_size - 1
                else:
                    x_ = x - padding_size

                if y <= padding_size:
                    y_ = padding_size - y
                elif y >= h + padding_size:
                    y_ = 2 * h - y + padding_size - 1
                else:
                    y_ = y - padding_size
                new_image.putpixel((x, y), image.getpixel((x_, y_)))
        return new_image

    @staticmethod
    def _clamp_padding(image, padding_size):
        w, h = image.size
        w_new, h_new = w + padding_size * 2, h + padding_size * 2
        new_image = Image.new(image.mode, (w_new, h_new))
        for x in range(w_new):
            for y in range(h_new):
                if x <= padding_size:
                    x_ = 0
                elif x >= w + padding_size:
                    x_ = w - 1
                else:
                    x_ = x - padding_size

                if y <= padding_size:
                    y_ = 0
                elif y >= h + padding_size:
                    y_ = h - 1
                else:
                    y_ = y - padding_size

                new_image.putpixel((x, y), image.getpixel((x_, y_)))
        return new_image

    @staticmethod
    def add_padding(image: Image, padding_size: int, padding_style: Style) -> Image:
        if padding_style in Style:
            if padding_style == Style.BLACK:
                new_image = Paddinger._black_padding(image, padding_size)
            elif padding_style == Style.MIRROR:
                new_image = Paddinger._mirror_padding(image, padding_size)
            elif padding_style == Style.CLAMP:
                new_image = Paddinger._clamp_padding(image, padding_size)
            else:
                new_image = Paddinger._black_padding(image, padding_size)
            return new_image
        else:
            raise TypeError('No such style')


if __name__ == "__main__":
    with Image.open('../images/fruits.jpg') as img:
        img.load()

    bw_img = img.convert('L')
    print(img.mode, bw_img.mode == 'L')
    new = Paddinger.add_padding(img, 20, Style.CLAMP)
    new.show()
