from PIL import Image
from enum import Enum
import numpy as np


class Blurr(Enum):
    MEAN = 1
    GAUSS = 2


class Blurrer:

    @staticmethod
    def get_kernel(kernel: Blurr = Blurr.MEAN, kernel_size: int = 3):
        if kernel == Blurr.MEAN:
            return np.ones((kernel_size, kernel_size)) / kernel_size**2
        else:  # kernel == Blurr.GAUSS
            sigma = 1.0
            ax = np.linspace(-(kernel_size - 1) / 2., (kernel_size - 1) / 2., kernel_size)
            gauss = np.exp(-0.5 * np.square(ax) / np.square(sigma))
            kernel = np.outer(gauss, gauss)
            return kernel / np.sum(kernel)

    @staticmethod
    def blurr(image: Image, kernel_type: Blurr, kernel_size: int):
        def _kernel_step(x_, y_):
            index = range(kernel_size)
            num = np.array([[image.getpixel((x_ + i, y_ + j)) for j in index] for i in index])
            return round(np.sum(num * kernel))

        w, h = image.size
        padding = kernel_size // 2
        kernel = Blurrer.get_kernel(kernel_type, kernel_size)
        w_new, h_new = w - 2 * padding, h - 2 * padding
        new_im = Image.new("L", (w_new, h_new))
        for x in range(w_new):
            for y in range(h_new):
                avg_ = _kernel_step(x, y)
                new_im.putpixel((x, y), avg_)
        return new_im


if __name__ == "__main__":
    b_kernel = Blurrer.get_kernel(Blurr.GAUSS, 5)
    print(b_kernel)
    print(np.sum(b_kernel))

    filename = 'images/cow_gauss.png'

    with Image.open(filename) as img:
        img.load()

    img_bw = img.convert('L')
    smooth = Blurrer.blurr(img_bw, Blurr.MEAN, kernel_size=5)
    smooth.show()
