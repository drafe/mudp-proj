from PIL import Image
from enum import Enum
import numpy as np


class Edge(Enum):
    X = 1
    Y = 2
    XY = 3


class SobelEdgeDetector:
    @staticmethod
    def _get_kernel(kernel_type: Edge):
        if kernel_type == Edge.X:
            kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        else:  # kernel_type == EDGE.Y:
            kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        return kernel

    @staticmethod
    def _L_edge_detect(image: Image, kernel_type: Edge = Edge.XY):
        def _kernel_step(x_, y_):
            num = np_img[y_:y_ + kernel_size, x_:x_ + kernel_size]
            return round(np.sum(num * kernel))

        w, h = image.size
        np_img = np.array(image)
        kernel_size = 3
        padding = kernel_size // 2
        if kernel_type == Edge.XY:
            x_img = SobelEdgeDetector._L_edge_detect(image, Edge.X)
            y_img = SobelEdgeDetector._L_edge_detect(image, Edge.Y)
            xy_img = np.linalg.norm(np.dstack((x_img, y_img)), axis=2).astype(int)
            new_im = Image.fromarray(xy_img)
            return new_im
        else:
            kernel = SobelEdgeDetector._get_kernel(kernel_type)
            w_new, h_new = w - 2 * padding, h - 2 * padding
            new_im = Image.new("L", (w_new, h_new))
            for x in range(w_new):
                for y in range(h_new):
                    avg_ = _kernel_step(x, y)
                    new_im.putpixel((x, y), avg_)
            return new_im

    @staticmethod
    def edge_detect(image: Image, kernel_type: Edge = Edge.XY):
        if image.mode == 'L':
            return SobelEdgeDetector._L_edge_detect(image, kernel_type)
        else:
            xy_img = np.linalg.norm(np.dstack([
                SobelEdgeDetector._L_edge_detect(ch, kernel_type) for ch in image.split()
            ]), axis=2).astype(int)
            new_im = Image.fromarray(xy_img).convert('L')
            return new_im


if __name__ == "__main__":
    filename = 'images/fruits.jpg'

    with Image.open(filename) as img:
        img.load()

    img_bw = img.convert('L')
    edges = SobelEdgeDetector.edge_detect(img)
    edges.show()

