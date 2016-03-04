import time

timing_count = 0

def timing(f):
    """
    Simple annotation to keep track of the time spent calculating. It's a bit hacky due to the global
    variable but it's a simple solution for this case.
    """
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        args[0].timing_count += (time2 - time1) * 1000.0
        return ret
    return wrap

class Canvas(object):
    """
    Parent canvas with some commond method and fill method definition.
    It has some tooling to keep track of the data access and validation.
    Must be extended by the concrete implementations.
    """
    class access_count_array(list):
        """
        Access counter for image matrix.
        """

        def set_parent(self, parent):
            self.parent = parent

        def __getitem__(self, index):
            self.parent.pixel_comparisons += 1
            return list.__getitem__(self, index)

    def __init__(self, pixels):
        self.pixels = Canvas.access_count_array(pixels)
        self.pixels.set_parent(self)
        self.pixel_comparisons = 0
        self.timing_count = 0

    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(map(str, row)), self.pixels))

    def validate(self, x, y, color):
        """
        Common validation for the fill input

        :param x:  the x coordinate where the user clicked
        :param y: the y coordinate where the user clicked
        :param color: the specified color to change the region to
        """

        # check that the seed value are integers
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError(
                "Invalid pixel seed format. Expecting integers {},{}".format(
                    x, y))

        # check that the seed value are within the image interval
        if x < 0 or x >= len(self.pixels) \
                or y < 0 or y >= len(self.pixels[0]):
            raise ValueError(
                "Invalid pixel seed for flood fill {},{}".format(
                    x, y))

        # check that the image has a size
        if len(self.pixels) == 0 or len(self.pixels[0]) == 0:
            raise ValueError("Image has an empty dimension")

        # check that the image has consistent sizes accross its dimensions
        len_h = len(self.pixels[0])

        if any([len_h != len(pixels) for pixels in self.pixels]):
            raise ValueError("Invalid image. Rows and columns have inconsistent sizes")

        # check that the new color is the same type of the pixels
        data_type = type(self.pixels[0][0])

        # This check is not always valid. numpy uses uint8 integers while the user can be in int format
        # The algorithm is still able to run properly

        #color == self.pixels[x][y]
        #if type(color) is not data_type:
        #    raise ValueError("Pixel img and chosen color are of different types: {} and {}"
        #                     .format(type(color), data_type))

        # check that all image pixels have the same type
        for t in self.pixels:
            for y in t:
                if type(y) is not data_type:
                    raise ValueError("Image contains inconsistent data")


    def fill(self, x, y, color):
        """
        Fills a region of color at a given location with a given color.

        :param x:  the x coordinate where the user clicked
        :param y: the y coordinate where the user clicked
        :param color: the specified color to change the region to
        """
        raise NotImplementedError  # Override this function in the Solution classes
