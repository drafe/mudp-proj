from PIL import Image


class ImageChanger:
    def __init__(self, image: Image) -> None:
        self.image = image
        self.mode = image.mode
        pass

    def change_brightness(self, brightness: int = 0) -> Image:
        """ This function create a copy of self.image,
        change brightness of copy and return changed image;

        :argument brightness ∈ [-255, 255];
            brightness = 0 return unchanged image;
            brightness ∈ [-255, 0) return image with low level of brightness;
            brightness ∈ (0, 255] return image with high level of brightness;

        Used function change_contrast_n_brightness"""

        pass

    def change_contrast(self, contrast: float = 1.0) -> Image:
        """ This function create a copy of self.image,
        change contrast of copy and return changed image

        :argument contrast ∈ [0.0, ...) ;
            contrast = 1 return unchanged image;
            contrast ∈ [0, 1) return image with low level of contrast;
            contrast > 1 return image with high level of contrast;

        Used function change_contrast_n_brightness"""

        pass

    def change_contrast_n_brightness(self, contrast: float, brightness: int) -> Image:
        """ This function create a copy of self.image,
        change contrast of copy and return changed image.

        If image mode is RGB then split image by r-g-b channels
        and work with them separately like black-white images.
        After all merge channels to new image and return it

        :argument contrast ∈ [0.0, ...) ;
            contrast = 1 return unchanged image;
            contrast ∈ [0, 1) return image with low level of contrast;
            contrast > 1 return image with high level of contrast;

        :argument brightness ∈ [-255, 255];
            brightness = 0 return unchanged image;
            brightness ∈ [-255, 0) return image with low level of brightness;
            brightness ∈ (0, 255] return image with high level of brightness;

        """

        pass

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
        and return it.

        :argument another_image is image to blend with
        :argument level ∈ [0, 1]
            level = 0 return just second image (another_image)
            level = 1 return just first image (self.image)
            level ∈ (0, 1) return mixed image with level*100% of first image
            and (1-level)*100% of second one

        If image mode is RGB then split image by r-g-b channels
        and work with them separately like black-white images.
        After all merge channels to new image and return it
        """
        pass

    def blurr_image(self, method='mean', kernel_size=3) -> Image:
        """ This function create a copy of self.image with paddings*
        and blurr it by chosen method.

        :argument method = ['mean', 'gauss']
        :argument kernel_size >=3

         *(padding size = kernel_size//2)
        """

        pass

    def detect_edge(self) -> Image:
        """ This function return image of edges detecting on self.image """

        pass
