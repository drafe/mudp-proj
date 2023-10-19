from PIL import Image


class ImageChanger:
    def __init__(self, image: Image) -> None:
        self.image = image
        pass

    def change_brightness(self, brightness: int) -> Image:
        pass

    def change_contrast(self, contrast: float) -> Image:
        pass

    def change_contrast_n_brightness(self, contrast: float, brightness: int) -> Image:
        pass

    def inverse_colors(self) -> Image:
        pass

    def select_frame(self, point1: list[int], point2: list[int]) -> Image:
        pass

    def blend_image(self, another_image: Image, level: float) -> Image:
        pass

    def blurr_image(self, func='mean', kernel_size=3) -> Image:
        pass

    def detect_edge(self) -> Image:
        pass
